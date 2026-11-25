# crousaz_ocr.py: Crousaz's Examen de l'Essay de M. Pope (1737) and Commentaire sur la traduction en vers de M. l'abbé
# Du Resnel (1738), page by page from the text layer (Google's OCR) of the Google Books PDFs the editor supplied
# (<WORK>/scans/pdf/EXA37.pdf, COM38.pdf), into texts/crousaz-examen-1737/EXA37.json and
# texts/crousaz-commentaire-1738/COM38.json (format nle-ocr/1).
#  - Printed page from the scan by a fixed offset, checked against the page numbers in the running heads; front
#    matter by scan. The running head (first line) is kept apart as "head"; the rest of the page as OCR'd, line breaks kept.
#  - "part": the division of the book the page belongs to, from the running heads.
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
import pymupdf as fitz
BOOKS = {
    'EXA37': {'text': 'crousaz-examen-1737', 'offset': 22, 'first': 23, 'last': 236,
              'front': {9: ('III', 'Avis du libraire'), 10: ('IV', 'Avis du libraire')}
                       | {s: (r, 'Préface') for s, r in zip(range(11, 23), ['V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI'])},
              'back': {237: ('', 'Fautes principales à corriger')},
              'title': 'Examen de l\'Essay de Monsieur Pope sur l\'homme. Lausanne, Marc-Mich. Bousquet & Comp., et se vend à Amsterdam chez Pierre Mortier, 1737',
              'copy': 'Google Books PDF supplied by the editor (242 scans); stamp of the Bibliothèque cantonale (BCU Lausanne) on scan 8'},
    'COM38': {'text': 'crousaz-commentaire-1738', 'offset': 8, 'first': 9, 'last': 382,
              'front': {7: ('', 'Avis au lecteur'), 8: ('', 'Avis au lecteur')}, 'back': {},
              'title': 'Commentaire sur la traduction en vers de Mr. l\'abbé Du Resnel, de l\'Essai de M. Pope sur l\'homme. Genève, Pellissari & Comp., 1738',
              'copy': 'Google Books PDF supplied by the editor (382 scans); stamp of the Biblioteca Nazionale Vittorio Emanuele, Rome; probably Google Books daRZAAAAcAAJ'},
}
def part_of(sig, head, prev):
    h = re.sub(r'[^A-Z ]', '', head.upper().replace('É', 'E'))
    if sig == 'EXA37': return 'Réflexions sur l\'Essai de M. Pope'
    if 'REPONSE' in h: return 'Réponse de M. de Crousaz'
    m = re.search(r'\b(IV|III|II|I)\s*EPITRE', h)
    if m: return 'Commentaire sur l\'Épître %s' % m.group(1)
    if 'LETTRE' in h or 'CROUSAZ' in h:
        if prev and prev.endswith('Épître IV'): return 'Seconde lettre à M. de Crousaz'
        if prev in (None, 'Lettre à M. de Crousaz'): return 'Lettre à M. de Crousaz'
    return prev or 'Lettre à M. de Crousaz'
for sig, B in BOOKS.items():
    d = fitz.open(os.path.join(WORK, 'scans', 'pdf', sig + '.pdf'))
    pages = []; prev = None; bad = []
    for s in range(1, d.page_count + 1):
        lines = [l.rstrip() for l in d[s - 1].get_text().split('\n')]
        lines = [l for l in lines if l.strip()]
        if B['first'] <= s <= B['last']: page = str(s - B['offset'])
        elif s in B['front']: page = B['front'][s][0]
        elif s in B['back']: page = B['back'][s][0]
        else: continue
        head = lines[0] if lines else ''
        if re.fullmatch(r'[\d\W]{1,6}', head) and len(lines) > 1: head = head + ' ' + lines[1]; lines = lines[1:]
        nums = re.findall(r'\b(\d{1,3})\b', head)
        if B['first'] <= s <= B['last'] and nums and page not in nums and len(lines) > 3: bad.append((s, page, head))
        if s in B['front']: part = B['front'][s][1]
        elif s in B['back']: part = B['back'][s][1]
        else: part = part_of(sig, head, prev); prev = part
        pages.append({'scan': s, 'page': page, 'part': part, 'head': head, 'text': '\n'.join(lines[1:])})
    out = {'format': 'nle-ocr/1', 'text': B['text'], 'volume': sig,
           'source': {'title': B['title'], 'copy': B['copy'], 'layer': 'Google OCR text layer of the PDF',
                      'note': 'scan numbers are the PDF pages; printed page = scan - %d' % B['offset']},
           'pages': pages}
    dd = os.path.join(ROOT, 'texts', B['text']); os.makedirs(dd, exist_ok=True)
    with open(os.path.join(dd, sig + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=0); f.write('\n')
    from collections import Counter
    print(sig, len(pages), 'pages', sum(len(p['text'].split()) for p in pages), 'words;', dict(Counter(p['part'] for p in pages)))
    print('  running heads whose number differs from the offset:', bad[:12], len(bad))
