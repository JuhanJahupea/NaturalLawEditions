# export_def41.py: the DEF41 page transcriptions into texts/vattel-defense-1741/DEF41.json (format nle-transcription/1),
# in the order of the scan map in editions/vattel-defense-1741/provenance/witness.json, with the second readers'
# corrections (<WORK>/tr/DEF41_check/*.json) under "checked" and the wanting pages under "lacunae".
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
W = json.load(open(os.path.join(ROOT, 'editions/vattel-defense-1741/provenance/witness.json')))
sm = W['scan_map']
order = [f['scan'] for f in sm['front']] + [s for s in sm['text'].values() if s] + [i['scan'] for i in sm.get('inserted', [])]
order = sorted(set(order))
KEYS = ['scan', 'kind', 'page', 'head', 'body', 'notes', 'catch', 'catch_notes', 'sig', 'notes_scan']
pages = []
for s in order:
    d = json.load(open(os.path.join(WORK, 'tr', 'DEF41', 's%04d.json' % s)))
    p = {k: d.get(k, [] if k == 'notes' else '') for k in KEYS}
    p['scan'] = s
    p['notes'] = [n if isinstance(n, dict) else {'mark': n[0], 'text': n[1] if len(n) > 1 else ''} for n in p['notes']]
    p['notes'] = [{'mark': n.get('mark', ''), 'text': n.get('text', '')} for n in p['notes']]
    pages.append(p)
checked = []
for f in sorted(glob.glob(os.path.join(WORK, 'tr', 'DEF41_check', '*.json'))):
    b = json.load(open(f))
    for pg in b['pages']:
        checked.append({'batch': b['batch'], 'scan': pg['scan'], 'words': pg.get('words'), 'changes': pg.get('changes', [])})
out = {'format': 'nle-transcription/1', 'text': 'vattel-defense-1741', 'volume': 'DEF41',
       'scan': {'source': "Google Books PDF of the BCU Lausanne copy, supplied by the editor (708 scans); the scan numbers are its PDF pages",
                'google_id': W['base_scan'].get('google_id', ''), 'second_scan': 'https://archive.org/details/dfensedusystmel00luzagoog',
                'pages': len(pages)},
       'lacunae': W.get('lacunae', []), 'checked': checked, 'pages': pages}
os.makedirs(os.path.join(ROOT, 'texts', 'vattel-defense-1741'), exist_ok=True)
with open(os.path.join(ROOT, 'texts', 'vattel-defense-1741', 'DEF41.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
print(len(pages), 'pages;', sum(len(p['notes']) for p in pages), 'notes;', len(checked), 'pages checked,',
      sum(len(c['changes']) for c in checked), 'corrections')
