"""Task 04 - Orchestration layer: the control plane around the model.

Jobs implemented here (from the handbook): task routing, context assembly,
permissions, reliability (retry / timeout / checkpoint / logging) and
completion / escalation. A prompt alone cannot do any of these.
"""
from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutTimeout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class TransientError(Exception):
    """Failure worth retrying (network blip, lock...)."""


class PermissionDenied(Exception):
    pass


class Escalate(Exception):
    """Human authority/information needed."""


@dataclass
class Permissions:
    allowed_tools: set
    write_roots: List[str] = field(default_factory=list)   # directories tools may write in
    needs_human: set = field(default_factory=set)          # e.g. {"deploy_prod"}

    def check(self, tool: str, path: Optional[str] = None) -> None:
        if tool in self.needs_human:
            raise Escalate(f"'{tool}' requires human approval")
        if tool not in self.allowed_tools:
            raise PermissionDenied(f"tool '{tool}' not allowed")
        if path is not None and not any(path.startswith(r) for r in self.write_roots):
            raise PermissionDenied(f"path '{path}' outside write scope {self.write_roots}")


@dataclass
class Orchestrator:
    tools: Dict[str, Callable[..., Any]]
    permissions: Permissions
    audit_path: Path
    state_path: Path
    max_retries: int = 2
    timeout_s: float = 5.0
    backoff_s: float = 0.01
    state: Dict[str, Any] = field(default_factory=lambda: {"done": [], "results": {}})

    # ---------- logging / checkpoints ----------
    def _log(self, **event) -> None:
        event["t"] = round(time.time(), 3)
        with self.audit_path.open("a") as f:
            f.write(json.dumps(event, default=str) + "\n")

    def checkpoint(self) -> None:
        self.state_path.write_text(json.dumps(self.state, indent=2, default=str))

    @classmethod
    def resume_state(cls, state_path: Path) -> Dict[str, Any]:
        return json.loads(Path(state_path).read_text())

    # ---------- executing one step ----------
    def call(self, step_id: str, tool: str, **args) -> Any:
        self.permissions.check(tool, args.get("path"))        # permission BEFORE execution
        attempt = 0
        while True:
            attempt += 1
            try:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    result = ex.submit(self.tools[tool], **args).result(timeout=self.timeout_s)
                self._log(step=step_id, tool=tool, attempt=attempt, status="ok")
                return result
            except TransientError as exc:                       # only transient errors retry
                self._log(step=step_id, tool=tool, attempt=attempt, status="transient", error=str(exc))
                if attempt > self.max_retries:
                    raise Escalate(f"{tool} still failing after {attempt} attempts: {exc}")
                time.sleep(self.backoff_s * attempt)
            except FutTimeout:
                self._log(step=step_id, tool=tool, attempt=attempt, status="timeout")
                raise Escalate(f"{tool} timed out after {self.timeout_s}s")

    # ---------- the plan runner (routing + completion logic) ----------
    def run(self, plan: List[dict], is_complete: Callable[[Dict[str, Any]], bool]) -> dict:
        for step in plan:
            sid = step["id"]
            if sid in self.state["done"]:                         # resume after crash
                self._log(step=sid, status="skipped (checkpoint)")
                continue
            try:
                res = self.call(sid, step["tool"], **step.get("args", {}))
            except (PermissionDenied, Escalate) as exc:
                kind = "ESCALATE" if isinstance(exc, Escalate) else "DENIED"
                self._log(step=sid, status=kind, reason=str(exc))
                self.checkpoint()
                return {"status": kind, "step": sid, "reason": str(exc)}
            self.state["results"][sid] = res
            self.state["done"].append(sid)
            self.checkpoint()
        return {"status": "COMPLETE" if is_complete(self.state) else "INCOMPLETE",
                "done": list(self.state["done"])}
