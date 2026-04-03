"""Git integration — branch-per-agent with auto-merge.

When enabled, each agent gets an isolated git worktree for their tick.
Changes are committed on the agent's branch and merged back to main.
This prevents file contention: Agent A and Agent B can both modify
the same file in the same tick, and git handles the merge.

Three contention strategies (configurable per preset):
  - branch-per-agent: git worktrees, full isolation (this module)
  - optimistic: no isolation, last write wins (default when git disabled)
  - lock: pessimistic file locking (future)

Designed so alternative strategies can be plugged in without changing
the engine or agent code — just the executor's working directory.
"""

from __future__ import annotations

import asyncio
import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass
class MergeResult:
    """Outcome of merging an agent's branch back to main."""
    agent_id: str
    agent_name: str
    branch: str
    success: bool
    files_changed: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)


class GitManager:
    """Manages git branch-per-agent using worktrees.

    Each agent gets an isolated working directory via git worktree.
    At tick end, changes are committed and merged back to main.
    Conflicts are detected and reported — agents resolve them next tick.

    Lifecycle per tick:
      1. create_agent_worktree() for each agent → returns working_dir
      2. Agents run concurrently in their own worktrees
      3. commit_and_merge() for each agent → returns MergeResult
      4. Workspace rescans to pick up merged changes
    """

    WORKTREE_BASE = ".agentciv/worktrees"

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.worktree_base = project_dir / self.WORKTREE_BASE
        self._agent_branches: dict[str, str] = {}  # agent_id → branch name
        self._main_branch: str = "main"
        self._initialized = False

    @staticmethod
    async def is_available() -> bool:
        """Check if git is installed on the system."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
            return proc.returncode == 0
        except FileNotFoundError:
            return False

    async def init(self) -> None:
        """Ensure the project directory is a git repository with a clean state."""
        if self._initialized:
            return

        # Ensure the project directory exists
        self.project_dir.mkdir(parents=True, exist_ok=True)

        git_dir = self.project_dir / ".git"
        if not git_dir.exists():
            # Fresh repo — initialise
            await self._run_git("init")
            # Add .agentciv/ to gitignore
            gitignore = self.project_dir / ".gitignore"
            existing = gitignore.read_text() if gitignore.exists() else ""
            if ".agentciv/" not in existing:
                with open(gitignore, "a") as f:
                    f.write("\n# AgentCiv Engine internals\n.agentciv/\n__pycache__/\n*.pyc\n")
            await self._run_git("add", "-A")
            await self._run_git(
                "commit", "-m", "AgentCiv: initial project state",
                "--allow-empty",
            )
            log.info("Initialised git repo at %s", self.project_dir)
        else:
            # Existing repo — snapshot any uncommitted changes
            status = await self._run_git("status", "--porcelain")
            if status.strip():
                await self._run_git("add", "-A")
                await self._run_git(
                    "commit", "-m", "AgentCiv: snapshot before run",
                    "--allow-empty",
                )
            log.info("Using existing git repo at %s", self.project_dir)

        # Detect the current branch name (main, master, etc.)
        self._main_branch = (
            await self._run_git("rev-parse", "--abbrev-ref", "HEAD")
        ).strip()

        # Clean up any stale worktrees from crashed runs
        await self._cleanup_stale_worktrees()
        self._initialized = True

    async def create_agent_worktree(
        self, agent_id: str, agent_name: str, tick: int,
    ) -> Path:
        """Create an isolated worktree for an agent.

        Returns the path to the worktree directory (agent's working_dir).
        The worktree starts from the current HEAD of main.
        """
        branch = f"agentciv/{agent_name.lower()}-tick-{tick}"
        worktree_dir = self.worktree_base / agent_id

        # Clean up if leftover from previous tick
        if worktree_dir.exists():
            try:
                await self._run_git(
                    "worktree", "remove", "--force", str(worktree_dir),
                )
            except Exception:
                shutil.rmtree(worktree_dir, ignore_errors=True)
                await self._run_git("worktree", "prune")

        # Delete branch if it exists from a previous run
        try:
            await self._run_git("branch", "-D", branch)
        except Exception:
            pass

        # Create worktree with new branch from HEAD
        self.worktree_base.mkdir(parents=True, exist_ok=True)
        try:
            await self._run_git(
                "worktree", "add", "-b", branch, str(worktree_dir),
            )
        except Exception as e:
            log.warning(
                "Failed to create worktree for %s: %s — falling back to project dir",
                agent_name, e,
            )
            # Ensure the directory exists even if git worktree add failed
            worktree_dir.mkdir(parents=True, exist_ok=True)

        # Verify the directory was actually created
        if not worktree_dir.exists():
            log.warning(
                "Worktree dir %s still missing after creation — creating manually",
                worktree_dir,
            )
            worktree_dir.mkdir(parents=True, exist_ok=True)

        self._agent_branches[agent_id] = branch
        log.debug(
            "Created worktree for %s at %s (branch: %s)",
            agent_name, worktree_dir, branch,
        )
        return worktree_dir

    async def commit_and_merge(
        self, agent_id: str, agent_name: str, tick: int,
    ) -> MergeResult:
        """Commit agent's worktree changes and merge back to main.

        Returns a MergeResult. On conflict, the merge is aborted and
        the conflict details are returned — the agent resolves next tick.
        """
        branch = self._agent_branches.get(agent_id)
        if not branch:
            return MergeResult(
                agent_id=agent_id, agent_name=agent_name,
                branch="unknown", success=True,
            )

        worktree_dir = self.worktree_base / agent_id
        if not worktree_dir.exists():
            return MergeResult(
                agent_id=agent_id, agent_name=agent_name,
                branch=branch, success=True,
            )

        # Stage all changes in the worktree
        await self._run_git("add", "-A", cwd=worktree_dir)

        # Check if there are actual changes to commit
        status = await self._run_git("status", "--porcelain", cwd=worktree_dir)
        if not status.strip():
            await self._cleanup_agent(agent_id, branch)
            return MergeResult(
                agent_id=agent_id, agent_name=agent_name,
                branch=branch, success=True,
            )

        # Commit the agent's changes
        await self._run_git(
            "commit", "-m", f"agentciv: {agent_name} tick {tick}",
            cwd=worktree_dir,
        )

        # Get list of changed files relative to main
        diff_output = await self._run_git(
            "diff", f"{self._main_branch}...HEAD", "--name-only",
            cwd=worktree_dir,
        )
        files_changed = [
            f.strip() for f in diff_output.strip().split("\n") if f.strip()
        ]

        # Merge into main (from the main working directory)
        try:
            await self._run_git("merge", branch, "--no-edit")
            log.info(
                "Merged %s's branch: %d files changed",
                agent_name, len(files_changed),
            )
            await self._cleanup_agent(agent_id, branch)
            return MergeResult(
                agent_id=agent_id, agent_name=agent_name,
                branch=branch, success=True,
                files_changed=files_changed,
            )
        except Exception:
            # Merge conflict — detect conflicted files
            try:
                conflict_output = await self._run_git(
                    "diff", "--name-only", "--diff-filter=U",
                )
                conflicts = [
                    f.strip()
                    for f in conflict_output.strip().split("\n")
                    if f.strip()
                ]
            except Exception:
                conflicts = files_changed  # fallback

            # Abort merge to keep main clean
            try:
                await self._run_git("merge", "--abort")
            except Exception:
                # If abort fails, hard reset to last good state
                try:
                    await self._run_git("reset", "--hard", "HEAD")
                except Exception:
                    pass

            log.warning(
                "Merge conflict for %s on files: %s",
                agent_name, conflicts,
            )
            await self._cleanup_agent(agent_id, branch)
            return MergeResult(
                agent_id=agent_id, agent_name=agent_name,
                branch=branch, success=False,
                files_changed=files_changed,
                conflicts=conflicts,
            )

    async def cleanup_all(self) -> None:
        """Remove all agentciv worktrees and branches."""
        await self._cleanup_stale_worktrees()
        # Remove agentciv branches
        try:
            result = await self._run_git("branch", "--list", "agentciv/*")
            for line in result.strip().split("\n"):
                branch = line.strip().lstrip("* ")
                if branch and branch.startswith("agentciv/"):
                    try:
                        await self._run_git("branch", "-D", branch)
                    except Exception:
                        pass
        except Exception:
            pass

    # --- Private helpers ---

    async def _cleanup_agent(self, agent_id: str, branch: str) -> None:
        """Remove an agent's worktree and branch."""
        worktree_dir = self.worktree_base / agent_id
        try:
            if worktree_dir.exists():
                await self._run_git(
                    "worktree", "remove", "--force", str(worktree_dir),
                )
        except Exception:
            shutil.rmtree(worktree_dir, ignore_errors=True)
        try:
            await self._run_git("branch", "-D", branch)
        except Exception:
            pass
        self._agent_branches.pop(agent_id, None)

    async def _cleanup_stale_worktrees(self) -> None:
        """Remove worktrees left over from crashed runs."""
        if self.worktree_base.exists():
            shutil.rmtree(self.worktree_base, ignore_errors=True)
        try:
            await self._run_git("worktree", "prune")
        except Exception:
            pass

    async def _run_git(self, *args: str, cwd: Path | None = None) -> str:
        """Run a git command and return stdout. Raises on non-zero exit."""
        cmd = ["git"] + list(args)
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(cwd or self.project_dir),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)

        if proc.returncode != 0:
            error = stderr.decode(errors="replace").strip()
            raise RuntimeError(f"git {' '.join(args)} failed: {error}")

        return stdout.decode(errors="replace")
