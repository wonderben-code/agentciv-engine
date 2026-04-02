"""Action executor — bridges agent decisions to real file-system operations.

Takes an Action from the cognitive loop and executes it against the workspace.
Returns an ActionResult the agent can observe and reflect on.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from ..core.types import Action, ActionResult, ActionType
from ..core.attention import AttentionMap
from .workspace import Workspace

log = logging.getLogger(__name__)


class WorkspaceExecutor:
    """Executes agent actions against the real file system.

    When git branching is enabled, `working_dir` is set to the agent's
    worktree. All file operations and commands run in that directory,
    giving each agent true isolation during their tick.
    """

    def __init__(
        self,
        workspace: Workspace,
        attention: AttentionMap | None = None,
        allowed_commands: list[str] | None = None,
        working_dir: Path | None = None,
    ):
        self.workspace = workspace
        self.attention = attention
        self.working_dir = working_dir  # None = use workspace.project_dir
        # Whitelist of allowed shell commands (safety)
        self.allowed_commands = allowed_commands or [
            "python", "python3", "pip", "npm", "node", "npx",
            "pytest", "ruff", "mypy", "tsc", "eslint",
            "cargo", "go", "make", "cat", "ls", "grep",
        ]

    @property
    def effective_dir(self) -> Path:
        """The directory where file operations and commands run."""
        return self.working_dir or self.workspace.project_dir

    async def execute(self, action: Action) -> ActionResult:
        """Execute an action and return the result."""
        try:
            match action.type:
                case ActionType.READ_FILE:
                    return self._read_file(action)
                case ActionType.WRITE_FILE:
                    return self._write_file(action)
                case ActionType.CREATE_FILE:
                    return self._create_file(action)
                case ActionType.DELETE_FILE:
                    return self._delete_file(action)
                case ActionType.RUN_COMMAND:
                    return await self._run_command(action)
                case ActionType.COMMUNICATE | ActionType.BROADCAST:
                    return self._communicate(action)
                case ActionType.CLAIM_TASK:
                    return self._claim_task(action)
                case ActionType.RELEASE_TASK:
                    return self._release_task(action)
                case ActionType.REQUEST_REVIEW:
                    return ActionResult(success=True, output="Review requested")
                case ActionType.PROPOSE_RESTRUCTURE | ActionType.VOTE:
                    return ActionResult(success=True, output=f"{action.type.name} recorded")
                case ActionType.IDLE:
                    return ActionResult(success=True, output="Waiting")
                case _:
                    return ActionResult(success=False, error=f"Unknown action: {action.type}")
        except Exception as e:
            log.exception("Action execution failed: %s", action.type.name)
            return ActionResult(success=False, error=str(e))

    def _read_file(self, action: Action) -> ActionResult:
        if not action.file_path:
            return ActionResult(success=False, error="No file path specified")

        # Read from agent's working directory (worktree or main)
        full_path = self.effective_dir / action.file_path
        if not full_path.exists():
            return ActionResult(success=False, error=f"File not found: {action.file_path}")

        content = full_path.read_text(errors="replace")

        # Truncate very large files for context window sanity
        if len(content) > 50_000:
            content = content[:50_000] + f"\n... [truncated, {len(content)} chars total]"

        return ActionResult(success=True, output=content)

    def _write_file(self, action: Action) -> ActionResult:
        if not action.file_path:
            return ActionResult(success=False, error="No file path specified")
        if not action.content:
            return ActionResult(success=False, error="No content to write")

        # Safety: don't write outside working dir
        base = self.effective_dir.resolve()
        full_path = (self.effective_dir / action.file_path).resolve()
        if not str(full_path).startswith(str(base)):
            return ActionResult(success=False, error="Path escapes project directory")

        # Contention warning via attention map
        warning = ""
        if self.attention:
            other = self.attention.is_file_being_worked_on(
                action.file_path, exclude_agent=action.agent_id,
            )
            if other:
                warning = f" WARNING: {other} is also working on this file."

        # Write to agent's working directory (worktree or main)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(action.content)
        # Update workspace metadata centrally
        self.workspace.update_file_metadata(
            action.file_path, action.agent_id, action.tick, len(action.content),
        )
        return ActionResult(
            success=True,
            output=f"Written {len(action.content)} chars to {action.file_path}.{warning}",
        )

    def _create_file(self, action: Action) -> ActionResult:
        if not action.file_path:
            return ActionResult(success=False, error="No file path specified")

        base = self.effective_dir.resolve()
        full_path = (self.effective_dir / action.file_path).resolve()
        if not str(full_path).startswith(str(base)):
            return ActionResult(success=False, error="Path escapes project directory")

        if full_path.exists():
            return ActionResult(success=False, error=f"File already exists: {action.file_path}")

        content = action.content or ""
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        self.workspace.update_file_metadata(
            action.file_path, action.agent_id, action.tick, len(content),
        )
        return ActionResult(
            success=True,
            output=f"Created {action.file_path} ({len(content)} chars)",
        )

    def _delete_file(self, action: Action) -> ActionResult:
        if not action.file_path:
            return ActionResult(success=False, error="No file path specified")

        full_path = self.effective_dir / action.file_path
        if not full_path.exists():
            return ActionResult(success=False, error=f"File not found: {action.file_path}")

        full_path.unlink()
        self.workspace.files.pop(action.file_path, None)
        return ActionResult(success=True, output=f"Deleted {action.file_path}")

    async def _run_command(self, action: Action) -> ActionResult:
        if not action.command:
            return ActionResult(success=False, error="No command specified")

        # Safety: check command against whitelist
        first_word = action.command.split()[0]
        if first_word not in self.allowed_commands:
            return ActionResult(
                success=False,
                error=f"Command '{first_word}' not in allowed list: {self.allowed_commands}",
            )

        try:
            proc = await asyncio.create_subprocess_shell(
                action.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.effective_dir),
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)

            output = stdout.decode(errors="replace")
            errors = stderr.decode(errors="replace")

            if proc.returncode == 0:
                # Update workspace state based on command
                if any(x in action.command for x in ["test", "pytest", "jest"]):
                    self.workspace.test_status = "passing"
                elif any(x in action.command for x in ["build", "tsc", "make"]):
                    self.workspace.build_status = "passing"
                return ActionResult(success=True, output=output[:10_000])
            else:
                if any(x in action.command for x in ["test", "pytest", "jest"]):
                    self.workspace.test_status = "failing"
                elif any(x in action.command for x in ["build", "tsc", "make"]):
                    self.workspace.build_status = "failing"
                return ActionResult(
                    success=False,
                    output=output[:5_000],
                    error=errors[:5_000],
                    side_effects=[f"exit code {proc.returncode}"],
                )
        except asyncio.TimeoutError:
            return ActionResult(success=False, error="Command timed out (60s)")

    def _communicate(self, action: Action) -> ActionResult:
        # Communication is handled by the engine (message routing)
        # The executor just validates
        if not action.content:
            return ActionResult(success=False, error="No message content")
        return ActionResult(success=True, output="Message sent")

    def _claim_task(self, action: Action) -> ActionResult:
        if action.content:
            # Update agent's focus
            return ActionResult(success=True, output=f"Claimed: {action.content}")
        return ActionResult(success=False, error="No task description")

    def _release_task(self, action: Action) -> ActionResult:
        return ActionResult(success=True, output="Task released")
