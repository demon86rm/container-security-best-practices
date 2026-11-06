#!/usr/bin/env python3
"""Build the A4 checklist handout from the Step 7 table.

Usage: python3 handout/build.py   (writes handout/checklist.html and checklist.pdf)
Needs Google Chrome for the PDF step; the HTML is written either way.
"""
import html, pathlib, re, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "documentation/modules/ROOT/pages/07-checklist.adoc").read_text()

# The checklist table is the first one under "== The Checklist".
body = src.split("== The Checklist", 1)[1].split("|===", 2)[1]
lines = [c[2:].strip() for c in body.splitlines() if c.startswith("| ")]
header = [h.strip() for h in lines[0].split(" | ")]  # the header row is on one line
cells = lines[1:]
rows = [cells[i:i + 3] for i in range(0, len(cells), 3)]
assert header[0] == "Practice" and all(len(r) == 3 for r in rows), "unexpected table shape"


def inline(text):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text, quote=False))


tr = "\n".join(
    f"<tr><td class=box><span></span></td><td>{inline(p)}</td><td>{inline(w)}</td><td>{inline(d)}</td></tr>"
    for p, w, d in rows
)

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Container security checklist</title>
<style>
@page {{ size: A4; margin: 14mm 14mm 12mm; }}
* {{ box-sizing: border-box; }}
body {{ font: 9.2pt/1.35 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1f2933; margin: 0; }}
header {{ border-top: 5px solid #0b5cab; padding-top: 6px; margin-bottom: 8px; }}
h1 {{ font-size: 17pt; margin: 0; color: #0b3d6e; }}
.sub {{ color: #52606d; margin: 2px 0 0; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 6px; }}
th {{ background: #0b3d6e; color: #fff; text-align: left; padding: 4px 6px; font-size: 8.5pt; }}
td {{ padding: 4px 6px; border-bottom: 1px solid #d9e2ec; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f5f8fb; }}
td.box {{ width: 7mm; text-align: center; }}
td.box span {{ display: inline-block; width: 3.4mm; height: 3.4mm; border: 1.2px solid #0b3d6e; margin-top: 1px; }}
th:nth-child(1) {{ width: 7mm; }} th:nth-child(3) {{ width: 36mm; }} th:nth-child(4) {{ width: 38mm; }}
code {{ font: 8.2pt Menlo, monospace; background: #e4ecf4; padding: 0 2px; border-radius: 2px; }}
h2 {{ font-size: 10.5pt; color: #0b3d6e; margin: 10px 0 3px; }}
ul {{ margin: 0; padding-left: 16px; }}
.note {{ font-size: 8pt; color: #52606d; border-top: 1px solid #d9e2ec; margin-top: 8px; padding-top: 5px; }}
</style></head><body>
<header><h1>Container security checklist for developers on OpenShift</h1>
<p class=sub>Score your team: tick what is true today. Each row is a practice from the workshop, with the DORA article it supports.</p></header>
<table><thead><tr><th></th><th>{html.escape(header[0])}</th><th>{html.escape(header[1])}</th><th>{html.escape(header[2])}</th></tr></thead>
<tbody>
{tr}
</tbody></table>
<h2>Three things to do on Monday</h2>
<ul>
<li>Add the Step 4 gate to one pipeline as a report-only job for two weeks, then turn on enforcement.</li>
<li>Ask the platform team which NetworkPolicy and vault integration already exist for your projects.</li>
<li>Ask about image signature verification on the registry.</li>
</ul>
<p class=note>Developer-side working mapping to the Digital Operational Resilience Act (Regulation (EU) 2022/2554, applicable since 17 January 2025). Not legal advice and not a compliance assessment: verify each row against the Regulation text (eur-lex.europa.eu/eli/reg/2022/2554/oj), Delegated Regulation (EU) 2024/1774 and your supervisor's guidance. Full course: demon86rm.github.io/container-security-best-practices</p>
</body></html>
"""

out = root / "handout"
(out / "checklist.html").write_text(page)

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if pathlib.Path(chrome).exists():
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out / 'checklist.pdf'}", (out / "checklist.html").as_uri()],
                   check=True, stderr=subprocess.DEVNULL)
    print("wrote", out / "checklist.pdf")
else:
    sys.exit("Chrome not found: open handout/checklist.html and print to PDF (A4)")
