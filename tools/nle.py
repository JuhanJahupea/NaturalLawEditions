# Shared conversion code: a working edition's data.json (section HTML with reuse spans) -> the collection format (docs/FORMAT.md).
import collections, hashlib, json, os, re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(path, encoding='utf-8') as f: return json.load(f)


def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')


def sha(path):
    with open(path, 'rb') as f: return hashlib.sha256(f.read()).hexdigest()


class PageBreak:
    """The HTML a build inserts for a page break, read from its template ({vol}, {scan}, {printed})."""
    def __init__(self, tpl):
        self.lead, self.trail = tpl.startswith(' '), tpl.endswith(' ')
        m = re.fullmatch(r'<span class="pb" data-pg="([^"]*)">(.*)</span>', tpl.strip(), re.S)
        rx = lambda t: re.compile(re.escape(t).replace(r'\{vol\}', '(?P<vol>[^:]*?)').replace(r'\{scan\}', r'(?P<scan>\d+)')
                                  .replace(r'\{printed\}', '(?P<printed>.*)'), re.S)
        self.attr, self.inner = rx(m.group(1)), rx(m.group(2))

    def read(self, pg, txt):
        a = self.attr.fullmatch(pg).groupdict(); b = self.inner.fullmatch(txt).groupdict()
        vol = a.get('vol') or ''
        assert b.get('vol', vol) == vol, (pg, txt)
        return vol, int(a['scan']), b['printed']


class Parse(HTMLParser):
    """Split the display HTML of one part back into plain text and marks."""
    ALLOWED = {('i', ''), ('a', 'xr'), ('span', 'u'), ('span', 'v73'), ('span', 'para'), ('span', 'pb'), ('span', 'd58')}

    def __init__(self, src, pb, old_title=None):
        super().__init__(convert_charrefs=True)
        self.pb, self.old_title = pb, old_title
        self.chars = []; self.stack = []; self.cap = None; self.skip = False
        self.at = collections.defaultdict(list)  # offset -> inserted elements, in order
        self.feed(src); self.close()
        assert not self.stack and self.cap is None and not self.skip

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); c = a.get('class', '')
        key = (tag, c)
        assert key in self.ALLOWED, key
        assert self.cap is None and not self.skip
        if c == 'para': self.at[len(self.chars)].append(('para',))
        if c in ('pb', 'd58'): self.cap = [c, a, '']
        if c == 'pb' and self.pb.lead:  # the space the build put before the break is not text
            assert self.chars and self.chars[-1] == (' ', None, None, None, ()); self.chars.pop()
        self.stack.append(key + (a,))

    def handle_endtag(self, tag):
        t, c, a = self.stack.pop(); assert t == tag
        if c in ('pb', 'd58'):
            kind, a, txt = self.cap; self.cap = None
            if kind == 'pb':
                self.at[len(self.chars)].append(('pb',) + self.pb.read(a['data-pg'], txt))
                self.skip = self.pb.trail
            else:
                assert a['title'] == self.old_title
                self.at[len(self.chars)].append(('d58', a['data-v'], txt))

    def handle_data(self, d):
        if self.cap is not None: self.cap[2] += d; return
        if self.skip:
            assert d[0] == ' ' and not self.stack; d = d[1:]; self.skip = False
        ital = ref = var = None; cov = ()
        for t, c, a in self.stack:
            if t == 'i': ital = True
            elif c == 'xr': ref = a['href'][1:]
            elif c == 'u': cov = tuple(int(x) for x in a['data-m'].split(','))
            elif c == 'v73': var = a['data-v']
            elif c == 'para': raise AssertionError('text inside para')
        for ch in d: self.chars.append((ch, ital, ref, var, cov))


def runs(vals):
    """[(start, end, value)] for maximal runs of equal non-empty values."""
    out = []; i = 0; n = len(vals)
    while i < n:
        j = i + 1
        while j < n and vals[j] == vals[i]: j += 1
        if vals[i]: out.append((i, j, vals[i]))
        i = j
    return out


def segments(pos):
    """Contiguous [a, b) segments of a sorted list of offsets."""
    out = []
    for p in pos:
        if out and out[-1][1] == p: out[-1][1] = p + 1
        else: out.append([p, p + 1])
    return out


class Split:
    """Turn sections into text.json units; collect the reuse and variant spans for the layers and tables."""
    def __init__(self, sections, unit_head, page_break, old_title=None):
        self.units = []
        self.reuse_at = collections.defaultdict(list); self.var_at = collections.defaultdict(list)
        self.older = collections.defaultdict(list); self.whole = collections.defaultdict(list)
        order = collections.Counter(); pb = PageBreak(page_break)
        for s in sections:
            rec = unit_head(s)
            parts = [('t', s['html'])] + [('n%d' % k, n['html']) for k, n in enumerate(s['notes'])]
            notes = []
            for part, src in parts:
                P = Parse(src, pb, old_title); ch = P.chars
                text = ''.join(c[0] for c in ch)
                assert all(ord(c) <= 0xFFFF for c in text)  # offsets in UTF-16 code units equal code points
                o = {'text': text}
                it = [[a, b] for a, b, _ in runs([c[1] for c in ch])]
                xr = [[a, b, v] for a, b, v in runs([c[2] for c in ch])]
                if it: o['i'] = it
                if xr: o['xr'] = xr
                pos_rows = collections.defaultdict(list); pos_vars = collections.defaultdict(list)
                for k, c in enumerate(ch):
                    for rid in c[4]: pos_rows[rid].append(k)
                    if c[3]: pos_vars[c[3]].append(k)
                for rid, ps in pos_rows.items(): self.reuse_at[rid] += [[part, a, b] for a, b in segments(ps)]
                for vid, ps in pos_vars.items(): self.var_at[vid] += [[part, a, b] for a, b in segments(ps)]
                para = []; pbs = []
                for k in sorted(P.at):
                    els = P.at[k]
                    order[tuple(e[0] for e in els)] += 1
                    for e in els:
                        if e[0] == 'para': assert part == 't'; para.append(k)
                        elif e[0] == 'pb': assert part == 't'; pbs.append([k, e[1], e[2], e[3]])
                        else: self.older[e[1]].append([part, k, e[2]])
                if part == 't':
                    rec.update(o)
                    if para: rec['para'] = para
                    if pbs: rec['pb'] = pbs
                else:
                    ni = int(part[1:]); nt = s['notes'][ni]
                    notes.append(dict({'mark': nt['mark']}, **o))
                    if nt.get('added'):
                        ln = len(text)
                        cand = [vid for vid, ps in pos_vars.items() if ps[0] == 0 and ps[-1] == ln - 1]
                        assert len(cand) == 1, (s['id'], ni, cand)
                        self.whole[cand[0]].append(ni)
            if notes: rec['notes'] = notes
            self.units.append(rec)
        # every inserted element sequence follows the build order: paragraph, older readings, page break
        for seq in order:
            assert list(seq) == sorted(seq, key=lambda x: {'para': 0, 'd58': 1, 'pb': 2}[x]), seq
        # each reuse span lies in its own section
        self.span_unit = {}
        for s in sections:
            for m in re.finditer(r'data-m="([\d,]+)"', s['html'] + ''.join(n['html'] for n in s['notes'])):
                for x in m.group(1).split(','): self.span_unit.setdefault(int(x), set()).add(s['id'])

    def reuse_row(self, r):
        """A data.json row in the reuse-table shape. Rows on a margin or not placed keep an empty 'at' and a 'where'."""
        at = self.reuse_at.get(r['id'], [])
        if r['where'] in ('m', ''):
            assert not at; where = 'margin' if r['where'] == 'm' else 'unplaced'
        else:
            assert len(at) == 1 and at[0][0] == r['where'] and self.span_unit[r['id']] == {r['sec']}, (r['id'], at, r['where'])
            where = None
        row = {'id': r['id'], 'unit': r['sec'], 'at': at}
        if where: row['where'] = where
        row.update({'family': r['fam'], 'work': r['work'], 'locus': r['locus'], 'page': r['page'], 'inNote': r['note'], 'label': r['label'],
                    'confidence': r['conf'], 'status': r['status'], 'step': r['step'], 'passage': r['vp'], 'source': r['sp']})
        if r.get('fr'): row['french'] = r['fr']
        row['reason'] = r['reason']; row['links'] = r['links']
        for k, n in (('ew', 'earliest'), ('near', 'nearer'), ('qa', 'quoting'), ('noteref', 'noteRef'), ('part', 'sourcePart')):
            if r.get(k): row[n] = r[k]
        return row


def write_text(ed, titles, units):
    dump({'format': 'nle-text/1', 'edition': ed, 'titles': titles, 'units': units}, os.path.join(ROOT, 'editions', ed, 'text.json'))


def write_tables(ed, tables, texts, steps, description, extra=None):
    """One reuse table per source text, in the order of `texts`. Returns the catalogue entries."""
    rdir = os.path.join(ROOT, 'reuse')
    os.makedirs(rdir, exist_ok=True)
    for f in os.listdir(rdir):
        if f.startswith(ed + '__'): os.remove(os.path.join(rdir, f))
    out = []
    for t in texts:
        rows = sorted(tables.get(t['id'], []), key=lambda r: r['id'])
        if not rows: continue
        path = 'reuse/%s__%s.json' % (ed, t['id'])
        head = {'format': 'nle-reuse/1', 'from': ed, 'to': t['id']}
        head.update((extra or {}).get(t['id'], {}))
        head['steps'] = {str(k): steps[k] for k in sorted({r['step'] for r in rows}, key=str)}
        head['description'] = description
        head['rows'] = rows
        dump(head, os.path.join(ROOT, path))
        e = {'path': path, 'from': ed, 'to': t['id'], 'rows': len(rows)}
        if 'toLayer' in head: e['toLayer'] = head['toLayer']
        out.append(e)
    return out


def update_catalogue(edition, texts, reuse):
    """Add or replace the edition, the source texts it names, and its reuse tables.
    The result does not depend on the order the converters run in: tables follow the order of the editions,
    texts the order in which the tables first name them; a text named by two projects keeps both sigla.
    Texts that no reuse table names any more are dropped."""
    cp = os.path.join(ROOT, 'catalogue.json'); cat = load(cp)
    eds = cat['editions']; i = next((k for k, e in enumerate(eds) if e['id'] == edition['id']), None)
    if i is None: eds.append(edition)
    else: eds[i] = edition
    have = {t['id']: t for t in cat['texts']}
    for t in texts:
        old = have.get(t['id'], {})
        have[t['id']] = dict(t, sigla=sorted(set(old.get('sigla', [])) | set(t['sigla'])))
    rank = {e['id']: k for k, e in enumerate(eds)}
    cat['reuse'] = sorted([c for c in cat['reuse'] if c['from'] != edition['id']] + reuse, key=lambda c: rank[c['from']])
    # a source text stays in the catalogue while a reuse table names it; an edited text is listed under editions
    named = []
    for c in cat['reuse']:
        if c['to'] not in rank and c['to'] not in named: named.append(c['to'])
    cat['texts'] = [have[n] for n in named]
    with open(cp, 'w', encoding='utf-8') as f:
        json.dump(cat, f, ensure_ascii=False, indent=2); f.write('\n')


def provenance(ed, src, inputs, note=''):
    d = os.path.join(ROOT, 'editions', ed, 'provenance'); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'README.md'), 'w', encoding='utf-8') as f:
        f.write('# Provenance\n\nConverted by `tools/convert_%s.py` from `%s`:\n\n| File | Bytes | SHA-256 |\n|---|---|---|\n' % (ed.replace('-', '_'), src))
        for n, p in inputs: f.write('| `%s` | %d | `%s` |\n' % (n, os.path.getsize(p), sha(p)))
        if note: f.write('\n' + note + '\n')
