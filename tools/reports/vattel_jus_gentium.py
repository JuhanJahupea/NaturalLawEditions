# vattel_jus_gentium.py: the data report "Vattel's Droit des gens and Wolff's Jus gentium: the order of reuse".
# Reads the edition's text and its Jus gentium table (match rows), writes reports/vattel-jus-gentium.md, the figure
# reports/vattel-jus-gentium.svg, and the report's entry in reports/index.json with the edition version it was built from.
# Run it again whenever the table changes: the numbers in the report come only from the data.
import os, re, json, math, collections, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED, TX, RID = 'vattel-1773', 'wolff-jus-gentium-1749', 'vattel-jus-gentium'
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
man = load('editions/%s/edition.json' % ED); T = load('editions/%s/text.json' % ED)
units = [u for u in T['units'] if u.get('kind') != 'heading']
idx = {u['id']: i for i, u in enumerate(units)}
rows = [r for r in load('reuse/%s__%s.json' % (ED, TX))['rows'] if r['status'] == 'match']
pts = []
for r in rows:
    m = re.match(r'§ ?(\d+)', r.get('locus') or '')
    if m and r['unit'] in idx: pts.append((idx[r['unit']], int(m.group(1)), r['unit']))
# Wolff's chapters: first § of each (Jus gentium, 1749)
JGCH = [(1, 'Prol.', 'Prolegomena'), (27, 'I', 'duties of nations to themselves'), (156, 'II', 'duties of nations to one another'),
        (274, 'III', 'dominion'), (368, 'IV', 'treaties'), (562, 'V', 'settling disputes'), (607, 'VI', 'the right of war'),
        (777, 'VII', 'the law of nations in war'), (959, 'VIII', 'peace'), (1041, 'IX', 'embassies')]
JGEND = 1100
def jgch(n): return [c for c in JGCH if c[0] <= n][-1][1]
BOOKS = [('Pref', 'Préface'), ('Prelim', 'Préliminaires'), ('I', 'Livre I'), ('II', 'Livre II'), ('III', 'Livre III'), ('IV', 'Livre IV')]
bk = lambda uid: uid.split('.')[0]
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r
rx, ry = rank([p[0] for p in pts]), rank([p[1] for p in pts]); n = len(pts)
mx, my = sum(rx) / n, sum(ry) / n
rho = sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
secs = {b: [u for u in units if bk(u['id']) == b] for b, _ in BOOKS}
withjg = collections.defaultdict(set); dist = collections.defaultdict(collections.Counter)
for x, y, u in pts: withjg[bk(u)].add(u); dist[bk(u)][jgch(y)] += 1
# chapters of Vattel's books with the fewest sections tied to the Jus gentium
chap = collections.defaultdict(list)
for u in units:
    if u.get('chap') and bk(u['id']) in ('I', 'II', 'III', 'IV'): chap['%s.%s' % (bk(u['id']), u['chap'])].append(u['id'])
def roman(k):
    o = ''
    for v, s in ((10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while k >= v: o += s; k -= v
    return o
allu = {u for _, _, u in pts}
low = []
for key, ids in chap.items():
    b, c = key.split('.'); share = sum(1 for i in ids if i in allu) / len(ids)
    if len(ids) >= 8: low.append((share, b, c, len(ids), T['titles'].get('%s.%s' % (b, c), '')))
low.sort()
# figure
W, H, L, B, TOP, R = 960, 560, 64, 44, 16, 200
X = lambda i: L + i / (len(units) - 1) * (W - L - R)
Y = lambda s: TOP + s / JGEND * (H - TOP - B)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="IBM Plex Sans, system-ui, sans-serif" font-size="12" role="img" aria-label="Sections of the Droit des gens against the § of the Jus gentium each reuses">' % (W, H),
       '<style>.ax{stroke:#5e6662;stroke-width:1}.g{stroke:#d9ddd6;stroke-width:1}.t{fill:#5e6662}.p{fill:#b5462f;fill-opacity:.45}.band{fill:#eceee9}'
       '@media (prefers-color-scheme:dark){.ax{stroke:#9aa39e}.g{stroke:#2c322f}.t{fill:#9aa39e}.p{fill:#f08a72;fill-opacity:.5}.band{fill:#202522}}</style>']
for k, (s, lab, name) in enumerate(JGCH):
    e = JGCH[k + 1][0] if k + 1 < len(JGCH) else JGEND
    if k % 2: svg.append('<rect class="band" x="%d" y="%.1f" width="%d" height="%.1f"/>' % (L, Y(s), W - L - R, Y(e) - Y(s)))
    svg.append('<text class="t" x="%d" y="%.1f" dominant-baseline="middle">%s %s</text>' % (W - R + 8, (Y(s) + Y(e)) / 2, lab, name))
for b, lab in BOOKS:
    ids = [idx[u['id']] for u in secs[b]]
    if not ids: continue
    svg.append('<line class="g" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (X(ids[0]), X(ids[0]), TOP, H - B))
    if b != 'Pref': svg.append('<text class="t" x="%.1f" y="%d" text-anchor="middle">%s</text>' % ((X(ids[0]) + X(ids[-1])) / 2, H - B + 18, lab.replace('Livre ', '')))
for s in (0, 200, 400, 600, 800, 1000):
    svg.append('<text class="t" x="%d" y="%.1f" text-anchor="end" dominant-baseline="middle">%d</text>' % (L - 8, Y(s), s))
svg.append('<line class="ax" x1="%d" x2="%d" y1="%d" y2="%d"/>' % (L, L, TOP, H - B))
svg.append('<line class="ax" x1="%d" x2="%d" y1="%d" y2="%d"/>' % (L, W - R, H - B, H - B))
svg.append('<text class="t" x="%d" y="%d" text-anchor="middle">Droit des gens, sections in order (Prélim., Livres I–IV)</text>' % ((L + W - R) / 2, H - 6))
svg.append('<text class="t" transform="translate(16 %d) rotate(-90)" text-anchor="middle">Jus gentium §</text>' % ((TOP + H - B) / 2))
svg += ['<circle class="p" cx="%.1f" cy="%.1f" r="2.2"/>' % (X(x), Y(y)) for x, y, _ in pts]
svg.append('</svg>')
os.makedirs(os.path.join(ROOT, 'reports'), exist_ok=True)
open(os.path.join(ROOT, 'reports', RID + '.svg'), 'w').write('\n'.join(svg) + '\n')
# text
fmt = lambda k: '{:,}'.format(k)
tab = ['| Book | Sections | With a *Jus gentium* row | Wolff\'s chapters reused (share of the book\'s rows) |', '|---|---|---|---|']
for b, lab in BOOKS:
    tot = sum(dist[b].values())
    main = ', '.join('%s %d%%' % (c, round(100 * k / tot)) for c, k in dist[b].most_common() if k / tot >= 0.1) if tot else ''
    tab.append('| %s | %d | %d (%d%%) | %s |' % (lab, len(secs[b]), len(withjg[b]), round(100 * len(withjg[b]) / max(1, len(secs[b]))), main))
lows = ['- Livre %s ch. %s, *%s*: %d of %d sections (%d%%).' % (b, c, re.sub(r'\s+', ' ', t).strip().rstrip('.').replace(' ,', ','), round(s * n_), n_, round(100 * s))
        for s, b, c, n_, t in low[:6]]
ver = man['version']; today = datetime.date.today().isoformat()
md = """# Vattel's *Droit des gens* and Wolff's *Jus gentium*: the order of reuse

*Data report, generated from the edition {ed} {ver} by `tools/reports/vattel_jus_gentium.py` on {today}. The numbers change when the table changes; the script writes them again.*

![Each dot is a match row: the place of a section in the Droit des gens (horizontal) against the § of the Jus gentium it reuses (vertical).](vattel-jus-gentium.svg)

{rows} match rows tie {nsec} of the {nall} sections of the *Droit des gens* (1773) to Wolff's *Jus gentium* (1749). {pts} of them name a § of Wolff.

Vattel follows Wolff's order. Spearman's rank correlation between the place of a section in the *Droit des gens* and the § of Wolff it reuses is {rho:.2f}. The dots run along one diagonal, chapter after chapter of Wolff.

{tab}

Wolff's chapters: Prol. §§ 1–26; I, duties of nations to themselves, from § 27; II, duties to one another, from § 156; III, dominion, from § 274; IV, treaties, from § 368; V, settling disputes, from § 562; VI, the right of war, from § 607; VII, the law of nations in war, from § 777; VIII, peace, from § 959; IX, embassies, from § 1041.

Chapters of eight sections or more with the smallest share of sections tied to the *Jus gentium*:

{lows}

Method: the rows are those of the edition's *Jus gentium* table at status match (`reuse/{ed}__{tx}.json`). A row names a § of Wolff where its locus begins with "§". A section counts as tied when it has at least one such row. [Open the edition](../viewer/?ed={ed}).
""".format(ed=ED, ver=ver, today=today, rows=fmt(len(rows)), nsec=fmt(len(allu)), nall=fmt(len(units)), pts=fmt(len(pts)), rho=rho,
           tab='\n'.join(tab), lows='\n'.join(lows), tx=TX)
open(os.path.join(ROOT, 'reports', RID + '.md'), 'w', encoding='utf-8').write(md)
ip = os.path.join(ROOT, 'reports', 'index.json')
I = json.load(open(ip)) if os.path.exists(ip) else {'format': 'nle-reports/1', 'reports': []}
entry = {'id': RID, 'kind': 'report', 'title': "Vattel's Droit des gens and Wolff's Jus gentium: the order of reuse",
         'summary': 'Vattel follows Wolff chapter by chapter: rank correlation %.2f over %s rows. Where he leaves Wolff.' % (rho, fmt(len(pts))),
         'date': today, 'file': RID + '.md', 'editions': [ED], 'texts': [TX], 'versions': {ED: ver}, 'generator': 'tools/reports/vattel_jus_gentium.py'}
I['reports'] = [r for r in I['reports'] if r['id'] != RID] + [entry]
json.dump(I, open(ip, 'w'), ensure_ascii=False, indent=1)
print(len(rows), 'rows;', len(pts), 'with a §; rho %.3f;' % rho, len(allu), 'sections')
