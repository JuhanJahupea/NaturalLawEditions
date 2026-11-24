# theodicee_text.py <epub> <vol I leaves.json> <vol II leaves.json> <out.json>: Leibniz's Essais de Théodicée by section,
# from the Wikisource text (Œuvres philosophiques de Leibniz, éd. P. Janet, Paris, Alcan, 1900, t. II; exported by
# ws-export as EPUB), each section linked to the leaf of the Amsterdam 1734 edition (Changuion; archive.org
# essaisdethodice01leibgoog = t. I, essaisdethodice00leibgoog = t. II) where it begins.
#  - Sections: Préface by paragraph (Pref.1-37), Discours de la conformité §§ 1-87 (Disc.n), the three parts §§ 1-417
#    (T.n), the Abrégé by objection (Abr.0 = the preamble, Abr.1-8), the Réflexions sur Hobbes §§ 1-12 (Hob.n), the
#    Remarques sur King §§ 1-27 (King.n). Janet's notes, note calls, page numbers and index are left out.
#  - Fixes of the Wikisource numbering: Partie I § 1 and § 5 carry no number there; Discours "63" after 64 is § 65;
#    "445" after 414 is § 415. Numbered items inside a section (King § 11) stay in their section.
#  - Leaves: each section goes on the leaf of the 1734 OCR, inside its part's range and at or after the previous section's,
#    that first holds most of its first fifteen long words (accents folded, long s and f as one letter). A section with fewer
#    than three of them found is placed between its neighbours and marked "approx".
import sys, re, json, html, zipfile
EPUB, V1, V2, OUT = sys.argv[1:5]
z = zipfile.ZipFile(EPUB)
s = z.read([n for n in z.namelist() if 'Texte_entier' in n][0]).decode('utf-8')
s = re.sub(r'<sup[^>]*class="[^"]*reference[^"]*"[^>]*>.*?</sup>', '', s, flags=re.S)
s = re.sub(r'<span[^>]*class="[^"]*pagenum[^"]*"[^>]*>.*?</span>', '', s, flags=re.S)
s = re.sub(r'<(div|ol)[^>]*class="[^"]*references[^"]*"[^>]*>.*?</\1>', '', s, flags=re.S)
def clean(p):
    p = re.sub(r'<(i|em)\b[^>]*>', '<i>', p); p = re.sub(r'</(i|em)>', '</i>', p)
    p = re.sub(r'<(?!/?i>)[^>]+>', '', p)
    return ' '.join(html.unescape(p).replace('﻿', '').split())
parts = []
for x in re.split(r'(<h[23][^>]*>.*?</h[23]>)', s, flags=re.S):
    m = re.match(r'<h([23])[^>]*>(.*?)</h\1>', x, re.S)
    if m: parts.append([clean(m.group(2)), []]); continue
    if parts: parts[-1][1] += [c for c in (clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', x, re.S)) if c]
KEYS = [('PRÉFACE', 'Pref', 'Préface'), ('DISCOURS', 'Disc', 'Discours de la conformité de la foi avec la raison'),
        ('PREMIÈRE PARTIE', 'T', 'Essais, première partie'), ('DEUXIÈME PARTIE', 'T', 'Essais, deuxième partie'),
        ('TROISIÈME PARTIE', 'T', 'Essais, troisième partie'), ('Abrégé', 'Abr', 'Abrégé de la controverse'),
        ('Réflexions', 'Hob', 'Réflexions sur l\'ouvrage de M. Hobbes'), ('Remarques', 'King', 'Remarques sur le livre de l\'Origine du mal')]
FIX = {('T', 'Après avoir réglé'): 1, ('T', 'De sorte que c’est un jugement terrible'): 5}
TYPO = {('Disc', 63, 64): 65, ('T', 445, 414): 415}
ROM = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8}
secs = []
for title, ps in parts:
    k = next((k for k in KEYS if title.startswith(k[0]) or title.upper().startswith(k[0].upper())), None)
    if not k: continue
    pre, part = k[1], k[2]; last = max([x['n'] for x in secs if x['pre'] == pre] or [0])
    cur = None
    for i, p in enumerate(ps):
        n = None
        if pre == 'Pref': n = i + 1
        elif pre == 'Abr':
            m = re.match(r'([IVX]+)\. Object', p)
            n = ROM[m.group(1)] if m else (0 if cur is None else None)
        else:
            m = re.match(r'(\d+)\.\s', p)
            if m:
                v = int(m.group(1)); v = TYPO.get((pre, v, last), v)
                if v == last + 1: n = v
            for (pp, start), v in FIX.items():
                if pp == pre and p.startswith(start) and v == last + 1: n = v
        if n is not None:
            cur = {'pre': pre, 'n': n, 'part': part, 'paras': []}; secs.append(cur); last = n
        if cur is not None: cur['paras'].append(p)
# leaves of the 1734 edition
L1, L2 = json.load(open(V1)), json.load(open(V2))
ITEM = {1: 'essaisdethodice01leibgoog', 2: 'essaisdethodice00leibgoog'}
RANGE = {'Pref': (1, 249, 280), 'Disc': (1, 281, 343), 'T1': (1, 344, 418), 'T23': (2, 12, 272),
         'Abr': (2, 273, 287), 'Hob': (2, 288, 303), 'King': (2, 304, 382)}
import unicodedata
def fold(t):
    t = unicodedata.normalize('NFD', re.sub(r'<[^>]+>', '', t).lower())
    return ''.join(c for c in t if not unicodedata.combining(c)).replace('ſ', 's').replace('s', 'f')
LEAF = {1: [re.sub(r'\s+', '', fold(p['text'])) for p in L1], 2: [re.sub(r'\s+', '', fold(p['text'])) for p in L2]}
def place(group, key, numbered=None):
    # each section on the leaf, at or after the previous section's, that holds most of its first long words
    # (accents folded, long s and f as one letter); with fewer than two found, placed between its neighbours (approx)
    vol, a, b = RANGE[key]; P = LEAF[vol]; prev = a; got = []
    for x in group:
        ws = [w for w in re.findall(r'[a-z]{6,}', fold(' '.join(x['paras'])[:700]))][:15]
        sc = {lf: sum(1 for w in ws if w in P[lf]) for lf in range(prev, min(b, prev + 12) + 1)}
        top = max(sc.values(), default=0)
        bl = min((lf for lf, v in sc.items() if v >= max(2, 0.6 * top)), default=None)
        if bl is not None and top >= 3 and top >= 0.3 * len(ws): prev = bl; got.append((x, bl, False))
        else: got.append((x, None, True))
    for i, (x, lf, ap) in enumerate(got):
        if lf is None:
            lo = next((g[1] for g in reversed(got[:i]) if g[1] is not None), a)
            hi = next((g[1] for g in got[i + 1:] if g[1] is not None), b)
            lf = lo if hi - lo <= 1 else (lo + hi) // 2
        x['scan'] = {'item': ITEM[vol], 'leaf': lf, 'url': 'https://archive.org/details/%s/page/n%d/mode/1up' % (ITEM[vol], lf)}
        if ap: x['scan']['approx'] = True
G = lambda pre, f=lambda x: True: [x for x in secs if x['pre'] == pre and f(x)]
place(G('Pref'), 'Pref', False); place(G('Disc'), 'Disc', True); place(G('T', lambda x: x['n'] <= 106), 'T1', True)
place(G('T', lambda x: x['n'] > 106), 'T23', True); place(G('Abr'), 'Abr', False); place(G('Hob'), 'Hob', True)
place(G('King'), 'King', True)
LAB = {'Pref': 'Préface ¶ %d', 'Disc': 'Discours § %d', 'T': '§ %d', 'Abr': 'Abrégé, objection %d', 'Hob': 'Réflexions sur Hobbes § %d', 'King': 'Remarques sur King § %d'}
out = []
for x in secs:
    lab = 'Abrégé, préambule' if x['pre'] == 'Abr' and x['n'] == 0 else LAB[x['pre']] % x['n']
    out.append({'id': '%s.%d' % (x['pre'], x['n']), 'part': x['part'], 'label': lab, 'text': '\n'.join(x['paras']), 'scan': x['scan']})
doc = {'format': 'nle-sections/1', 'text': 'leibniz-theodicee-1734',
       'source': {'text': 'Wikisource, "Essais de Théodicée" (Œuvres philosophiques de Leibniz, éd. Paul Janet, 2e éd., Paris, Alcan, 1900, t. II), CC BY-SA 4.0: https://fr.wikisource.org/wiki/Essais_de_Th%C3%A9odic%C3%A9e',
                  'scans': 'Essais de théodicée, nouvelle édition augmentée de l\'histoire de la vie & des ouvrages de l\'auteur, par M. L. de Neufville, Amsterdam, François Changuion, 1734, 2 vols: https://archive.org/details/essaisdethodice01leibgoog (t. I), https://archive.org/details/essaisdethodice00leibgoog (t. II)'},
       'sections': out}
json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(x['pre'] for x in secs)
print(len(out), 'sections', dict(c), sum(len(x['text'].split()) for x in out), 'words;',
      sum(1 for x in out if not x['scan'].get('approx')), 'placed by their opening words')
for pre in c:
    ns = [x['n'] for x in secs if x['pre'] == pre]
    miss = sorted(set(range(min(ns), max(ns) + 1)) - set(ns))
    if miss: print('  missing', pre, miss)
