from dataclasses import asdict
from multi_agent import run_graph, should_delegate, task_tracker_graph, find_conflicts

print("== When to delegate? ==")
for label, args in [("tiny label bug, one file", (1, False, False)),
                    ("feature + tests + review, clean boundaries", (4, True, False)),
                    ("review needs final diff", (4, True, True))]:
    print(f"  {label:<45} -> {should_delegate(*args)}")

g = task_tracker_graph()
print("\n== Delegation contract for the Implementation agent ==")
for k, v in asdict(g["implement"].contract).items():
    print(f"  {k:<14}: {v}")

print("\n== Task graph run ==")
res = run_graph(g)
for name, rep in res.items():
    print(f"  {name:<10} touched={rep['touched']}  {rep['notes']}")

print("\n== Same file given to two agents -> conflict ==")
g = task_tracker_graph(); g["test"].contract.allowed_files = ["tracker.py", "test_tracker.py"]
print("  ", find_conflicts(g, ["implement", "test"]))
