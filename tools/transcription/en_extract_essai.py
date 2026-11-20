# en_extract_essai.py <pdf> <out>: Vattel, Essay on the Foundation of Natural Law, T. J. Hochstrasser's translation, from the
# Liberty Fund Law of Nations (2008), PDF pages 775-800 (printed 747-772) -> {unit id: {page, text, notes}}, units E.n by the
# roman paragraph numbers. Keeps Vattel's own notes and drops the editor's [[...]] notes and their calls. Restores spaces the PDF
# leaves out (a gap of more than 0.6 pt between glyphs). The epigraph before § I goes to "epigraph".
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
def text_of(line, keep_small=False):
    out = ''; prev = None; calls = []
    for s in line['spans']:
        small = s['size'] < 8.5
        for ch in s['chars']:
            c = ch['c']
            if small and not keep_small:
                calls.append(c); continue
            if prev is not None and c != ' ' and not out.endswith(' ') and ch['bbox'][0] - prev > 0.6: out += ' '
            out += c; prev = ch['bbox'][2]
    return out, ''.join(calls)
units = {}; cur = None; epigraph = []; notes = []
def add(u, txt):
    if u['text'].endswith('-') and txt[:1].islower(): u['text'] = u['text'][:-1] + txt
    else: u['text'] += (' ' if u['text'] else '') + txt
for pi in range(774, 800):
    pg = d[pi]; lp = pi - 27
    lines = [l for b in pg.get_text('rawdict')['blocks'] for l in b.get('lines', [])]
    for l in lines:
        sz = l['spans'][0]['size']; t, calls = text_of(l); t = t.strip()
        if not t: continue
        if 10.8 < sz < 11.6:   # body
            m = re.match(r'^([IVXLC]+)\.\s+(.*)$', t)
            if m and (cur is None or unroman(m.group(1)) == cur['n'] + 1):
                n = unroman(m.group(1)); cur = units.setdefault('E.%d' % n, {'n': n, 'page': lp, 'text': '', 'notes': []}); t = m.group(2)
            if cur is None: epigraph.append(t); continue
            add(cur, t)
            if calls: cur.setdefault('calls', []).append(calls)
        elif 9.0 < sz < 10.0:  # notes
            notes.append((lp, cur['n'] if cur else 0, t))
        # running heads (10.5, small capitals), titles (13.9) and other sizes are left out
# notes: a numbered note starts "n. "; editor's notes are in [[ ]]
merged = []
for lp, n, t in notes:
    if re.match(r'^\d+\.\s', t) or not merged: merged.append([lp, n, t])
    else:
        prev = merged[-1][2]
        merged[-1][2] = prev[:-1] + t if prev.endswith('-') and t[:1].islower() else prev + ' ' + t
for lp, n, t in merged:
    body = re.sub(r'^\d+\.\s*', '', t)
    if body.startswith('[['): continue
    if n: units['E.%d' % n]['notes'].append(body)
res = {k: {'page': v['page'], 'text': re.sub(r'\s+', ' ', v['text']).strip(), 'notes': v['notes']} for k, v in units.items()}
json.dump({'epigraph': ' '.join(epigraph), 'units': res}, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(res), 'units', sorted(int(k[2:]) for k in res)[-3:], 'notes', sum(len(v['notes']) for v in res.values()))
print('epigraph:', ' '.join(epigraph)[:300])
