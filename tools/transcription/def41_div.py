# def41_div.py <batches dir> <out dir> [units per batch]: screen batches for the divergence layer of Vattel's Défense du
# système leibnitien (1741), step 5: where Vattel departs from Leibniz or Wolff. Items: the units with a reuse row to
# the Théodicée or the Psychologia rationalis (editions/vattel-defense-1741/provenance/reuse/), each with the segments
# those rows name (at most four, the most rows first) and their reuse labels. Disagreements with Crousaz and Roques are in
# the reuse rows already (stance "rejects"). Readers may add a segment from <batches dir>/segments.json.
import sys, os, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
BD, OUT = sys.argv[1], sys.argv[2]; PER = int(sys.argv[3]) if len(sys.argv) > 3 else 12
os.makedirs(OUT, exist_ok=True)
SEG = json.load(open(os.path.join(BD, 'segments.json')))
ITEMS = {}
for f in glob.glob(os.path.join(BD, 'b*.json')):
    for it in json.load(open(f))['items']: ITEMS[it['unit']] = it
R = collections.defaultdict(list)
for t in ('leibniz-theodicee-1734', 'wolff-psychologia-rationalis-1734'):
    for r in json.load(open(os.path.join(ROOT, 'editions', 'vattel-defense-1741', 'provenance', 'reuse', t + '.json')))['rows']:
        R[r['unit']].append(r)
order = [u for u in ITEMS if u in R]
items = []
for u in order:
    it = ITEMS[u]; segs = collections.Counter(r['page'] for r in R[u])
    cands = []
    for s, n in segs.most_common(4):
        cands.append({'key': s, 'locus': SEG[s]['locus'], 'text': SEG[s]['text'][:4000],
                      'reuse': sorted({'%s (%s)' % (r['label'], r.get('stance', '')) for r in R[u] if r['page'] == s})})
    items.append({'vattel_id': u, 'vattel_text': it['text'], 'vattel_notes': it['notes'], 'candidates': cands})
for k in range(0, len(items), PER):
    json.dump({'items': items[k:k + PER]}, open(os.path.join(OUT, 's%02d.json' % (k // PER)), 'w'), ensure_ascii=False, indent=1)
print(len(items), 'units;', sum(len(i['candidates']) for i in items), 'pairs;', (len(items) + PER - 1) // PER, 'batches')
