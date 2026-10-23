# make_pass.py <edition> <text id> <rows.json> <step label> <text layer> [<date>]: write editions/<ed>/passes/<text id>.json.
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
ed, tid, rf, step, layer = sys.argv[1:6]; date = sys.argv[6] if len(sys.argv) > 6 else '2026-10-22'
rows = json.load(open(rf))['rows']
P = {'format': 'nle-pass/1', 'edition': ed, 'text': tid, 'date': date, 'textLayer': layer,
     'table': {'pass': 'editions/%s/passes/%s.json' % (ed, tid), 'steps': {'T': step},
               'description': 'Reuse of the source in the edition, found by retrieval on a vision transcription of the source and judged by a language model. '
                              'status match: confidence >= 0.5; possible: 0.3-0.5. Source passages are quoted from the transcription (long s as s, '
                              'line-end hyphens joined). Rows of the earlier OCR pass are in editions/%s/provenance/superseded/.' % ed,
               'sourceLabel': 'source (transcription)'},
     'rows': rows}
os.makedirs('%s/editions/%s/passes' % (R, ed), exist_ok=True)
with open('%s/editions/%s/passes/%s.json' % (R, ed, tid), 'w', encoding='utf-8') as f:
    json.dump(P, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
print(ed, tid, len(rows), 'rows')
