# essai_data.py <texts/vattel-loisir-1747/LOI47.json> <out data.json>: Vattel's Essai sur le fondement du droit naturel (Le loisir philosophique, 1747),
# from the page transcriptions (LOI47, scans 19-86) to a working-edition data.json: one section per numbered paragraph
# (E.1 ... E.41, as printed; the print has no 28 and no 32) and the title (E.0). Reading text: long s as s, line-end
# hyphens joined (kept before t-, il, vous, même, ...), running heads, catchwords and signatures dropped, page breaks as
# <span class="pb">. Each footnote goes to the section whose text calls it on that page; "cont" notes join the note before.
import sys, os, re, json, glob, html
TR, OUT = sys.argv[1], sys.argv[2]
GB = 'https://books.google.com/books?id=130TAAAAQAAJ&pg=PA%s'
KEEP = {'t', 'il', 'ils', 'elle', 'elles', 'on', 'vous', 'nous', 'je', 'tu', 'moi', 'toi', 'lui', 'leur', 'là', 'ci', 'même', 'mêmes', 'être', 'ce', 'y', 'en', 'dire'}
PB = ' <span class="pb" data-pg="%d">p. %s</span> '
AMBIG = {'on', 'ce', 'en', 'y', 'ci', 'je', 'il', 'le'}   # also endings of ordinary words (acti-on, essen-ce)
VOCAB = set()
for pg in json.load(open(TR))['pages']:
    for line in pg['body'].replace('ſ', 's').split('\n'):
        VOCAB |= {w.lower() for w in re.findall(r'[\wÀ-ÿ]+', re.sub(r'<[^>]+>', '', line))[1:-1]}

def join_lines(s):
    """Line breaks of one zone: a hyphen at line end is joined to the next word unless that word is a pronoun or particle
    (dites-\nvous, arrivera-\nt-il); quotation marks at the start of the continuation line go; italics split over the
    break are merged."""
    def rep(m):
        pre, close, opn, word = m.group(1), m.group(2) or '', m.group(4) or '', m.group(5)
        w = re.split(r"[-'’]", word.lower())[0]
        if close and opn: close = opn = ''
        frag = re.search(r'[\wÀ-ÿ]+$', s[:m.start(1) + 1]).group(0).lower()
        keep = w in KEEP and (w not in AMBIG or (frag + w) not in VOCAB)
        return pre + ('-' if keep else '') + close + opn + word
    s = re.sub(r'(\w)-(</i>)?\n((?:„|,,)\s*)?(<i>)?([\wÀ-ÿ]+)', rep, s)
    return re.sub(r'\s*\n\s*', ' ', s)

def reading(s): return join_lines(s.replace('ſ', 's'))

def esc(s):
    """Escape for HTML, keeping <i>…</i>."""
    parts = re.split(r'(</?i>)', s)
    return ''.join(p if p in ('<i>', '</i>') else html.escape(p) for p in parts)

pages = json.load(open(TR))['pages']
pages = [p for p in pages if 19 <= p['scan'] <= 86]
assert [p['scan'] for p in pages] == list(range(19, 87))
secs = []; cur = None; pending_hyphen = None
title = None
for p in pages:
    body = p['body']
    # a catchword the reader wrote as the last body line
    lines = body.rstrip().split('\n'); norm = lambda x: re.sub(r'<[^>]+>|„|,,|\s', '', x).replace('ſ', 's')
    if len(lines) > 1 and p.get('catch') and norm(lines[-1]) == norm(p['catch']): body = '\n'.join(lines[:-1])
    if p['scan'] == 19:
        pre, body = body.split('<<§ 1>>', 1)
        pre = re.sub(r'^\s*PIECES\s*\n?\s*DIVERSES\.\s*', '', pre.replace('ſ', 's'))
        title = re.sub(r'\s+', ' ', reading(pre)).strip()
        secs.append({'id': 'E.0', 'chap': 0, 'para': 0, 'margin': '', 'html': esc(title), 'notes': [], 'pages': [{'scan': 19, 'printed': '3', 'z': GB % 3}], 'citedBy': []})
        body = '<<§ 1>>' + body
        printed = '3'
    else:
        printed = p['page']
    segs = re.split(r'<<§ (\d+)>>\n?', body)
    first = True
    # text before the first marker continues the current section
    chunks = [(None, segs[0])] + [(int(segs[i]), segs[i + 1]) for i in range(1, len(segs), 2)]
    for n, raw in chunks:
        if n is not None:
            cur = {'id': 'E.%d' % n, 'chap': 0, 'para': n, 'margin': '', 'raw': [], 'notes': [], 'pages': [], 'citedBy': []}
            secs.append(cur)
        if cur is None or cur['id'] == 'E.0': continue
        if not raw.strip(): continue
        if not cur['pages'] or cur['pages'][-1]['scan'] != p['scan']:
            if cur['raw'] and p['scan'] != 19:
                cur['raw'].append(('pb', p['scan'], printed))
            cur['pages'].append({'scan': p['scan'], 'printed': printed, 'z': GB % printed})
        cur['raw'].append(('t', raw.rstrip('\n'), p['scan']))
    # notes of this page: to the section that calls them on this page
    for nt in p['notes']:
        mk = nt['mark'].strip()
        if mk == 'cont':
            last = next(s for s in reversed(secs) if s['notes'])
            last['notes'][-1]['raw'] += '\n' + nt['text']; continue
        host = None
        for s in reversed(secs):
            if s['id'] == 'E.0': continue
            txt = ''.join(x[1] for x in s.get('raw', []) if x[0] == 't' and x[2] == p['scan'])
            if mk in txt.replace(' ', '') or mk.replace('(', '( ').replace(')', ' )') in txt or re.sub(r'[()]', '', mk) and re.search(r'\(\s*(<i>)?%s(</i>)?\s*\)' % re.escape(re.sub(r'[()]', '', mk)), txt):
                host = s; break
        if host is None: host = cur; print('note without call on its page', p['scan'], mk)
        host['notes'].append({'mark': mk, 'raw': nt['text']})

# assemble html: join text pieces; a word split over a page break is joined and the break goes after it
for s in secs:
    if s['id'] == 'E.0': continue
    out = ''
    for x in s.pop('raw'):
        if x[0] == 'pb':
            m = re.search(r'(\w)-\s*$', out)
            if m: out = out[:m.start() + 1]; s['_hold'] = PB % (x[1], x[2])
            else: out = out.rstrip() + PB % (x[1], x[2])
            continue
        t = esc(reading(x[1]))
        if s.get('_hold'):
            m = re.match(r'(\S*)(.*)', t, re.S); out += m.group(1) + s.pop('_hold') + m.group(2).lstrip()
        else:
            out += t if out.endswith(' ') or not out else ' ' + t
    s['html'] = re.sub(r'\s+', ' ', out).strip()
    s['notes'] = [{'mark': n['mark'], 'html': re.sub(r'\s+', ' ', esc(reading(n['raw']))).strip()} for n in s['notes']]
json.dump({'sections': secs, 'rows': [], 'titles': {'E': title}}, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(secs), 'sections', sum(len(s['notes']) for s in secs), 'notes', sum(len(s['html']) for s in secs), 'chars')
