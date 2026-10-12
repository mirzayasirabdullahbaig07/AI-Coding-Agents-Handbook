from pathlib import Path

from context_packet import ASSUMPTION_PROMPT, ContextPacket, prepare, select_relevant_files

repo = Path(__file__).parent / "sample_repo"

print("1) Which files are relevant? (bounded budget, secrets skipped)")
chosen = select_relevant_files(repo, ["task", "filter", "status"], budget_tokens=400)
for f, t in chosen.items():
    print(f"   + {f:16s} ~{t} tokens")
print("   - billing.py  (irrelevant)   - auth.py  (contains a secret)\n")

print("2) The 6-line context packet")
packet = ContextPacket(
    goal="Add a status filter (All / Open / Done) to Task Tracker",
    files=list(chosen),
    current="All tasks are always shown",
    expected="Only tasks with the selected status are shown",
    constraints="Existing stack, stdlib only; no unrelated refactor",
    acceptance="All/Open/Done cases pass; current behaviour preserved",
)
print(packet.render(), "\n")
print("   gate ->", prepare(packet), "\n")

print("3) A bad packet: missing acceptance + leaked key")
bad = ContextPacket(goal="fix filter", files=["auth.py"], current="API_KEY=sk-demo-FAKEKEY0123456789abcdef",
                    expected="works", constraints="none")
print("   gate ->", prepare(bad), "\n")

print("4) Ask the agent for missing assumptions first:")
print("  ", ASSUMPTION_PROMPT)
