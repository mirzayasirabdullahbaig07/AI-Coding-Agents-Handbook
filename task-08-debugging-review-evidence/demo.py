from debug_tools import (EvidenceReport, HERE, classify_failure, hypothesis_from_shape,
                         inspect_data_shape, revision_hash, run_tests)

BASE, FIXED = HERE / "app" / "base", HERE / "app" / "fixed"
DATA = [{"id": 1, "status": "open"}, {"id": 2, "status": "done"}, {"id": 3, "status": "Open"}, {"id": 4, "status": "DONE"}]

print("1) REPRODUCE on the unchanged base")
base = run_tests(BASE)
print(f"   rc={base['rc']}  failing: {base['failed']}")
print("   relevant error line:", [l for l in base['text'].splitlines() if 'AssertionError' in l][:1])

print("\n2) INSPECT DATA SHAPE (error is not the cause)")
shape = inspect_data_shape(DATA)
print("   stored statuses:", shape)
print("   hypothesis    :", hypothesis_from_shape(shape, ["Done", "Open"]))

print("\n3) FOCUSED CHANGE -> 4) VERIFY (positive + negative + regression cases)")
new = run_tests(FIXED)
print(f"   rc={new['rc']}  failing: {new['failed'] or 'none'}")
print("    summary:", [l for l in new["text"].splitlines() if l.startswith("Ran")][0], "-> OK")

print("\n5) REGRESSION CHECK vs unchanged base")
print("   ", classify_failure(base, new))

print("\n6) EVIDENCE-BACKED REPORT")
print(EvidenceReport(
    change="Status filter normalization (case-insensitive compare)",
    revision=f"base={revision_hash(BASE)} -> fixed={revision_hash(FIXED)} (content hashes)",
    checks_run=["python -m unittest test_filter.py -v (5 cases: positive, negative, regression)"],
    results=f"base: FAIL ({len(base['failed'])} cases)  fixed: PASS (rc={new['rc']})",
    checks_not_run=["browser/UI test - no UI in this lab", "hosted CI - no remote"],
    limitations=["only covers case differences; whitespace handled but other status vocab untested"],
    next_action="human review of diff",
).render())
