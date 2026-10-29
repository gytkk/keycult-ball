# /// script
# requires-python = ">=3.11"
# dependencies = ["shapely==2.1.2", "pymupdf==1.26.7"]
# ///
"""Check independent geometry, artifacts and PDF scale. Not manufacturing DRC."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import ast
import itertools
import json
import math
import re
import xml.etree.ElementTree as ET
import pymupdf
from shapely.geometry import box

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design/preliminary'


def read_json(name):
    return json.loads((DESIGN / name).read_text())


def close(actual, expected, label):
    assert math.isclose(actual, expected, abs_tol=1e-6), (label, actual, expected)


def check_local_link(path, target):
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or not parts.path or target.startswith('/'):
        return
    linked = (path.parent / unquote(parts.path)).resolve()
    assert linked.is_relative_to(ROOT), (path, target)
    assert linked.exists(), f'Broken local link: {path.relative_to(ROOT)} -> {target}'


class LinkParser(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('src', 'href') and value:
                check_local_link(self.path, value)


for path in ROOT.rglob('*'):
    if not path.is_file() or any(p in {'.git', '.venv', '.cache', '__pycache__', 'upstream', 'local'} for p in path.parts):
        continue
    if path.suffix == '.json': json.loads(path.read_text())
    elif path.suffix == '.svg': ET.fromstring(path.read_text())
    elif path.suffix == '.html': LinkParser(path).feed(path.read_text())
    elif path.suffix == '.py': ast.parse(path.read_text())
    elif path.suffix == '.md':
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            check_local_link(path, link)

layout = read_json('layout.json')
report = read_json('validation.json')
plate_width, plate_height, _ = layout['official_plate_envelope_mm']
polygon = box(-plate_width/2, -plate_height/2, plate_width/2, plate_height/2)
assert layout['plate_visualization'].startswith('generic rectangular bounding envelope')
containment = {}
for name, key_count, gap in [('preferred', 66, 3), ('alternative', 64, 2)]:
    data = layout[name]
    keys = data['keys']
    assert len(keys) == key_count == data['key_count']
    assert len({(k['x_mm'], k['y_mm']) for k in keys}) == key_count
    values = report['layouts'][data['name']]
    for i, k in enumerate(keys):
        close(k['x_mm'], (k['column'] - (11 + gap) / 2) * 19.05, 'x pitch')
        close(k['y_mm'], (k['row'] - 2) * 19.05, 'y pitch')
    assert {k['label'] for k in keys} >= set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    close(sum(k['x_mm'] for k in keys), 0, 'centering')
    for first, second in itertools.combinations(keys, 2):
        assert abs(first['x_mm'] - second['x_mm']) >= 18 or abs(first['y_mm'] - second['y_mm']) >= 18
    ball_gap = min(math.hypot(max(abs(k['x_mm']) - 9, 0), max(abs(k['y_mm']) - 9, 0)) - 17 for k in keys)
    keep_gap = min(max(abs(k['x_mm']) - 34, abs(k['y_mm']) - 34) for k in keys)
    close(ball_gap, values['ball_to_keycap_min_mm'], 'ball gap')
    close(keep_gap, values['50mm_square_to_keycap_min_signed_mm'], 'keepout gap')
    assert ball_gap > 0
    assert (keep_gap > 0) if name == 'preferred' else (keep_gap < 0)
    containment[name] = {}
    for proxy, half in [('switch_proxy', 7), ('keycap_assumption', 9)]:
        boxes = [(k['id'], box(k['x_mm']-half, k['y_mm']-half, k['x_mm']+half, k['y_mm']+half)) for k in keys]
        outside = [key for key, rectangle in boxes if not polygon.covers(rectangle)]
        assert not outside, (name, proxy, outside)
        containment[name][proxy] = {
            'outside_rectangular_reference': outside,
            'min_clearance_to_rectangular_reference_mm': round(min(rectangle.distance(polygon.boundary) for _, rectangle in boxes), 6),
        }
(DESIGN / 'envelope-containment.json').write_text(json.dumps({
    'scope': 'Generic rectangular bounding envelope ONLY; does not prove official contour or case opening fit.',
    'layouts': containment,
}, indent=2) + '\n')
# Public drawings must not silently reintroduce the copied plate contour.
for name in ('layout.svg', 'alternative.svg', 'print-1to1.svg'):
    root = ET.fromstring((DESIGN / name).read_text())
    reference = root.find('.//*[@id="plate-envelope"]')
    assert reference is not None and reference.tag.endswith('rect'), name
    assert float(reference.attrib['width']) == plate_width
    assert float(reference.attrib['height']) == plate_height
    assert all(element.attrib.get('fill', 'none') == 'none'
               for element in root.iter('{http://www.w3.org/2000/svg}path')), name
assert layout['case_opening_mm'] is None and layout['plate_to_floor_mm'] is None
assert layout['trackball']['holder_verified_envelope_mm'] is None
assert layout['trackball']['ball_center_height_above_plate_mm'] is None

with pymupdf.open(DESIGN / 'print-1to1.pdf') as pdf:
    assert len(pdf) == 1
    page = pdf[0]
    width, height = page.rect.width * 25.4 / 72, page.rect.height * 25.4 / 72
    assert abs(width - 420) < 1 and abs(height - 297) < 1, (width, height)
    calibration = []
    for drawing in page.get_drawings():
        for item in drawing['items']:
            if item[0] == 'l':
                start, end = item[1:3]
                length = abs(end.x - start.x) * 25.4 / 72
                if abs(end.y - start.y) < .001 and abs(length - 100) < .05:
                    calibration.append(length)
    assert calibration, 'No 100mm calibration segment in PDF'
    measured = {'page_count': 1, 'page_size_mm': [width, height], 'calibration_horizontal_line_lengths_mm': calibration,
                'print_driver_scaling': 'user must still print actual size/100%, no fit-to-page'}
    (DESIGN / 'print-validation.json').write_text(json.dumps(measured, indent=2) + '\n')

print('PASS: Python/JSON/SVG/HTML/link syntax; 66/64 keys, pitch and centers; cap/ball/reservation checks; generic rectangular envelope; A3 PDF scale.')
print(f'PDF calibration: {calibration[0]:.6f} mm. Case opening and full 3D assembly remain unverified.')
