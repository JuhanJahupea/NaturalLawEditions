# en_extract.py <pdf> <out>: Burlamaqui, Principles of Natural Law, Nugent's translation, from the Liberty Fund PDF (vol. 1,
# PDF pages 54-283) -> {unit id: {page, text, margin, notes}}. Keeps Burlamaqui's own notes (*) and drops the editor's
# numbered notes and their calls. Restores spaces the PDF leaves out (a gap of more than 0.6 pt between glyphs).
import sys, re, json
import pymupdf as fitz
pdf, out = sys.argv[1:3]
d = fitz.open(pdf)
ROM = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
def unroman(s):
    t = 0
    for i, c in enumerate(s):
        v = ROM[c]; t += -v if i + 1 < len(s) and ROM.get(s[i + 1], 0) > v else v
    return t
def text_of(line, drop_small=True):
    out = ''; prev = None
    for s in line['spans']:
        if drop_small and s['size'] < 8.5 and line['spans'][0]['size'] > 10: continue  # superscript calls
        for ch in s['chars']:
            c = ch['c']
            if prev is not None and c != ' ' and not out.endswith(' ') and ch['bbox'][0] - prev > 0.6: out += ' '
            out += c; prev = ch['bbox'][2]
    return out
units = {}; part = 0; chap = 0; sec = None; cur = None
notes_open = None
def start(uid, page):
    global cur
    cur = units.setdefault(uid, {'page': page, 'text': '', 'margin': [], 'notes': []})
def add(txt):
    if cur['text'].endswith('-') and txt[:1].islower(): cur['text'] = cur['text'][:-1] + txt
    else: cur['text'] += (' ' if cur['text'] else '') + txt
for pi in list(range(30, 32)) + list(range(54, 284)):
    pg = d[pi]; lp = pi - 23
    lines = [l for b in pg.get_text('rawdict')['blocks'] for l in b.get('lines', [])]
    if pi in (30, 31):  # the Author's Advertisement
        if pi == 30: start('AV', lp)
        for l in lines:
            sz = l['spans'][0]['size']; t = text_of(l).strip()
            if 10.8 < sz < 11.6 and t: add(t)
        continue
    marg = []
    mains = [l['bbox'][0] for l in lines if 10.8 < l['spans'][0]['size'] < 11.6 and l['bbox'][1] >= 50]
    left = min(mains) if mains else 54
    for l in lines:
        sz = round(l['spans'][0]['size'], 1); t = text_of(l).strip(); x0, y0 = l['bbox'][0], l['bbox'][1]
        if not t or y0 < 50: continue  # running head and page number
        if sz >= 12.5:
            t2 = t.replace(' ', '').lower()
            m = re.match(r'chapter([ivxl]+)\*?$', t2)
            if m: chap = unroman(m.group(1).upper()); sec = None; continue
            m = re.match(r'u?part(i+)u?$', t2)
            if m: part = len(m.group(1)); chap = 0; sec = None; continue
            continue
        if sz < 9 and (x0 > 360 or x0 < left - 5):  # marginal summary, right or left of the text
            marg.append((y0, t)); continue
        if 9.0 <= sz <= 10.0:  # footnotes
            if re.match(r'^\*', t): notes_open = cur; cur['notes'].append(t.lstrip('* ').strip())
            elif re.match(r'^\d+\. ', t): notes_open = None
            elif notes_open is not None and notes_open['notes']:
                n = notes_open['notes'][-1]; notes_open['notes'][-1] = (n[:-1] + t) if n.endswith('-') else n + ' ' + t
            continue
        if 10.8 < sz < 11.6:
            m = re.match(r'^([IVXL]+)\.\s', t)
            if m and x0 < left + 3 and part and chap:
                n = unroman(m.group(1))
                if sec is None or n in (sec + 1, sec + 2):
                    sec = n; start('P%d.%d.%d' % (part, chap, n), lp); t = t[m.end():]
                    if cur['margin'] and False: pass
            mb = re.search(r'\[([IVXL]+)\.\]\s*', t)  # the editor's bracketed number where Nugent prints none
            if mb and part and chap:
                if mb.start() and cur is not None: add(t[:mb.start()].strip())
                sec = unroman(mb.group(1)); start('P%d.%d.%d' % (part, chap, sec), lp); t = t[mb.end():]
            if part and chap and sec is None:  # a chapter whose first § has no number in Nugent's text
                sec = 0; start('P%d.%d.0' % (part, chap), lp)
            if cur is None: continue
            add(t)
    for y, t in sorted(marg):
        if cur is not None:
            if cur['margin'] and cur['margin'][-1].endswith('-'): cur['margin'][-1] = cur['margin'][-1][:-1] + t
            elif cur['margin'] and not re.search(r'[.!?]$', cur['margin'][-1]): cur['margin'][-1] += ' ' + t
            else: cur['margin'].append(t)
for u in units.values():
    u['text'] = re.sub(r'\s*<\s*\d+\s*>\s*', ' ', u['text']); u['text'] = re.sub(r'\s[*†‡]+(?=\s)', '', re.sub(r'[*†‡]+(?=\S)|(?<=\S)[*†‡]+', '', u['text']))
    u['text'] = re.sub(r'\s+', ' ', u['text']).strip()
json.dump(units, open(out, 'w'), ensure_ascii=False, indent=0)
print(len(units), 'units')
