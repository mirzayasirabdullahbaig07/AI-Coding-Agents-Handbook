from prompt_kit import BETTER, STRONG, TEMPLATES, WEAK, grade

print("== Weak -> Better -> Strong ==")
for name, p in [("Weak", WEAK), ("Better", BETTER), ("Strong", STRONG)]:
    g = grade(p)
    print(f"\n[{name}] score {g['score']}/{g['of']} -> {g['level']}   missing: {g['missing'] or 'nothing'}")
    print("  " + p.replace("\n", "\n  "))

print("\n== Copy-ready templates ==")
for k, v in TEMPLATES.items():
    print(f"\n{k}:\n  {v}")
