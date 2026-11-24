# qc_def41.py [--pages]: checks of the DEF41 transcription (Vattel, Défense du système leibnitien, 1741).
# Reads <WORK>/tr/DEF41/s<NNNN>.json for the scans in editions/vattel-defense-1741/provenance/witness.json and reports:
#  - missing page files;
#  - the paragraph markers <<§ n>> out of sequence (gaps, repeats), and the order of <<PARTIE>>, <<CHAP>>, <<SECTION>>;
#  - printed page numbers that differ from the scan map;
#  - catchwords that do not begin the next page;
#  - pages whose words agree poorly with Google's OCR of the same scan (the PDF's text layer): the share of OCR words
#    of six letters or more (long s and f folded, accents dropped) found in the transcription, and the reverse.
# Writes <WORK>/tr/DEF41_qc.json. With --pages, prints one line per page with the two shares.
import os, re, sys, json, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
import pymupdf as fitz
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = json.load(open(os.path.join(ROOT, 'editions/vattel-defense-1741/provenance/witness.json')))
front = [(f['label'], f['scan']) for f in W['scan_map']['front']]
text = sorted(((int(p), s) for p, s in W['scan_map']['text'].items()), key=lambda x: x[1])
order = [(lab, s) for lab, s in front] + [(str(p), s) for p, s in text]
TR = os.path.join(WORK, 'tr', 'DEF41')
pdf = fitz.open(os.path.join(WORK, 'scans', 'pdf', 'DEF41.pdf'))
def fold(s):
    s = unicodedata.normalize('NFD', s.replace('ſ', 's').lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.replace('f', 's')
def words(s, n=6): return [w for w in re.findall(r'[a-z]+', fold(re.sub(r'<[^>]+>', '', s))) if len(w) >= n]
def first_word(body):
    for line in body.split('\n'):
        line = re.sub(r'<<[^>]*>>', '', re.sub(r'<[^>]+>', '', line)).strip()
        if line: return line.split()[0]
    return ''
rep = {'missing': [], 'markers': [], 'structure': [], 'page': [], 'catch': [], 'ocr': []}
pages = []; lastpar = None; struct = []
for lab, s in order:
    f = os.path.join(TR, 's%04d.json' % s)
    if not os.path.exists(f): rep['missing'].append(s); pages.append(None); continue
    d = json.load(open(f))
    d['notes'] = [n if isinstance(n, dict) else {'mark': n[0], 'text': n[1] if len(n) > 1 else ''} for n in d.get('notes', [])]
    pages.append(d)
    for m in re.finditer(r'<<\s*(PARTIE|CHAP|SECTION|§|DEDICACE|PREFACE)\s*(\d*)\s*>>', d.get('body', '')):
        k, n = m.group(1), m.group(2)
        if k == '§':
            n = int(n)
            if lastpar is not None and n != lastpar + 1: rep['markers'].append({'scan': s, 'after': lastpar, 'got': n})
            lastpar = n
        else: struct.append((s, k, n))
    if lab.isdigit() and d.get('page', '') not in ('', lab): rep['page'].append({'scan': s, 'expected': lab, 'got': d.get('page')})
    ocr = pdf[s - 1].get_text()
    a, b = words(ocr), set(words(d.get('body', '') + ' ' + ' '.join(n.get('text', '') for n in d.get('notes', []))))
    ob = set(a)
    sh1 = sum(1 for w in a if w in b) / len(a) if a else 1.0
    sh2 = len(b & ob) / len(b) if b else 1.0
    if a and (sh1 < 0.8 or sh2 < 0.8): rep['ocr'].append({'scan': s, 'ocr_in_tr': round(sh1, 2), 'tr_in_ocr': round(sh2, 2)})
    if '--pages' in sys.argv: print(s, lab, round(sh1, 2), round(sh2, 2))
for i in range(len(order) - 1):
    a, b = pages[i], pages[i + 1]
    if not a or not b or not a.get('catch'): continue
    c, w = fold(re.sub(r'<[^>]+>', '', a['catch'])).strip('-'), fold(first_word(b.get('body', '')))
    c = re.sub(r'[^a-z]', '', c); w = re.sub(r'[^a-z]', '', w)
    if c and w and not (w.startswith(c[:4]) or c.startswith(w[:4])): rep['catch'].append({'scan': order[i][1], 'catch': a['catch'], 'next': first_word(b.get('body', ''))})
rep['structure'] = [{'scan': s, 'marker': k, 'n': n} for s, k, n in struct]
json.dump(rep, open(os.path.join(WORK, 'tr', 'DEF41_qc.json'), 'w'), ensure_ascii=False, indent=1)
print('pages', len(order), '| missing', len(rep['missing']), '| marker breaks', len(rep['markers']), '| page numbers off', len(rep['page']),
      '| catchwords off', len(rep['catch']), '| low OCR agreement', len(rep['ocr']), '| last §', lastpar)
