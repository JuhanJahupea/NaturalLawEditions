# def41_data.py <texts/vattel-defense-1741/DEF41.json> <out data.json>: Vattel's Défense du système leibnitien (1741), from
# the page transcriptions to a working-edition data.json, as essai_data.py does for the Essai.
#  - Units: the dedication and the Préface by page (Ded.1-10, Pref.1-48); the text by Vattel's numbered paragraphs
#    (D.1 ... D.409), each with its part (I, II), chapter (roman) and, in Partie II ch. VIII, its section; the fold-out
#    table (Tab.1). Paragraphs 345 and 346 begin on pp. 458-459, wanting in the copy: D.345 holds only the gap, and the
#    text of p. 460 opens D.346.
#  - Titles: the parts, chapters and sections, from the headings between the markers.
#  - Reading text: long s as s, line-end hyphens joined (kept before t-, il, vous, même, ...), quotation marks at the
#    start of continued lines dropped, running heads, catchwords and signatures dropped, page breaks as
#    <span class="pb">. Each footnote goes to the unit whose text calls it on that page; "cont" notes join the note before.
import sys, os, re, json, html
TR, OUT = sys.argv[1], sys.argv[2]
GB = 'https://books.google.com/books?id=qVwOAAAAQAAJ&pg=PA%s'
KEEP = {'t', 'il', 'ils', 'elle', 'elles', 'on', 'vous', 'nous', 'je', 'tu', 'moi', 'toi', 'lui', 'leur', 'là', 'ci', 'même', 'mêmes', 'être', 'ce', 'y', 'en', 'dire', 'chose'}
AMBIG = {'on', 'ce', 'en', 'y', 'ci', 'je', 'il', 'le'}
PB = '<span class="pb" data-pg="%d"> p. %s </span>'
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X'}
T = json.load(open(TR)); pages = T['pages']
VOCAB = set()
for pg in pages:
    for line in pg['body'].replace('ſ', 's').split('\n'):
        VOCAB |= {w.lower() for w in re.findall(r'[\wÀ-ÿ]+', re.sub(r'<[^>]+>', '', line))[1:-1]}

def join_lines(s):
    def rep(m):
        pre, close, opn, word = m.group(1), m.group(2) or '', m.group(4) or '', m.group(5)
        w = re.split(r"[-']", word.lower())[0]
        if close and opn: close = opn = ''
        frag = re.search(r'[\wÀ-ÿ]+$', s[:m.start(1) + 1]).group(0).lower()
        keep = w in KEEP and (w not in AMBIG or (frag + w) not in VOCAB)
        return pre + ('-' if keep else '') + close + opn + word
    s = re.sub(r'(\w)-(</i>)?\n((?:„|,,|«)\s*)?(<i>)?([\wÀ-ÿ]+)', rep, s)
    s = re.sub(r'\n\s*(?:„|,,)\s*', '\n', s)
    return re.sub(r'\s*\n\s*', ' ', s)
def reading(s): return join_lines(s.replace('ſ', 's'))
def esc(s):
    parts = re.split(r'(</?i>)', s)
    return ''.join(p if p in ('<i>', '</i>') else html.escape(p) for p in parts)
def flat(s): return re.sub(r'\s+', ' ', esc(reading(s))).strip()
def norm(x): return re.sub(r'<[^>]+>|„|,,|\s', '', x).replace('ſ', 's')

units = []; titles = {}; cur = None; part = None; chap = None; sect = None
def new(uid, div, kind, n=None):
    u = {'id': uid, 'div': div, 'kind': kind, 'n': n, 'part': part, 'chap': chap, 'section': sect,
         'raw': [], 'notes': [], 'pages': []}
    units.append(u); return u
for p in pages:
    s, printed, body = p['scan'], p.get('page', ''), p['body']
    lines = body.rstrip().split('\n')
    if len(lines) > 1 and p.get('catch') and norm(lines[-1]) == norm(p['catch']): body = '\n'.join(lines[:-1])
    if s in (17, 18): continue                                   # title page and its verso: titlepage.json
    if s in (555, 556):                                          # the fold-out table and its blank verso
        if s == 555:
            u = new('Tab.1', 'Tab', 'page', 1); u['pages'].append({'scan': s, 'printed': ''}); u['raw'].append(('t', body, s))
        continue
    if p['head'].upper().startswith('DEDICATOIRE') or '<<DEDICACE>>' in body:
        k = sum(1 for x in units if x['div'] == 'Ded') + 1
        cur = new('Ded.%d' % k, 'Ded', 'page', k); body = body.replace('<<DEDICACE>>\n', '').replace('<<DEDICACE>>', '')
        cur['pages'].append({'scan': s, 'printed': ''}); cur['raw'].append(('t', body, s)); cur['_notes_here'] = True
    elif 'PREFACE' in p['head'].upper().replace('É', 'E') or '<<PREFACE>>' in body:
        k = sum(1 for x in units if x['div'] == 'Pref') + 1
        cur = new('Pref.%d' % k, 'Pref', 'page', k); body = body.replace('<<PREFACE>>\n', '').replace('<<PREFACE>>', '')
        cur['pages'].append({'scan': s, 'printed': ''}); cur['raw'].append(('t', body, s))
    else:
        if s == 568:                                             # pp. 458-459 wanting: § 345 lost, § 346 continues on p. 460
            gap = new('D.345', 'D', 'section', 345); gap['gap'] = 'pp. 458-459'; gap['raw'].append(('gap', '', s))
            cur = new('D.346', 'D', 'section', 346); cur['gap'] = 'pp. 458-459'; cur['raw'].append(('gap', '', s))
        toks = re.split(r'(<<(?:PARTIE|CHAP|SECTION|§) \d+>>)\n?', body)
        for tok in toks:
            m = re.match(r'<<(PARTIE|CHAP|SECTION|§) (\d+)>>', tok)
            if m:
                k, n = m.group(1), int(m.group(2))
                if k == 'PARTIE': part = ROMAN[n]; chap = None; sect = None; cur = {'_title': 'P.%s' % part, 'raw': [], 'notes': []}; titles[cur['_title']] = cur
                elif k == 'CHAP': chap = ROMAN[n]; sect = None; cur = {'_title': '%s.%s' % (part, chap), 'raw': [], 'notes': []}; titles[cur['_title']] = cur
                elif k == 'SECTION': sect = n; cur = {'_title': '%s.%s.%d' % (part, chap, sect), 'raw': [], 'notes': []}; titles[cur['_title']] = cur
                else: cur = new('D.%d' % n, 'D', 'section', n)
                continue
            if not tok.strip() or cur is None: continue
            if '_title' in cur:
                if s == 83 and cur['_title'] == 'P.I' and not cur['raw']: pass
                cur['raw'].append(('t', tok, s)); continue
            if not cur['pages'] or cur['pages'][-1]['scan'] != s:
                if cur['raw']: cur['raw'].append(('pb', s, printed))
                cur['pages'].append({'scan': s, 'printed': printed})
            cur['raw'].append(('t', tok.rstrip('\n'), s))
    for nt in p['notes']:
        mk = nt['mark'].strip()
        if mk == 'cont':
            last = next(x for x in reversed(units + list(titles.values())) if x.get('notes')); last['notes'][-1]['raw'] += '\n' + nt['text']; continue
        host = None; bare = re.sub(r'[()\s]', '', mk)
        for x in reversed(units):
            txt = ''.join(r[1] for r in x['raw'] if r[0] == 't' and r[2] == s)
            if not txt: continue
            if bare and re.search(r'\(\s*(<i>)?\s*%s\s*(</i>)?\s*\)' % re.escape(bare), txt) or mk in txt: host = x; break
        if host is None:                                         # a call in a part, chapter or section heading
            for key, tv in reversed(list(titles.items())):
                txt = ''.join(r[1] for r in tv['raw'] if r[2] == s)
                if txt and bare and re.search(r'\(\s*(<i>)?\s*%s\s*(</i>)?\s*\)' % re.escape(bare), txt): host = tv; break
        if host is None:
            host = next((x for x in reversed(units) if any(r[0] == 't' and r[2] == s for r in x['raw'])), units[-1])
            print('note without call on its page', s, mk)
        host.setdefault('notes', [])
        host['notes'].append({'mark': mk, 'raw': nt['text']})

MARK = '\x00%d\x00'
for u in units:
    out = ''; pbs = []
    for x in u.pop('raw'):
        if x[0] == 'gap':
            out += (' ' if out else '') + '<span class="gap">[pp. 458–459 wanting in this copy]</span> '; continue
        if x[0] == 'pb':
            pbs.append(PB % (x[1], x[2]))
            m = re.search(r'(\w)-\s*(</i>)?\s*$', out)
            if m: u['_hold'] = (MARK % (len(pbs) - 1), m)
            else: out = out.rstrip() + ' ' + MARK % (len(pbs) - 1) + ' '
            continue
        t = esc(reading(x[1]))
        if u.get('_hold'):
            mk, m = u.pop('_hold')
            t = re.sub(r'^\s*(?:„|,,)\s*', '', t)
            ital = bool(m.group(2) and t.startswith('<i>'))
            if ital: t = t[3:]
            w = re.match(r'[\wÀ-ÿ]+', t); w = w.group(0).lower() if w else ''
            frag = re.search(r'[\wÀ-ÿ]+$', out[:m.start(1) + 1]).group(0).lower()
            keep = w in KEEP and (w not in AMBIG or (frag + w) not in VOCAB)
            out = out[:m.start(1) + 1] + ('-' if keep else '') + ('' if ital else (m.group(2) or ''))
            m2 = re.match(r'(\S*)(.*)', t, re.S)
            if ital and '</i>' not in m2.group(1): out += m2.group(1) + '</i>' + mk + '<i>' + m2.group(2).lstrip()
            else: out += m2.group(1) + mk + m2.group(2)
        else:
            out += t if out.endswith(' ') or not out else ' ' + t
    out = re.sub(r'\s+', ' ', out).strip()
    u['html'] = re.sub(r'\s*\x00(\d+)\x00\s*', lambda m: ' ' + pbs[int(m.group(1))], out)
    u['notes'] = [{'mark': n['mark'], 'html': flat(n['raw'])} for n in u['notes']]
    for pg in u['pages']:
        if pg['printed']: pg['z'] = GB % pg['printed']
    u.pop('_notes_here', None)
T2 = {k: flat(''.join(r[1] + '\n' for r in v['raw'])) for k, v in titles.items()}
TN = {k: [{'mark': n['mark'], 'html': flat(n['raw'])} for n in v['notes']] for k, v in titles.items() if v.get('notes')}
json.dump({'units': units, 'titles': T2, 'titleNotes': TN, 'lacunae': T.get('lacunae', [])}, open(OUT, 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(units), 'units', dict(Counter(u['div'] for u in units)), sum(len(u['notes']) for u in units), 'notes',
      sum(len(u['html']) for u in units), 'chars;', len(T2), 'titles')
