# corpus.py <WORK>: assemble the page transcriptions of a work into pages with loci.
# Output corpus/<WORK>.json: {"work", "pages": [{id, vol, scan, page, kind, sect, text, spans, margin, notes}]}
#   text: reading form of the main text (long s kept as s, hyphens joined, tags dropped);
#   spans: [[start, end, locus]] over text; margin: [{mark, text, locus}]; notes: [{mark, sec, by, text, locus}].
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
B = WORK
ROM = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
def roman(n):
    out = ''
    for v, s in ((100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v: out += s; n -= v
    return out
def unroman(s):
    s = s.upper().replace('J', 'I'); t = 0
    for i, c in enumerate(s):
        v = ROM.get(c, 0); t += -v if i + 1 < len(s) and ROM.get(s[i + 1], 0) > v else v
    return t

# Front matter by scan: (first scan, section name, locus prefix). Body sections follow the markers.
WORKS = {
    'GRO24': {'vols': ['GRO24T1', 'GRO24T2'], 'front': {
        'GRO24T1': [(1, 'front', ''), (5, 'epitre', 'Épître dédicatoire'), (9, 'preface', 'Préface du traducteur'),
                    (52, 'toc', ''), (55, 'prolegomena', 'Discours préliminaire'), (91, 'text', None)],
        'GRO24T2': [(1, 'front', ''), (None, 'text', None)]}},
    'PUF34': {'vols': ['PUF34T1', 'PUF34T2'], 'front': {
        'PUF34T1': [(1, 'front', ''), (11, 'epitre', 'Épître dédicatoire'), (21, 'avertissement', 'Avertissement'),
                    (31, 'preface', 'Préface du traducteur'), (152, 'toc', ''), (155, 'text', None)],
        'PUF34T2': [(1, 'front', ''), (None, 'text', None)]}},
}

def reading(s):
    s = re.sub(r'</?i>', '', s).replace('ſ', 's')
    s = re.sub(r'(\w)-\n(?=[a-zàâäéèêëîïôöùûüç])', lambda m: m.group(1), s)
    s = re.sub(r'\s*\n\s*', ' ', s)
    return re.sub(r'  +', ' ', s).strip()

def locus(st, para=True):
    if st['sect'] == 'text':
        if not st['livre']: return ''
        l = 'Liv. %s' % roman(st['livre'])
        if st['chap']: l += ' ch. %s' % roman(st['chap'])
        if para and st['para']: l += ' § %d' % st['para']
        return l
    pre = st['prefix'] or ''
    return pre + (' § %d' % st['para'] if para and st['para'] and pre else '')

def sec_parse(sec):
    """'§. VII' -> (None, None, 7); 'CH. II. §. I' -> (None, 2, 1); 'LIV. II. CH. I. §. I' -> (2, 1, 1)."""
    s = sec.upper().replace(' ', '')
    lv = re.search(r'LIV\.?([IVXL]+)', s); ch = re.search(r'CH(?:AP)?\.?([IVXL]+)', s); pa = re.search(r'§\.?([IVXLC]+)', s)
    return (unroman(lv.group(1)) if lv else None, unroman(ch.group(1)) if ch else None, unroman(pa.group(1)) if pa else None)

def build(work):
    cfg = WORKS[work]; pages = []
    st = {'sect': 'front', 'prefix': '', 'livre': 0, 'chap': 0, 'para': 0}
    seen = []  # (livre, chap, para, sect, prefix) in body order, for note loci
    lastsec = ''
    for vol in cfg['vols']:
        front = cfg['front'].get(vol, [])
        for f in sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol))):
            d = json.load(open(f)); scan = d['scan']
            for first, sect, prefix in front:
                if first is not None and scan == first:
                    st.update(sect=sect, prefix=prefix, para=0)
                    if sect == 'text': st.update(livre=0, chap=0)
            kind = d.get('kind', 'text')
            pg = {'id': '%s.p%d' % (vol, scan), 'vol': vol, 'scan': scan, 'page': d.get('page', ''), 'kind': kind,
                  'head': reading(d.get('head', ''))}
            if kind in ('toc', 'index', 'errata', 'blank', 'plate', 'title', 'other') and not d.get('body', '').strip():
                pg.update(sect=st['sect'], text='', spans=[], margin=[], notes=[]); pages.append(pg); continue
            # main text: walk lines, markers update the state
            text = ''; spans = []; cur = locus(st); start = 0; pstarts = []
            def close():
                nonlocal start
                if len(text) > start: spans.append([start, len(text), cur])
                start = len(text)
            raw = re.sub(r'(\w)-\n(?=[a-zſàâäéèêëîïôöùûüç])', lambda m: m.group(1) + '\x00', re.sub(r'</?i>', '', d.get('body', '')))
            raw = re.sub(r'[ \t]*(<<\s*(?:LIVRE|CHAP|§)\s*\d+\s*>>)[ \t]*', r'\n\1\n', raw)
            for line in raw.split('\n'):
                m = re.match(r'\s*<<\s*(LIVRE|CHAP|§)\s*(\d+)\s*>>\s*$', line)
                if m:
                    close(); kind_m, n = m.group(1), int(m.group(2))
                    if kind_m == 'LIVRE':
                        if st['sect'] != 'text': st.update(sect='text', prefix=None)
                        st.update(livre=n, chap=0, para=0)
                    elif kind_m == 'CHAP':
                        if st['sect'] != 'text': st.update(sect='text', prefix=None)
                        st.update(chap=n, para=0)
                    else:
                        st['para'] = n; pstarts.append(locus(st))
                    seen.append((st['sect'], st['prefix'], st['livre'], st['chap'], st['para']))
                    cur = locus(st); continue
                if not line.strip(): continue
                piece = reading(line.replace('\x00', ''))
                text += (' ' if text and not text.endswith(' ') else '') + piece
            close()
            text = re.sub(r'  +', ' ', text)
            pg_loc0 = spans[0][2] if spans else cur
            # margin: lettered notes follow the calls of the same letter in the body; summaries follow the § starts
            margin = []; calls = [(m.start(), m.group(0)) for m in re.finditer(r'\([a-z]\)', text)]; used = set(); k = 0
            for mg in d.get('margin', []):
                mk = mg.get('mark', '') if isinstance(mg, dict) else ''
                tx = reading(mg.get('text', '') if isinstance(mg, dict) else str(mg))
                loc = pg_loc0
                if mk:
                    for i, (pos, c) in enumerate(calls):
                        if c == mk and i not in used:
                            used.add(i); loc = next((s[2] for s in spans if s[0] <= pos < s[1]), pg_loc0); break
                else:
                    if k < len(pstarts): loc = pstarts[k]
                    k += 1
                margin.append({'mark': mk, 'text': tx, 'locus': loc})
            # notes: group label, else the last label; chapter = latest body occurrence of that §
            notes = []
            for nt in d.get('notes', []):
                sec = (nt.get('sec') or '').strip() or lastsec
                if nt.get('sec'): lastsec = nt['sec'].strip()
                lv, ch, pa = sec_parse(sec) if sec else (None, None, None)
                base = ''
                if pa:
                    for s_, p_, l_, c_, a_ in reversed(seen[-40:]):
                        if s_ != st['sect'] or (s_ == 'text' and l_ != (lv or st['livre'])): continue
                        if a_ == pa and (ch is None or c_ == ch):
                            base = locus({'sect': s_, 'prefix': p_, 'livre': l_, 'chap': c_, 'para': a_}); break
                    if not base and st['sect'] == 'text' and st['livre']:
                        base = locus({**st, 'chap': ch or st['chap'], 'para': pa})
                if not base: base = pg_loc0
                mk = nt.get('mark', '')
                if mk == '' and notes:  # an unnumbered paragraph that goes on from the note before it
                    mk = notes[-1]['mark']; base = notes[-1]['locus'].split(', n.')[0]
                if mk == 'cont' and notes: mk = notes[-1]['mark']
                elif mk == 'cont' and pages:
                    prev = next((p for p in reversed(pages) if p.get('notes')), None)
                    if prev: mk = prev['notes'][-1]['mark']; base = prev['notes'][-1]['locus'].split(', n.')[0]
                nm = re.sub(r'[()]', '', mk)
                notes.append({'mark': mk, 'sec': sec, 'by': nt.get('by', ''), 'text': reading(nt.get('text', '')),
                              'locus': base + (', n. %s' % nm if nm and nm != 'cont' else '')})
                if nt.get('mark') == 'cont' and len(notes) == 1: notes[0]['cont'] = True
            pg.update(sect=st['sect'], text=text, spans=spans, margin=margin, notes=notes)
            pages.append(pg)
    # a note split over two pages is the author's on both pages if either part is signed
    prev = None
    for p in pages:
        if p.get('notes') and p['notes'][0].get('cont') and prev and prev['notes']:
            a, b = prev['notes'][-1], p['notes'][0]
            if 'author' in (a['by'], b['by']): a['by'] = b['by'] = 'author'
        if p.get('notes'): prev = p
    return pages

if __name__ == '__main__':
    work = sys.argv[1]
    pages = build(work)
    os.makedirs(B + '/corpus', exist_ok=True)
    json.dump({'work': work, 'pages': pages}, open('%s/corpus/%s.json' % (B, work), 'w'), ensure_ascii=False)
    n = sum(1 for p in pages if p['text'])
    print(work, len(pages), 'pages,', n, 'with text,', sum(len(p['notes']) for p in pages), 'notes')
