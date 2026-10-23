# build_judge.py <edition> <WORK> <candidates.json> <outdir> [batch size]: judge batches of consecutive units with their pages.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
B = WORK
R = ROOT
ed, work, cf, outdir = sys.argv[1:5]; size = int(sys.argv[5]) if len(sys.argv) > 5 else 10
EDN = {'vattel-1773': 'Vattel, Le droit des gens (Neuchâtel 1773)', 'burlamaqui-1747': 'Burlamaqui, Principes du droit naturel (Genève 1747)'}
SRC = {'GRO24': 'Grotius, Le droit de la guerre et de la paix, trad. Barbeyrac (Amsterdam 1724)',
       'PUF34': 'Pufendorf, Le droit de la nature et des gens, trad. Barbeyrac (Amsterdam 1734)'}
AUTH = {'GRO24': 'Grotius', 'PUF34': 'Pufendorf'}
units = [u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units'] if u['kind'] != 'heading']
P = {p['id']: p for p in json.load(open('%s/corpus/%s.json' % (B, work)))['pages']}
cand = json.load(open(cf))['cand']

def parts(p):
    out = []
    for a, b, loc in p['spans']: out.append({'part': 'text', 'locus': loc, 'text': p['text'][a:b].strip()})
    for m in p['margin']: out.append({'part': 'margin', 'locus': m['locus'], 'text': m['text']})
    for n in p['notes']:
        out.append({'part': 'note', 'by': AUTH[work] if n['by'] == 'author' else 'Barbeyrac', 'locus': n['locus'], 'text': n['text']})
    for k, x in enumerate(out): x['k'] = k
    return [dict(k=x.pop('k'), **x) for x in out]

os.makedirs(outdir + '/in', exist_ok=True); os.makedirs(outdir + '/out', exist_ok=True)
order = [u for u in units if cand.get(u['id'])]
nb = 0; chars = []
i = 0
while i < len(order):
    chunk = []; pages = []
    while i < len(order) and len(chunk) < size:
        u = order[i]; new = [p for p in cand[u['id']] if p not in pages]
        if chunk and len(pages) + len(new) > 30: break
        chunk.append(u); pages += new; i += 1
    js = {'edition': EDN[ed], 'source': SRC[work],
          'pages': {p: {'printed': P[p]['page'], 'parts': parts(P[p])} for p in pages},
          'items': [{'unit': u['id'], 'margin': u.get('margin', ''), 'text': u['text'],
                     'notes': [{'mark': n['mark'], 'text': n['text']} for n in u.get('notes', [])], 'candidates': cand[u['id']]} for u in chunk]}
    s = json.dumps(js, ensure_ascii=False); chars.append(len(s))
    open('%s/in/b%03d.json' % (outdir, nb), 'w').write(s); nb += 1
print(len(order), 'units,', nb, 'batches; chars per batch mean', sum(chars) // nb, 'max', max(chars))
