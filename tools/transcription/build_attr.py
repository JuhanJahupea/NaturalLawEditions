# build_attr.py <candidates> <dir> [rows per batch]: attribution batches (ATTR_PROMPT.md). Rows are grouped by unit; each unit
# goes with its margin, main text and notes. keys.json ties each key to the row's edition, table, unit, page and passages.
import sys, os, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
cf, d = sys.argv[1:3]; BS = int(sys.argv[3]) if len(sys.argv) > 3 else 30
C = json.load(open(cf))
def strip(h): return re.sub(r'<[^>]+>', '', h)
CAT = json.load(open(R + '/catalogue.json')); TX = {t['id']: t for t in CAT['texts']}
for e in CAT['editions']: TX.setdefault(e['id'], {'author': e['author'], 'title': e['title'], 'date': e['date']})
units, tables = {}, {}
for ed in {c['ed'] for c in C}:
    units[ed] = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
groups = collections.OrderedDict(); keys = {}
for k, c in enumerate(C):
    tf = '%s/reuse/%s__%s.json' % (R, c['ed'], c['to'])
    if tf not in tables: tables[tf] = {r['id']: r for r in json.load(open(tf))['rows']}
    r = tables[tf][c['id']]; t = TX[c['to']]
    part = r['at'][0][0] if r.get('at') else ('m' if r.get('where') == 'margin' else 't')
    by = "Barbeyrac's note" if r['family'] == 'Bb' else (t['author'].split(' ')[-1] if r['family'] != 'Lz' else 'Leibniz')
    groups.setdefault((c['ed'], c['unit']), []).append({'key': k, 'source': '%s, %s (%s)' % (t['author'], t['title'], t.get('date', '')),
        'by': by, 'label': r['label'], 'part': part, 'passage': r['passage'], 'source_passage': r['source']})
    keys[k] = {'ed': c['ed'], 'to': c['to'], 'id': r['id'], 'unit': r['unit'], 'page': r['page'], 'passage': r['passage'], 'source': r['source']}
items = []
for (ed, uid), rows in groups.items():
    u = units[ed][uid]
    items.append({'unit': uid, 'margin': u.get('margin', ''), 'text': strip(u['text']),
                  'notes': [{'part': 'n%d' % i, 'mark': n.get('mark', ''), 'text': strip(n['text'])} for i, n in enumerate(u.get('notes', []))],
                  'rows': rows})
os.makedirs(d + '/in', exist_ok=True); os.makedirs(d + '/out', exist_ok=True)
json.dump(keys, open(d + '/keys.json', 'w'), ensure_ascii=False)
b, cur, n = 0, [], 0
for it in items:
    cur.append(it); n += len(it['rows'])
    if n >= BS: json.dump(cur, open('%s/in/a%03d.json' % (d, b), 'w'), ensure_ascii=False); b += 1; cur, n = [], 0
if cur: json.dump(cur, open('%s/in/a%03d.json' % (d, b), 'w'), ensure_ascii=False); b += 1
print(len(C), 'rows;', len(items), 'units;', b, 'batches')
