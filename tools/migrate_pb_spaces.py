# Restore the space at page breaks in a working edition's data.json, once (2026-11-20).
# Usage: python tools/migrate_pb_spaces.py <data.json> <edition id> '<template in data.json>'
# The working editions of Vattel 1773 and Burlamaqui 1747 dropped the space between the two words around a page break
# ("de<pb>régler"), so text.json read "derégler". This rewrites each break with the edition's template (edition.json
# viewer.pageBreak) after a restored space (tools/nle.py restore_pb_spaces) and moves the English sentence spans (fs) of
# each section to the new text. Reuse rows are spans in the HTML and move with it. Offsets in the edition's pass files and
# static layers are moved separately (tools/transcription/remap_text.py).
import json, os, sys, difflib
from nle import ROOT, Parse, PageBreak, load, restore_pb_spaces

path, ed, frm = sys.argv[1:4]
MAN = load(os.path.join(ROOT, 'editions', ed, 'edition.json')); to = MAN['viewer']['pageBreak']
old_title = next((l.get('otherTitle') for l in MAN['layers'] if l['kind'] == 'variants'), None)
D = load(path)
plain = lambda h, tpl: ''.join(c[0] for c in Parse(h, PageBreak(tpl), old_title).chars)
before = {s['id']: plain(s['html'], frm) for s in D['sections']}
n = restore_pb_spaces(D['sections'], frm, to)
moved = 0
for s in D['sections']:
    if not s.get('fs'): continue
    a, b = before[s['id']], plain(s['html'], to)
    if a == b: continue
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    def m(x, end):
        for tag, i1, i2, j1, j2 in ops:
            if tag == 'equal' and ((i1 < x <= i2) if end else (i1 <= x < i2)): return j1 + x - i1
        for tag, i1, i2, j1, j2 in ops:
            if i1 <= x <= i2: return j2 if end else j1
    s['fs'] = [[m(x, False), m(y, True)] for x, y in s['fs']]; moved += 1
with open(path, 'w', encoding='utf-8') as f: json.dump(D, f, ensure_ascii=False, separators=(',', ':'))
print('spaces restored', n, 'sections with English spans moved', moved)
