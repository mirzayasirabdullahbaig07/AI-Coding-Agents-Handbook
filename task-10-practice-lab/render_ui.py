"""Render a static HTML view of the Task Tracker per filter (used for screenshots)."""
import html
from pathlib import Path

from task_tracker import filter_tasks, load_tasks

OUT = Path(__file__).parent / "ui"
CSS = """body{font-family:system-ui,sans-serif;background:#f6f7f9;margin:0;padding:32px;color:#1c2330}
.card{max-width:640px;margin:auto;background:#fff;border-radius:14px;box-shadow:0 2px 12px #0001;padding:24px}
h1{margin:0 0 16px;font-size:22px}.tabs{display:flex;gap:8px;margin-bottom:16px}
.tab{padding:6px 16px;border-radius:999px;background:#eef0f4;font-size:14px}.tab.on{background:#2f5bea;color:#fff}
.row{display:flex;align-items:center;gap:12px;padding:12px 4px;border-top:1px solid #eee}
.pill{font-size:12px;padding:2px 10px;border-radius:999px}.open{background:#fff3d6;color:#8a5a00}.done{background:#d9f5e3;color:#176b3a}
.id{color:#8a93a5;width:24px}.count{color:#6b7488;font-size:13px;margin-top:12px}"""


def page(active: str) -> str:
    tasks = filter_tasks(load_tasks(), active)
    tabs = "".join(f"<span class='tab {'on' if s == active else ''}'>{s.capitalize()}</span>" for s in ("all", "open", "done"))
    rows = "".join(f"<div class='row'><span class='id'>{t['id']}</span><span style='flex:1'>{html.escape(t['title'])}</span>"
                   f"<span class='pill {t['status'].lower()}'>{t['status'].lower()}</span></div>" for t in tasks)
    return (f"<!doctype html><meta charset=utf-8><style>{CSS}</style><div class=card><h1>Task Tracker</h1>"
            f"<div class=tabs>{tabs}</div>{rows}<div class=count>Showing {len(tasks)} task(s) - filter: {active}</div></div>")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for s in ("all", "open", "done"):
        (OUT / f"tracker_{s}.html").write_text(page(s))
        print("wrote", OUT / f"tracker_{s}.html")
