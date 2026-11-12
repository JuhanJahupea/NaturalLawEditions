# write_attr.py <dir> [date]: attribution verdicts (ATTR_PROMPT.md) -> editions/<ed>/passes/attributions.json for each edition.
# A verdict is kept when attributed is true and the cue is found in the named part of the unit (exact, or with free whitespace).
# The converters copy each kept verdict onto its reuse row as "attributed" (tools/nle.py write_tables).
import sys, os, json, re, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
from merge_find import find
R = ROOT
d = sys.argv[1]; date = sys.argv[2] if len(sys.argv) > 2 else '2026-11-12'
keys = json.load(open(d + '/keys.json'))
def strip(h): return re.sub(r'<[^>]+>', '', h)
units = {}
out = collections.defaultdict(list); c = collections.Counter(); judged = collections.Counter()
for f in sorted(glob.glob(d + '/out/a*.json')):
    for v in json.load(open(f))['items']:
        k = keys[str(v['key'])]; ed = k['ed']; judged[ed] += 1
        if not v.get('attributed'): c['not attributed'] += 1; continue
        if ed not in units: units[ed] = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
        u = units[ed][k['unit']]; part = v.get('cue_part') or 't'
        hay = u.get('margin', '') if part == 'm' else strip(u['text']) if part == 't' else strip((u.get('notes') or [{}] * 99)[int(part[1:])].get('text', '')) if re.match(r'n\d+$', part) and int(part[1:]) < len(u.get('notes', [])) else ''
        r = find(hay, v.get('cue', '')) if v.get('cue') else None
        if not r:
            # the cue may stand in another part
            for p2, h2 in [('t', strip(u['text'])), ('m', u.get('margin', ''))] + [('n%d' % i, strip(n['text'])) for i, n in enumerate(u.get('notes', []))]:
                r = find(h2, v.get('cue', '')) if v.get('cue') else None
                if r: part, hay = p2, h2; c['cue in other part'] += 1; break
        if not r and ' et ' in v.get('cue', ''):
            v['cue'] = v['cue'].replace(' et ', ' & ')  # the reader wrote out the ampersand
            for p2, h2 in [('t', strip(u['text'])), ('m', u.get('margin', ''))] + [('n%d' % i, strip(n['text'])) for i, n in enumerate(u.get('notes', []))]:
                r = find(h2, v['cue'])
                if r: part, hay = p2, h2; break
        if not r: c['cue not found'] += 1; print('cue not found', k['unit'], repr(v.get('cue'))[:80]); continue
        form = v.get('form') if v.get('form') in ('quotation', 'reference') else 'reference'
        c['attributed ' + form] += 1
        out[ed].append({'text': k['to'], 'unit': k['unit'], 'page': k['page'], 'passage': k['passage'], 'source': k['source'],
                        'form': form, 'cue': hay[r[0]:r[1]], 'cuePart': part, 'confidence': round(float(v.get('confidence', 0)), 2),
                        'reason': v.get('reason', '')})
for ed, items in out.items():
    order = {u: i for i, u in enumerate(units[ed])}
    items.sort(key=lambda a: (order[a['unit']], a['text']))
    P = {'format': 'nle-pass/1', 'edition': ed, 'date': date,
         'description': ('Reuse rows where the author names the source for the passage: in its sentence, in the sentence that introduces it, '
                         'in a note called there, or in the margin beside it. form quotation: the passage is given as the source\'s words; '
                         'reference: the source is named for the content. cue: the words that name it; cuePart: t main text, m margin, n0 … notes. '
                         'Candidates: rows (not citation or commonplace) whose unit names the source\'s author or work anywhere (%d rows). '
                         'Judged by a language model, not checked by hand. Rows labelled citation name the source by definition and are not listed.' % judged[ed]),
         'attributions': items}
    with open('%s/editions/%s/passes/attributions.json' % (R, ed), 'w', encoding='utf-8') as f:
        json.dump(P, f, ensure_ascii=False, indent=1); f.write('\n')
    print(ed, len(items), 'attributed of', judged[ed], dict(collections.Counter(a['form'] for a in items)), dict(collections.Counter(a['text'] for a in items)))
print(dict(c))
