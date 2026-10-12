import json, tempfile
from pathlib import Path
from orchestrator import Orchestrator, Permissions, TransientError

work = Path(tempfile.mkdtemp())
attempts = {"n": 0}

def read_tests():            return "3 existing tests found"
def flaky_ci_status():
    attempts["n"] += 1
    if attempts["n"] < 3:
        raise TransientError("CI API 503")
    return "CI reachable"
def write_file(path, text):  return f"wrote {path}"
def deploy_prod():           return "deployed"

tools = {"read_tests": read_tests, "ci_status": flaky_ci_status, "write_file": write_file, "deploy_prod": deploy_prod}
perms = Permissions(allowed_tools=set(tools), write_roots=["src/", "tests/"], needs_human={"deploy_prod"})

def run(title, plan, **kw):
    o = Orchestrator(tools, perms, work / "audit.jsonl", work / f"state_{title}.json", **kw)
    result = o.run(plan, lambda s: len(s["done"]) == len(plan))
    print(f"{title:<28} -> {result}")

print("== Orchestrator demo (permissions, retry, escalation) ==")
run("1 normal plan", [{"id": "inspect", "tool": "read_tests"},
                      {"id": "ci", "tool": "ci_status"},
                      {"id": "edit", "tool": "write_file", "args": {"path": "src/tracker.py", "text": "..."}}])
run("2 write outside scope", [{"id": "edit", "tool": "write_file", "args": {"path": "/etc/hosts", "text": "x"}}])
run("3 production deploy", [{"id": "ship", "tool": "deploy_prod"}])
print("\n== audit log (evidence is stored by the orchestrator) ==")
for line in (work / "audit.jsonl").read_text().splitlines():
    e = json.loads(line); e.pop("t")
    print(e)
