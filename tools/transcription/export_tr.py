# export_tr.py <text id> <SIGLUM>...: copy the page transcriptions into the repository, one file per volume.
# texts/<text id>/<SIGLUM>.json: {"format": "nle-transcription/1", "text", "volume", "scan": {...}, "pages": [...]}
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
B = WORK
R = ROOT
IA = {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2',
      'PUF34T1': 'ledroitdelanatur01pufe', 'PUF34T2': 'ledroitdelanatur02pufe'}
KEYS = ['scan', 'kind', 'page', 'head', 'margin', 'body', 'notes', 'catch', 'catch_notes', 'sig', 'notes_scan']
tid, vols = sys.argv[1], sys.argv[2:]
os.makedirs('%s/texts/%s' % (R, tid), exist_ok=True)
for vol in vols:
    pages = []
    for f in sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol))):
        d = json.load(open(f))
        p = {k: d.get(k, '' if k not in ('margin', 'notes') else []) for k in KEYS}
        p['scan'] = int(d['scan'])
        p['margin'] = [m if isinstance(m, dict) else {'mark': '', 'text': str(m)} for m in p['margin']]
        p['notes'] = [{'mark': n.get('mark', ''), 'sec': n.get('sec', ''), 'by': n.get('by', ''), 'text': n.get('text', '')} for n in p['notes']]
        pages.append(p)
    scans = [p['scan'] for p in pages]
    assert scans == list(range(1, len(scans) + 1)), (vol, 'gap')
    out = {'format': 'nle-transcription/1', 'text': tid, 'volume': vol,
           'scan': {'source': 'archive.org', 'item': IA[vol], 'url': 'https://archive.org/details/' + IA[vol], 'pages': len(pages)},
           'pages': pages}
    with open('%s/texts/%s/%s.json' % (R, tid, vol), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
    print(vol, len(pages), 'pages', sum(1 for p in pages if p['body']), 'with body', sum(len(p['notes']) for p in pages), 'notes')
