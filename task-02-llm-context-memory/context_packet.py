"""Task 02 - Context packet: relevant, current, bounded information.

A 6-field packet (Goal, Files, Current, Expected, Constraints, Acceptance)
plus guards: secret scanning and a token budget for file selection.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Dict, List

FIELDS = ["goal", "files", "current", "expected", "constraints", "acceptance"]

SECRET_PATTERNS = {
    "api key": re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    "aws key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "password assignment": re.compile(r"(?i)\b(password|passwd|pwd|secret|token)\b\s*[=:]\s*['\"][^'\"]{4,}['\"]"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "email (possible customer data)": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
}


@dataclass
class ContextPacket:
    goal: str = ""
    files: List[str] = field(default_factory=list)
    current: str = ""
    expected: str = ""
    constraints: str = ""
    acceptance: str = ""

    def missing(self) -> List[str]:
        return [f for f in FIELDS if not getattr(self, f)]

    def render(self) -> str:
        files = ", ".join(self.files) or "-"
        return "\n".join([
            f"Goal: {self.goal}",
            f"Files: {files}",
            f"Current: {self.current}",
            f"Expected: {self.expected}",
            f"Constraints: {self.constraints}",
            f"Acceptance criteria: {self.acceptance}",
        ])


def scan_secrets(text: str) -> List[str]:
    return [name for name, rx in SECRET_PATTERNS.items() if rx.search(text)]


def estimate_tokens(text: str) -> int:
    """Rough rule of thumb: ~4 characters per token."""
    return max(1, len(text) // 4)


def select_relevant_files(repo: Path, keywords: List[str], budget_tokens: int = 400) -> Dict[str, int]:
    """Rank files by keyword hits; include best ones until the budget is used.

    Files that contain secrets are skipped entirely (never put in context).
    Returns {relative_path: estimated_tokens}.
    """
    scored = []
    for p in sorted(Path(repo).rglob("*")):
        if not p.is_file() or p.suffix not in {".py", ".md"}:
            continue
        text = p.read_text()
        if scan_secrets(text):
            continue
        hits = sum(text.lower().count(k.lower()) for k in keywords)
        if p.name == "AGENTS.md":          # repository instructions always matter
            hits += 100
        if hits:
            scored.append((hits, p, estimate_tokens(text)))
    chosen, used = {}, 0
    for hits, p, tok in sorted(scored, key=lambda t: -t[0]):
        if used + tok > budget_tokens:
            continue
        chosen[str(p.relative_to(repo))] = tok
        used += tok
    return chosen


def prepare(packet: ContextPacket) -> dict:
    """Gate: refuse to send a packet that is incomplete or leaks secrets."""
    problems = []
    if packet.missing():
        problems.append(f"missing fields: {', '.join(packet.missing())}")
    leaks = scan_secrets(packet.render())
    if leaks:
        problems.append(f"possible secrets in context: {', '.join(leaks)}")
    return {"ok": not problems, "problems": problems,
            "tokens": estimate_tokens(packet.render())}


ASSUMPTION_PROMPT = ("Before coding, list every assumption you are making and anything "
                     "in this packet that is missing or ambiguous.")
