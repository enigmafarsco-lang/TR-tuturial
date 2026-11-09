"""Validate the canonical illustrated Markdown and its actual PDF companion.
Run with the research environment: .venv/bin/python tests/check_book.py
"""
from pathlib import Path
import hashlib
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
text = (DOCS / 'TRADING_AI_GUIDE_FA.md').read_text()
assert len(re.findall(r'^<!-- PAGE \d+ -->', text, re.M)) == 52
assert len(re.findall(r'^## درس ', text, re.M)) == 52
images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
assert len(images) == 52 and len(set(images)) == 52
for image in images:
    assert (DOCS / image).is_file(), image
manifest = json.loads((DOCS / 'images/manifest.json').read_text())
assert len(manifest) == 52
shots = [x for x in manifest if x['kind'] == 'real_software_screenshot']
assert len(shots) == 8
assert len({hashlib.sha256((DOCS / x['path']).read_bytes()).hexdigest() for x in shots}) == 8
layout = json.loads((DOCS / 'layout-check.json').read_text())
assert len(layout) == 52
assert all(x['scroll'] <= x['height'] + 1 and x['contentBottom'] < x['footerTop'] - 4 for x in layout)
pdf = PdfReader(DOCS / 'TRADING_AI_GUIDE_FA.pdf')
assert len(pdf.pages) == 52, len(pdf.pages)
assert all(len(p.extract_text() or '') > 650 for p in pdf.pages), 'Empty or content-light PDF page'
assert all(abs(float(p.mediabox.width) - 595.28) < 2 for p in pdf.pages), 'Not A4'
print('Book: 52 lessons, 52 embedded local images, 8 distinct real software screenshots,')
print('52 A4 PDF pages with text, and no HTML page overflow. All checks passed.')
