# src_pages.py <out dir>: reading-form pages of the sources for the additions and recall readers.
# JG.json, INST.json, PPU1.json, TN1.json and LOG40.json (Wolff): {id 'JG.pdf<scan>', scan, page, paras: [§ numbers on the page], text, starts: [[offset, §]]}
# with long s as s, line-end hyphens joined, tags dropped; § of an offset = the last start before it (or the page's carried §).
# GRO24, PUF34, DEV56: the corpus files (corpus.py) are used as they are.
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
out = sys.argv[1]
def reading(s):
    s = s.replace('ſ', 's').replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'Ae'); s = re.sub(r'</?[a-z]+>', '', s)
    s = re.sub(r'(\w)[-¬]\n\s*(\w)', r'\1\2', s); s = re.sub(r'\s*\n\s*', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()
for vol, path in (('JG', 'texts/wolff-jus-gentium-1749/JG.json'), ('INST', 'texts/wolff-institutiones-1750/INST.json'), ('PPU1', 'texts/wolff-philosophia-practica-1738/PPU1.json'),
                  ('TN1', 'texts/wolff-theologia-naturalis-1739/TN1.json'), ('LOG40', 'texts/wolff-discursus-praeliminaris-1740/LOG40.json')):
    d = json.load(open(os.path.join(R, path))); pages = []; cur = None; index = {}
    for p in d['pages']:
        body = p.get('body', '') or ''
        parts = re.split(r'<<§ ?(\d+)>>', body)
        text = reading(parts[0]); starts = []
        carried = cur
        for i in range(1, len(parts), 2):
            n = int(parts[i]); seg = reading(parts[i + 1])
            if text: text += ' '
            starts.append([len(text), n]); text += seg; cur = n
            index.setdefault(n, '%s.pdf%d' % (vol, p['scan']))
        pid = '%s.pdf%d' % (vol, p['scan'])
        pages.append({'id': pid, 'scan': p['scan'], 'page': p.get('page', ''), 'carried': carried, 'starts': starts,
                      'margin': [reading(m['para'] + ' ' + m['text']) for m in p.get('margin', [])], 'text': text})
    json.dump({'text': vol, 'pages': pages, 'first_page_of': {str(k): v for k, v in index.items()}}, open(os.path.join(out, vol + '.json'), 'w'), ensure_ascii=False)
    print(vol, len(pages), 'pages', len(index), '§')
