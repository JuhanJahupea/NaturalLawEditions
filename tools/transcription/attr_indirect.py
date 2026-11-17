# attr_indirect.py <out>: reuse rows (not citation, commonplace or already attributed) whose unit designates a source without
# naming it: "le savant traducteur", "l'auteur de l'Esprit des loix", "un illustre auteur", "ce grand homme" … For the
# attribution check (ATTRIBUTION_PROMPT.md, with the indirect rule).
import os, sys, json, re, glob, unicodedata, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
def fold(s):
    s = unicodedata.normalize('NFD', s.replace('ſ', 's')); return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
PAT = re.compile(r"\b(?:un|le|ce|cet|notre|un des|l'un des)\s+(?:plus\s+)?(?:savant|scavant|illustre|celebre|habile|judicieux|grand homme|docte|moderne)\b"
                 r"|\b(?:les|des|nos|ces|quelques)\s+(?:plus\s+)?(?:savans|scavans|illustres|celebres|habiles)\s+(?:auteurs|ecrivains|jurisconsultes|hommes)\b"
                 r"|\btraducteur\b|\bcommentateur\b|\bannotateur\b|\bl'auteur\s+(?:de|du|des)\s+(?!la nature|l'univers|notre|toutes|tout|ces|ce |cette)"
                 r"|\bcet auteur\b|\bnotre auteur\b|\bun auteur\b|\bun ecrivain\b|\bun jurisconsulte\b|\bun philosophe\b|\besprit des loi|\btheorie des sentimens|\bspectateur\b")
def strip(h): return re.sub(r'<[^>]+>', '', h)
done = set()
for ed in ('vattel-1773', 'burlamaqui-1747'):
    for a in json.load(open('%s/editions/%s/passes/attributions.json' % (R, ed)))['attributions']: done.add((ed, a['text'], a['unit'], a['page'], a['passage']))
out = []; c = collections.Counter(); hits = collections.Counter()
for ed in ('vattel-1773', 'burlamaqui-1747'):
    U = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
    for f in sorted(glob.glob('%s/reuse/%s__*.json' % (R, ed))):
        T = json.load(open(f))
        for r in T['rows']:
            if r['label'] in ('commonplace', 'citation') or 'attributed' in r: continue
            if (ed, T['to'], r['unit'], r['page'], r['passage']) in done: continue
            u = U[r['unit']]; full = fold(' '.join([u.get('margin', ''), strip(u['text'])] + [strip(n['text']) for n in u.get('notes', [])]))
            m = PAT.findall(full)
            if m: out.append({'ed': ed, 'to': T['to'], 'id': r['id'], 'unit': r['unit']}); c[ed] += 1; hits.update(x.strip() for x in m)
json.dump(out, open(sys.argv[1], 'w'))
print(dict(c)); print(hits.most_common(25))
