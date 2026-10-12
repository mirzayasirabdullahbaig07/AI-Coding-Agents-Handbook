"""Render real code + real command output into PNG screenshots with headless Chromium."""
import html
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

sys.path.insert(0, str(Path(__file__).parent))
from tasks_meta import TASKS

ROOT = Path(__file__).resolve().parent.parent
FMT = HtmlFormatter(style="monokai", nowrap=False, linenos="inline")

FRAME = """<!doctype html><meta charset=utf-8><style>
body{{margin:0;padding:28px;background:linear-gradient(135deg,#1d2433,#2b3550);width:1060px}}
.win{{background:#1e1f26;border-radius:12px;box-shadow:0 12px 40px #0008;overflow:hidden}}
.bar{{background:#2c2e38;padding:10px 14px;display:flex;align-items:center;gap:7px;font:13px system-ui,sans-serif;color:#b8bccb}}
.d{{width:12px;height:12px;border-radius:50%}} .r{{background:#ff5f57}} .y{{background:#febc2e}} .g{{background:#28c840}}
.t{{margin-left:10px}} pre{{margin:0;padding:16px 18px;font:14px/1.45 'DejaVu Sans Mono',Menlo,monospace;color:#e6e6e6;white-space:pre-wrap;word-break:break-word}}
.p{{color:#7ee787}} {css}
.highlight{{background:#1e1f26!important}} .highlight pre{{white-space:pre}} .linenos{{color:#6b7080;margin-right:14px}}
</style><div class=win><div class=bar><span class="d r"></span><span class="d y"></span><span class="d g"></span><span class=t>{title}</span></div>{body}</div>"""


def code_html(path: Path) -> str:
    return highlight(path.read_text(), PythonLexer(), FMT)


def term_html(cmd: str, out: str) -> str:
    return f"<pre><span class=p>$ {html.escape(cmd)}</span>\n{html.escape(out.rstrip())}</pre>"


def run(task_dir: Path, args, label):
    cp = subprocess.run([sys.executable, *args], cwd=task_dir, capture_output=True, text=True)
    return f"python {' '.join(args)}", (cp.stdout + cp.stderr)


def main():
    jobs = []   # (png_path, title, body_html)
    for t in TASKS:
        d = ROOT / t["folder"]
        (d / "screenshots").mkdir(exist_ok=True)
        s = d / "screenshots"
        jobs.append((s / "01_code_main.png", t["main"], code_html(d / t["main"])))
        jobs.append((s / "02_code_demo.png", "demo.py" if t["n"] != 10 else t["test"], code_html(d / ("demo.py" if t["n"] != 10 else t["test"]))))
        test_args = ["-m", "unittest", "discover", "-v"] if t["n"] != 10 else ["-m", "unittest", "discover", "-s", "tests", "-v"]
        jobs.append((s / "03_tests.png", "terminal - run the tests", term_html(*run(d, test_args, "tests"))))
        if t["n"] == 10:
            cmds = [(["-m", "task_tracker", "list", "--status", "done"], "04_cli_done.png"),
                    (["-m", "task_tracker", "list"], "05_cli_all.png"),
                    (["diagnose_bug.py"], "06_bug_diagnosis.png"),
                    (["generate_handoff.py"], "07_handoff_generated.png"),
                    (["rubric_check.py"], "08_rubric.png")]
            subprocess.run([sys.executable, "render_ui.py"], cwd=d, capture_output=True)
            subprocess.run([sys.executable, "generate_handoff.py"], cwd=d, capture_output=True)
            for args, name in cmds:
                jobs.append((s / name, "terminal", term_html(*run(d, args, name))))
            jobs.append((s / "09_demo_output.png", "terminal - python demo.py", term_html(*run(d, ["demo.py"], "demo"))))
        else:
            jobs.append((s / "04_demo_output.png", "terminal - python demo.py", term_html(*run(d, ["demo.py"], "demo"))))

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1116, "height": 400}, device_scale_factor=1.5)
        for png, title, body in jobs:
            pg.set_content(FRAME.format(css=FMT.get_style_defs(".highlight"), title=html.escape(title), body=body))
            pg.screenshot(path=str(png), full_page=True)
            print("shot", png.relative_to(ROOT))
        # Task Tracker UI (static html) screenshots
        ui = ROOT / "task-10-practice-lab"
        pg2 = b.new_page(viewport={"width": 760, "height": 300}, device_scale_factor=1.5)
        for name, n in [("all", "10_ui_all.png"), ("open", "11_ui_open.png"), ("done", "12_ui_done.png")]:
            pg2.goto((ui / "ui" / f"tracker_{name}.html").as_uri())
            pg2.screenshot(path=str(ui / "screenshots" / n), full_page=True)
            print("shot ui", n)
        b.close()


if __name__ == "__main__":
    main()
