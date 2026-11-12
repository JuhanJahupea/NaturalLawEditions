# en_align.py <units_en.json> <plain_fr.json> <text.json> <out layer>: sentence alignment of Nugent's English with the 1747
# French, chapter by chapter. Gale-Church length costs; a group of French sentences stays inside one section; an English
# section that Nugent numbers starts at the first sentence of the French section with that number (where Nugent leaves a
# number out, the alignment finds the boundary). Writes the translation layer in the format of the Vattel edition.
import sys, re, json, math, collections
ef, pf, tf, out = sys.argv[1:5]
EN = json.load(open(ef)); PL = json.load(open(pf)); T = json.load(open(tf))
units = [u for u in T['units'] if u['kind'] != 'heading']
ABBR = r'(?:§|Liv|Ch|Chap|chap|Art|art|Mr|M|Mrs|St|Dr|p|pp|v|vol|n|Voy|Sect|sect|Lib|lib|cap|Tom|tom|ib|Ib|Id|id|ver|Ps|Matth|Rom|Cor|Gen|Exod|Deut|Prov|Eccl|Heb|Jac|Act|Joh|Luc|Marc|viz|i\.e|e\.g|&c|ch|liv|L|T|S)'
def sentences(t):
    out = []; start = 0
    for m in re.finditer(r'[.!?]["»”’)]*\s+(?=[«"“A-ZÀ-ÝŒÆ(§])', t):
        pre = t[max(0, m.start() - 12):m.start() + 1]
        if re.search(r'(?:^|[\s(])' + ABBR + r'\.$', pre) or re.search(r'(?:^|[\s(])[IVXLC]+\.$', pre) or re.search(r'\b\d+\.$', pre):
            continue
        end = m.start() + 1
        while end < len(t) and t[end] in '"»”’)': end += 1
        out.append((start, end)); start = m.end()
    if start < len(t.rstrip()): out.append((start, len(t.rstrip())))
    return [(a, b) for a, b in out if t[a:b].strip()]
def phi(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
PRIOR = {(1, 1): .89, (1, 0): .005, (0, 1): .005, (2, 1): .0445, (1, 2): .0445, (2, 2): .011, (3, 1): .003, (1, 3): .003, (3, 2): .002, (2, 3): .002}
def cost(lf, le, c, s2=6.8):
    if lf == 0 or le == 0: return 0.0
    m = (lf + le / c) / 2
    d = (le - lf * c) / math.sqrt(m * s2)
    p = max(1e-12, 2 * (1 - phi(abs(d))))
    return -math.log(p)
def chapter_of(uid): return '.'.join(uid.split('.')[:2]) if uid != 'AV' else 'AV'
chapters = collections.OrderedDict()
for u in units: chapters.setdefault(chapter_of(u['id']), []).append(u['id'])
layer = {}; stats = collections.Counter()
for ch, uids in chapters.items():
    ekeys = sorted([k for k in EN if chapter_of(k) == ch], key=lambda k: int(k.split('.')[-1]) if k != 'AV' else 0)
    if not ekeys: stats['chapters without English'] += 1; continue
    F = []  # (unit, start, end, length)
    for uid in uids:
        for a, b in sentences(PL[uid]): F.append((uid, a, b, b - a))
    E = []; anchor = {}
    for k in ekeys:
        ss = sentences(EN[k]['text'])
        if k in uids or k == 'AV': anchor[len(E)] = k
        for a, b in ss: E.append((k, EN[k]['text'][a:b].strip()))
    first = {}
    for i, f in enumerate(F): first.setdefault(f[0], i)
    afirst = {v: k for k, v in anchor.items()}  # unit -> English anchor index
    c = sum(len(e[1]) for e in E) / max(1, sum(f[3] for f in F))
    n, m = len(F), len(E); INF = float('inf')
    D = [[INF] * (m + 1) for _ in range(n + 1)]; B = [[None] * (m + 1) for _ in range(n + 1)]; D[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if D[i][j] == INF: continue
            for (a, b), pr in PRIOR.items():
                if i + a > n or j + b > m: continue
                fu = {F[x][0] for x in range(i, i + a)}
                if len(fu) > 1: continue
                if any(x in anchor for x in range(j + 1, j + b)): continue  # an anchor must open its group
                if j in anchor and b and anchor[j] in first and (a == 0 or i != first[anchor[j]]): continue
                if a and i == first.get(F[i][0]) and F[i][0] in afirst and (b == 0 or j != afirst[F[i][0]]): continue
                lf = sum(F[x][3] for x in range(i, i + a)); le = sum(len(E[y][1]) for y in range(j, j + b))
                cc = D[i][j] - math.log(pr) + cost(lf, le, c)
                if cc < D[i + a][j + b]: D[i + a][j + b] = cc; B[i + a][j + b] = (a, b)
    if D[n][m] == INF: stats['chapters not aligned'] += 1; print('no alignment', ch); continue
    groups = []; i, j = n, m
    while i or j:
        a, b = B[i][j]; groups.append((list(range(i - a, i)), list(range(j - b, j)))); i -= a; j -= b
    groups.reverse()
    # assign groups to units; English-only groups go with the group before (or after, at the start)
    per = collections.OrderedDict((u, []) for u in uids); last = uids[0]
    for fi, ej in groups:
        if fi: last = F[fi[0]][0]
        per[last].append((fi, ej))
    for uid, gs in per.items():
        fidx = [x for x in range(len(F)) if F[x][0] == uid]
        if not fidx: continue
        base = fidx[0]; sents = []; align = []
        for fi, ej in gs:
            loc = list(range(len(sents), len(sents) + len(ej))); sents += [E[y][1] for y in ej]
            align.append([[x - base for x in fi], loc])
        src = [k for k in ekeys if k == uid] or [E[gs[0][1][0]][0]] if gs and gs[0][1] else ekeys[:1]
        k0 = src[0] if src else ekeys[0]
        layer[uid] = {'page': EN.get(uid, EN[k0])['page'], 'sents': sents, 'notes': EN[uid]['notes'] if uid in EN else [],
                      'fr': [[F[x][1], F[x][2]] for x in fidx], 'align': align, 'flags': []}
        stats['units'] += 1; stats['1-1'] += sum(1 for f, e in align if len(f) == 1 and len(e) == 1); stats['groups'] += len(align)
        stats['fr only'] += sum(1 for f, e in align if not e); stats['en only'] += sum(1 for f, e in align if not f)
json.dump(layer, open(out, 'w'), ensure_ascii=False)
print(dict(stats))
