# build_verify.py <screen dir> <outdir> [min confidence]: pairs the screen flagged (diverges or partly) -> verification batches.
# Each item carries the whole source § (cut at 15000 characters) and Barbeyrac's notes to it (cut at 6000).
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
sd, outdir = sys.argv[1:3]; mc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
S = json.load(open(sd + '/sections.json')); ED = S.get('edition', 'vattel-1773'); K = ED.split('-')[0]
units = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ED)))['units']}
def cap(t, n): return t if len(t) <= n else t[:n] + ' [...]'
items = []; seen = 0
for f in sorted(glob.glob(sd + '/out/d*.json')):
    for it in json.load(open(f))['items']:
        u = units[it[K + '_id']]
        for pr in it.get('pairs', []):
            seen += 1
            if not pr.get('same_question') or pr.get('relation') not in ('diverges', 'partly'): continue
            if float(pr.get('confidence', 0)) < mc or pr['source_id'] not in S['sec']: continue
            items.append({K + '_sec': u['id'], K + '_margin': u.get('margin', ''), K + '_text': u['text'],
                          K + '_notes': ' '.join('%s %s' % (n['mark'], n['text']) for n in u.get('notes', [])),
                          'source_ref': pr['source_id'], 'source_text': cap(S['sec'][pr['source_id']], 15000),
                          'barbeyrac_notes': cap(' '.join(S['notes'].get(pr['source_id'], [])), 6000),
                          'screen': {'question': it.get('question', ''), **{k: pr.get(k, '') for k in
                                     ('relation', 'source_answer', K + '_answer', 'source_passage', K + '_passage')}}})
os.makedirs(outdir + '/in', exist_ok=True); os.makedirs(outdir + '/out', exist_ok=True)
BS = 8
for b in range(0, len(items), BS):
    json.dump(items[b:b + BS], open('%s/in/v%03d.json' % (outdir, b // BS), 'w'), ensure_ascii=False)
print(seen, 'pairs screened;', len(items), 'flagged;', (len(items) + BS - 1) // BS, 'batches')
