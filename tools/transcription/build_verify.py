# build_verify.py <screen dir> <outdir> [min confidence]: pairs the screen flagged (diverges or partly) -> verification batches.
# Each item carries the whole source § (cut at 15000 characters) and Barbeyrac's notes to it (cut at 6000).
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
sd, outdir = sys.argv[1:3]; mc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
S = json.load(open(sd + '/sections.json'))
units = {u['id']: u for u in json.load(open('%s/editions/vattel-1773/text.json' % R))['units']}
def cap(t, n): return t if len(t) <= n else t[:n] + ' [...]'
items = []; seen = 0
for f in sorted(glob.glob(sd + '/out/d*.json')):
    for it in json.load(open(f))['items']:
        u = units[it['vattel_id']]
        for pr in it.get('pairs', []):
            seen += 1
            if not pr.get('same_question') or pr.get('relation') not in ('diverges', 'partly'): continue
            if float(pr.get('confidence', 0)) < mc or pr['grotius_id'] not in S['sec']: continue
            items.append({'vattel_sec': u['id'], 'vattel_margin': u.get('margin', ''), 'vattel_text': u['text'],
                          'vattel_notes': ' '.join('%s %s' % (n['mark'], n['text']) for n in u.get('notes', [])),
                          'grotius_ref': pr['grotius_id'], 'grotius_text': cap(S['sec'][pr['grotius_id']], 15000),
                          'barbeyrac_notes': cap(' '.join(S['notes'].get(pr['grotius_id'], [])), 6000),
                          'screen': {'question': it.get('question', ''), **{k: pr.get(k, '') for k in
                                     ('relation', 'grotius_answer', 'vattel_answer', 'grotius_passage', 'vattel_passage')}}})
os.makedirs(outdir + '/in', exist_ok=True); os.makedirs(outdir + '/out', exist_ok=True)
BS = 8
for b in range(0, len(items), BS):
    json.dump(items[b:b + BS], open('%s/in/v%03d.json' % (outdir, b // BS), 'w'), ensure_ascii=False)
print(seen, 'pairs screened;', len(items), 'flagged;', (len(items) + BS - 1) // BS, 'batches')
