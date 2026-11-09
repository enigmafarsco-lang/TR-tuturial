"""Validate local assets, fragment links and SVG XML; no external requests."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragments = []
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate id: {attrs['id']}"
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.fragments.append(attrs['href'][1:])
        if tag in ('img', 'script') and 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'img':
            assert attrs.get('alt'), 'Image needs alternative text'

page = Document()
page.feed((ROOT / 'index.html').read_text())
assert set(page.fragments) <= page.ids, 'Broken section link'
for asset in page.assets:
    assert (ROOT / asset).is_file(), f'Missing asset: {asset}'
for asset in (ROOT / 'assets').glob('*.svg'):
    ET.parse(asset)
assert len(list((ROOT / 'assets').glob('*.svg'))) == 3
print('Document: IDs, section links, local assets, alt text and 3 SVGs passed.')
