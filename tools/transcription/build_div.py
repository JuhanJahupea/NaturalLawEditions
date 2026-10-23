# build_div.py <WORK> <rows.json> <candidates.json> <outdir>: divergence screen batches for Vattel against a source's sections.
# Pairs: the source §§ of the Vattel § 's reuse rows (status match, not commonplace; text and the author's notes),
# plus the best source § by retrieval among the Vattel § 's candidate pages. Up to 4 per Vattel §. Source §§ longer than
# 9000 characters are cut there.
import sys, os, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from lex import toks
B = WORK
R = ROOT
work, rf, cf, outdir = sys.argv[1:5]
pages = json.load(open('%s/corpus/%s.json' % (B, work)))['pages']
units = {u['id']: u for u in json.load(open('%s/editions/vattel-1773/text.json' % R))['units']}
order = list(units)
# source sections: main text by locus (across pages), Barbeyrac's notes by the § they belong to
SEC = collections.OrderedDict(); NOTES = collections.defaultdict(list); PAGES = collections.defaultdict(list)
for p in pages:
    for a, b, loc in p['spans']:
        if '§' not in loc: continue
        SEC.setdefault(loc, []).append(p['text'][a:b].strip())
        if p['id'] not in PAGES[loc]: PAGES[loc].append(p['id'])
    for n in p['notes']:
        base = n['locus'].split(', n.')[0]
        if '§' in base: NOTES[base].append('%s %s' % (n['mark'], n['text']))
SEC = {k: ' '.join(v) for k, v in SEC.items()}
CAP = 9000
def cap(t): return t if len(t) <= CAP else t[:CAP] + ' [...]'
rows = json.load(open(rf))['rows']; cand = json.load(open(cf))['cand']
pairs = collections.defaultdict(list); labels = collections.defaultdict(list)
for r in rows:
    if r['status'] != 'match' or r['label'] == 'commonplace': continue
    base = r['locus'].split(', n.')[0]
    if base not in SEC: continue
    if base not in pairs[r['unit']]: pairs[r['unit']].append(base)
    labels[(r['unit'], base)].append(r['label'])
def overlap(a, b):
    A, Bt = set(toks(a)), set(toks(b))
    return len(A & Bt) / (len(A | Bt) or 1)
items = []
for uid in order:
    if uid not in pairs: continue
    u = units[uid]; full = ' '.join([u.get('margin', ''), u['text']])
    c = list(pairs[uid])
    # one more: the § on the unit's candidate pages with the largest word overlap
    pool = [loc for loc, pg in PAGES.items() if any(p in cand.get(uid, []) for p in pg) and loc not in c]
    if pool: c.append(max(pool, key=lambda l: overlap(full, SEC[l])))
    c = c[:4]
    items.append({'vattel_id': uid, 'vattel_margin': u.get('margin', ''), 'vattel_text': u['text'],
                  'vattel_notes': ' '.join('%s %s' % (n['mark'], n['text']) for n in u.get('notes', [])),
                  'candidates': [{'grotius_id': l, 'text': cap(SEC[l]), 'reuse': labels.get((uid, l), [])} for l in c]})
os.makedirs(outdir + '/in', exist_ok=True); os.makedirs(outdir + '/out', exist_ok=True)
json.dump({'sec': SEC, 'notes': NOTES, 'pages': PAGES}, open(outdir + '/sections.json', 'w'), ensure_ascii=False)
BS = 10
for b in range(0, len(items), BS):
    json.dump(items[b:b + BS], open('%s/in/d%03d.json' % (outdir, b // BS), 'w'), ensure_ascii=False)
print(len(items), 'Vattel §§;', (len(items) + BS - 1) // BS, 'batches;', sum(len(i['candidates']) for i in items), 'pairs')
