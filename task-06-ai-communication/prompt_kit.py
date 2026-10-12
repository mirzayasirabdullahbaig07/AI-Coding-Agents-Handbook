"""Task 06 - Communicating with AI: structured prompts + a prompt grader.

Structure: Goal -> Context -> Scope -> Constraints -> Acceptance criteria
           -> Verification -> Required response
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

SECTIONS = ["goal", "context", "scope", "constraints", "acceptance", "verification", "response"]

# keyword evidence that a section exists in free text
SIGNALS = {
    "goal": r"\b(fix|add|implement|explain|review|diagnose|goal|bug|wrong|shows?)\b",
    "context": r"\b(currently|observed|expected|file|component|because|context)\b",
    "scope": r"\b(scope|only|allowed|limit(ed)? to|files?:)\b",
    "constraints": r"\b(preserve|no unrelated|do not|don't|without|constraint|no new dependenc)",
    "acceptance": r"\b(acceptance|criteria|should|must|expected)\b",
    "verification": r"\b(run|test|check|verify|verification)\b",
    "response": r"\b(report|response|list|show me|give me|diff|assumptions)\b",
}


@dataclass
class PromptSpec:
    goal: str
    context: str
    scope: str
    constraints: str
    acceptance: str
    verification: str
    response: str

    def render(self) -> str:
        return (f"Goal: {self.goal}\nContext: {self.context}\nScope: {self.scope}\n"
                f"Constraints: {self.constraints}\nAcceptance criteria: {self.acceptance}\n"
                f"Verification: {self.verification}\nRequired response: {self.response}")


def grade(prompt: str) -> Dict[str, object]:
    """Score a free-text prompt 0..7 by which sections it covers. Heuristic, not magic."""
    found = {k: bool(re.search(rx, prompt, re.I)) for k, rx in SIGNALS.items()}
    if len(prompt.split()) < 6:                    # too short to carry real context
        found = {k: (k == "goal" and found[k]) for k in found}
    score = sum(found.values())
    level = "Weak" if score <= 2 else "Better" if score <= 5 else "Strong"
    return {"score": score, "of": len(SECTIONS), "level": level,
            "missing": [k for k, v in found.items() if not v]}


TEMPLATES = {
    "explain": "Explain this feature's data flow in simple terms. Name the relevant files/functions, list "
               "assumptions and unclear points separately. Do not modify code.",
    "diagnose": "Compare observed vs expected behavior and test the likely cause with evidence. Do not modify "
                "files. Give the next smallest verification step.",
    "bounded_change": "Make the minimum coherent change for this acceptance criteria. Follow the allowed scope, "
                      "run relevant checks, and report diff + results + limitations.",
    "review_diff": "Review this diff without modifying it. Check correctness, regressions, security/data access "
                   "and missing tests. Give findings with evidence and severity.",
}

DAILY = ("Goal: {task}. Context: {context}. Scope: {scope}. Constraints: preserve existing behavior; no "
         "unrelated refactor. Acceptance: {acceptance}. Verification: run appropriate checks and inspect diff. "
         "Response: assumptions, changes, exact revision/checks/results, checks not run, limitations, next action.")

WEAK = "Fix the filter."
BETTER = "The status filter shows Open tasks when Done is selected. Expected: only Done tasks."
STRONG = PromptSpec(
    goal="Fix the Task Tracker status filter",
    context="Selecting Done also returns Open tasks (stored status is lowercase 'done').",
    scope="filter component + relevant tests only",
    constraints="Preserve existing All behavior; no unrelated refactor; no new dependencies",
    acceptance="All/Open/Done return the right tasks; Done never contains Open",
    verification="Run the Open/Done/All checks and inspect the diff",
    response="Report diff, assumptions, exact checks/results and remaining uncertainty",
).render()

FORBIDDEN_ASKS = [r"chain[- ]of[- ]thought", r"hidden reasoning", r"your (private|internal) thoughts"]


def lint_response_request(prompt: str) -> List[str]:
    """Handbook: ask for concise rationale + verification, NOT hidden chain-of-thought."""
    return [p for p in FORBIDDEN_ASKS if re.search(p, prompt, re.I)]
