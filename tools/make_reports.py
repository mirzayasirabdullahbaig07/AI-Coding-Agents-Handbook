"""Build report.pdf + README.md for every task from real test runs and the screenshots."""
import hashlib
import io
import subprocess
import sys
from datetime import date
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (HRFlowable, Image as RLImage, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).parent))
from tasks_meta import TASKS

ROOT = Path(__file__).resolve().parent.parent
W, H = A4
CW = W - 4 * cm
ss = getSampleStyleSheet()
BLUE = colors.HexColor("#2f5bea")
S = dict(
    title=ParagraphStyle("t", parent=ss["Title"], fontSize=22, leading=27, textColor=colors.HexColor("#1c2330"), alignment=0),
    sub=ParagraphStyle("s", parent=ss["Normal"], fontSize=10.5, textColor=colors.HexColor("#6b7488")),
    h=ParagraphStyle("h", parent=ss["Heading2"], fontSize=14, textColor=BLUE, spaceBefore=14, spaceAfter=6),
    body=ParagraphStyle("b", parent=ss["BodyText"], fontSize=10.5, leading=15),
    bullet=ParagraphStyle("bl", parent=ss["BodyText"], fontSize=10.5, leading=15, leftIndent=14, bulletIndent=2),
    cap=ParagraphStyle("c", parent=ss["Normal"], fontSize=8.5, textColor=colors.HexColor("#6b7488"), spaceAfter=8),
    cell=ParagraphStyle("cell", parent=ss["Normal"], fontSize=9.5, leading=13),
)


def tests_cmd(t):
    return ["-m", "unittest", "discover", "-v"] if t["n"] != 10 else ["-m", "unittest", "discover", "-s", "tests", "-v"]


def run_tests(d, t):
    cp = subprocess.run([sys.executable, *tests_cmd(t)], cwd=d, capture_output=True, text=True)
    out = cp.stdout + cp.stderr
    ran = [l for l in out.splitlines() if l.startswith("Ran ")][0]
    return cp.returncode, ran


def rev_hash(d):
    h = hashlib.sha256()
    for p in sorted(d.rglob("*.py")):
        if "__pycache__" in p.parts:
            continue
        h.update(str(p.relative_to(d)).encode()); h.update(p.read_bytes())
    return h.hexdigest()[:12]


def slices(png: Path, max_h_pt=640):
    """Split a tall screenshot into page-sized pieces. Returns list of RLImage."""
    im = Image.open(png)
    scale = CW / im.width
    step = int(max_h_pt / scale)
    out = []
    for top in range(0, im.height, step):
        piece = im.crop((0, top, im.width, min(im.height, top + step)))
        buf = io.BytesIO(); piece.save(buf, "PNG"); buf.seek(0)
        out.append(RLImage(buf, width=CW, height=piece.height * scale))
    return out


def shot(d, name, caption):
    p = d / "screenshots" / name
    parts = slices(p)
    items = [parts[0], Paragraph(caption, S["cap"])] if len(parts) == 1 else []
    if len(parts) > 1:
        items = []
        for i, part in enumerate(parts, 1):
            items += [part, Paragraph(f"{caption} (part {i}/{len(parts)})", S["cap"])]
    return items


def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#8a93a5"))
    canvas.drawString(2 * cm, 1.2 * cm, "AI Coding Agents - Intern Handbook | Task Tracker learning path")
    canvas.drawRightString(W - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def kv_table(rows):
    data = [[Paragraph(f"<b>{k}</b>", S["cell"]), Paragraph(v, S["cell"])] for k, v in rows]
    t = Table(data, colWidths=[4.2 * cm, CW - 4.2 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9dde6")),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f4fb")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def build(t):
    d = ROOT / t["folder"]
    rc, ran = run_tests(d, t)
    status = "PASS" if rc == 0 else "FAIL"
    files = sorted(str(p.relative_to(d)) for p in d.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.suffix in {".py", ".json", ".md", ".html"}
                   and p.name not in {"README.md"} and "screenshots" not in p.parts)
    test_cmd = "python " + " ".join(tests_cmd(t)).replace(" -v", "")
    st = []
    st += [Paragraph(f"Task {t['n']:02d} - {t['title']}", S["title"]),
           Paragraph(f"Handbook reference: {t['page']} of 10 &nbsp;|&nbsp; Report date: {date.today().isoformat()} &nbsp;|&nbsp; "
                     f"Folder: <font face='Courier'>{t['folder']}/</font>", S["sub"]),
           Spacer(1, 6), HRFlowable(width="100%", color=BLUE, thickness=1.2)]
    st += [Paragraph("1. Concept from the handbook", S["h"]), Paragraph(t["concept"], S["body"])]
    st += [Paragraph("2. What was built", S["h"]), Paragraph(t["built"], S["body"])]
    st += [Paragraph("3. Behaviours demonstrated", S["h"])]
    st += [Paragraph(p, S["bullet"], bulletText="•") for p in t["points"]]
    st += [Paragraph("4. Files in this task", S["h"]),
           Paragraph(", ".join(f"<font face='Courier'>{f}</font>" for f in files), S["body"]),
           Paragraph(f"Run it: <font face='Courier'>python demo.py</font> &nbsp;&nbsp; Test it: <font face='Courier'>{test_cmd}</font>"
                     if t["n"] != 10 else "Run it: <font face='Courier'>python demo.py</font> &nbsp;&nbsp; Test it: "
                     "<font face='Courier'>python -m unittest discover -s tests</font>", S["body"])]
    st += [PageBreak(), Paragraph("5. Code screenshots", S["h"])]
    st += shot(d, "01_code_main.png", f"Main implementation: {t['main']}")
    st += shot(d, "02_code_demo.png", "Demo script" if t["n"] != 10 else f"Test file: {t['test']}")
    st += [PageBreak(), Paragraph("6. Demo and test screenshots", S["h"])]
    st += shot(d, "03_tests.png", "Test run (real output)")
    if t["n"] == 10:
        for n, c in [("04_cli_done.png", "CLI: list --status done"), ("05_cli_all.png", "CLI: list (existing behaviour preserved)"),
                     ("06_bug_diagnosis.png", "Bug diagnosis script"), ("07_handoff_generated.png", "PR handoff generated from real results"),
                     ("08_rubric.png", "5-point rubric self-check"), ("09_demo_output.png", "Full demo run"),
                     ("10_ui_all.png", "UI render - All"), ("11_ui_open.png", "UI render - Open"), ("12_ui_done.png", "UI render - Done")]:
            st += shot(d, n, c)
    else:
        st += shot(d, "04_demo_output.png", "Demo output (python demo.py)")
    ev = [("Change", t["title"]), ("Revision tested", f"content hash <font face='Courier'>{rev_hash(d)}</font> of all .py files in this folder "
                                                      "(re-run with the git commit SHA after you commit)"),
          ("Checks run", f"<font face='Courier'>{test_cmd}</font> and <font face='Courier'>python demo.py</font>"),
          ("Results", f"<b>{status}</b> - {ran}"), ("Checks not run", "; ".join(t["not_run"])),
          ("Known limitations", "; ".join(t["limits"])), ("Next required action", "Human review, then CI on the pull request")]
    st += [KeepTogether([Paragraph("7. Evidence-backed report", S["h"]), kv_table(ev),
                         Paragraph("8. Practical takeaway", S["h"]), Paragraph(t["takeaway"], S["body"])])]
    SimpleDocTemplate(str(d / "report.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                      bottomMargin=2 * cm, title=f"Task {t['n']:02d} - {t['title']}", author="Cemmaly").build(
        st, onFirstPage=footer, onLaterPages=footer)
    # per-task README
    (d / "README.md").write_text(f"""# Task {t['n']:02d} - {t['title']}

Handbook reference: {t['page']} of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

{t['concept'].replace('<b>', '**').replace('</b>', '**')}

## What is in this folder
{chr(10).join('- `' + f + '`' for f in files)}
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
{'python -m unittest discover -v' if t['n'] != 10 else 'python -m unittest discover -s tests -v'}
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
{status}: {ran} (content hash `{rev_hash(d)}`, {date.today().isoformat()})

## Not run / limitations
- Not run: {'; '.join(t['not_run'])}
- Limitations: {'; '.join(t['limits'])}
""")
    print(f"task {t['n']:02d}: {status} {ran}")
    return status


if __name__ == "__main__":
    res = [build(t) for t in TASKS]
    sys.exit(0 if all(r == "PASS" for r in res) else 1)
