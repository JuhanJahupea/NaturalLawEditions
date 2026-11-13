# note_moves.py <notes dir> <corrections out>: the readers' answers (NOTE_PAGE_PROMPT.md) -> editions/vattel-1773/corrections.json
# noteMoves. A note moves when the reader puts its call in another unit, is certain, and that unit shares a printed page with
# the note's unit. Continuation notes go with the note they continue. Prints what it leaves out and the balance after moves.
import os, json, glob, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
d, out = sys.argv[1:3]
U = json.load(open(R + '/editions/vattel-1773/text.json'))['units']; by = {u['id']: u for u in U}; order = {u['id']: i for i, u in enumerate(U)}
def strip(h): return re.sub(r'<[^>]+>', '', h)
pages = lambda uid: {(p.get('vol'), p['printed']) for p in by[uid]['pages']}
ans = [a for f in sorted(glob.glob(d + '/out/*.json')) for a in json.load(open(f))['notes']]
seen = {}
for a in ans: seen[(a['unit'], a['index'])] = a
moves = []; skipped = []; c = collections.Counter()
for (uid, i), a in sorted(seen.items(), key=lambda x: (order[x[0][0]], x[0][1])):
    n = by[uid]['notes'][i]
    if n['mark'] == 'cont': continue
    to = a.get('call_unit')
    if not to or to == uid: c['stays'] += 1; continue
    if to not in by: skipped.append((uid, i, n['mark'], to, 'unknown unit')); continue
    if not a.get('certain'): skipped.append((uid, i, n['mark'], to, 'not certain: ' + a.get('remark', ''))); continue
    if not (pages(uid) & pages(to)) and abs(order[uid] - order[to]) > 1 and a.get('page') not in {p for _, p in pages(to)}:
        skipped.append((uid, i, n['mark'], to, 'no shared page')); continue
    cont = []; j = i + 1
    while j < len(by[uid]['notes']) and by[uid]['notes'][j]['mark'] == 'cont': cont.append(j); j += 1
    m = {'from': uid, 'note': i, 'mark': n['mark'], 'to': to, 'start': strip(n['text'])[:60], 'page': a.get('page', ''),
         'reason': 'Printed at the foot of p. %s; answers the call %s in %s%s.' % (a.get('page', '?'), a.get('call_mark', '?'), to, (' (' + a['remark'] + ')') if a.get('remark') else '')}
    if cont: m['cont'] = cont
    moves.append(m); c['moves'] += 1
# unmarked paragraphs that continue a note of the section before (decided by hand from the readers' remarks)
EXTRA = [('IV.102', 0, 'IV.101', "Unmarked paragraph at the head of p. 283 ('Le même historien …'); continues the Timur-Bec note of IV.101."),
         ('IV.111', 2, 'IV.110', 'Unmarked paragraph on p. 294 after note (b); continues that note, whose call is in IV.110.')]
for uid, i, to, why in EXTRA:
    n = by[uid]['notes'][i]; assert n['mark'] == ''
    moves.append({'from': uid, 'note': i, 'mark': '', 'to': to, 'start': strip(n['text'])[:60], 'reason': why}); c['moves'] += 1
# balance after moves
CALL = re.compile(r'[\(\[]\s*(\*+|[a-z†])\s*[\)\]]')
cnt = {u['id']: [len(CALL.findall(u['text'])), len([n for n in u.get('notes', []) if n['mark'] != 'cont'])] for u in U}
for m in moves: cnt[m['from']][1] -= 1; cnt[m['to']][1] += 1
still = [(k, v) for k, v in cnt.items() if v[0] != v[1]]
json.dump({'format': 'nle-corrections/1', 'edition': 'vattel-1773',
           'description': 'Corrections to the working edition (data.json), applied by the converter (tools/nle.py apply_note_moves) and by tools/check_edition.js. '
                          'noteMoves: footnotes the working edition attached to the neighbouring section on a shared page. Each names the note by its section and '
                          'index in data.json (cont: continuation notes that go with it), its mark, and the section whose call it answers. Read from the MDZ scans '
                          '(bsb10725331, bsb10725332) by Claude Sonnet, one reader per run of sections; only answers the reader marked certain and whose two '
                          'sections share a printed page are applied.',
           'noteMoves': moves}, open(out, 'w'), ensure_ascii=False, indent=1)
print(dict(c), 'skipped', len(skipped))
for s in skipped: print('  skip', s)
print('units with calls != notes after moves:', len(still))
for s in still: print('  ', s)
