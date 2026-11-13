# attr_cand.py <out>: reuse rows (both editions) whose unit names the source's author or work somewhere (text, notes, margin).
# These are the candidates for the attribution check. Citation rows are attributed by definition; commonplace rows are left out.
import sys, os, json, re, glob, unicodedata, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
def fold(s):
    s = unicodedata.normalize('NFD', s.replace('ſ', 's')); return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
NAMES = {
 'wolff': r'\bwolf+(?:ius|ii|io|ium)?\b|jus gentium|jus naturae|institutiones',
 'pufendorf': r'\bpuf+endorf|\bpuff?end|\bdevoirs de l.homme|droit de la nature et des gens',
 'grotius': r'\bgrot(?:ius|ii|io|\.)|droit de la guerre',
 'burlamaqui': r'\bburlamaqui',
 'bynkershoek': r'\bbyn?c?kershoe?c?k',
 'formey': r'\bformey',
 'montesquieu': r'\bmontesquieu|esprit des loi',
 'wicquefort': r'\bwic?quefort',
 'vattel': r'\bloisir|poliergie|questions de droit naturel|amusemens',
 'locke': r'\blocke?\b|entendement humain', 'malebranche': r'\bmalebranche|recherche de la verite',
 'port-royal': r'port.royal|art de penser', 'descartes': r'\bdescartes', 'pouilly': r'\bpouilly|sentimens agreables',
 'cumberland': r'\bcumberland', 'hutcheson': r'\bhutch[ei]son', 'leclerc': r'\ble clerc|\bclericus|\bclerc\b',
 'cicero': r'\bcic(?:ero|eron|\.)|\btull', 'seneca': r'\bsenec|\bseneq', 'digest': r'\bdig(?:est)?\.?|\bff\.|\bpandect|\bulpi',
 'clarke': r'\bclarke?\b', 'crousaz': r'\bcrousaz', 'spectateur': r'\bspectat', 'elemens': r'(?!x)x', 'barbeyrac': r'\bbarbeyrac',
}
def keys_of(tid, fam):
    k = [n for n in NAMES if tid.startswith(n) or tid.split('-')[0] == n]
    if tid.startswith('port-royal'): k = ['port-royal']
    if tid.startswith('leclerc'): k = ['leclerc']
    if tid.startswith('burlamaqui-elemens'): k = ['elemens']
    if 'barbeyrac' in tid: k.append('barbeyrac')
    return k
def strip(h): return re.sub(r'<[^>]+>', '', h)
out = []; stats = collections.Counter()
for ed in ('vattel-1773', 'burlamaqui-1747'):
    U = {u['id']: u for u in json.load(open(f'{R}/editions/{ed}/text.json'))['units']}
    for f in sorted(glob.glob(f'{R}/reuse/{ed}__*.json')):
        T = json.load(open(f)); tid = T['to']; ks = keys_of(tid, None)
        assert ks, tid
        rx = re.compile('|'.join('(?:%s)' % NAMES[k] for k in ks))
        for r in T['rows']:
            if r['label'] == 'commonplace': stats['commonplace'] += 1; continue
            if r['label'] == 'citation': stats['citation'] += 1; continue
            u = U[r['unit']]
            full = ' '.join([u.get('margin', ''), strip(u['text'])] + [strip(n['text']) for n in u.get('notes', [])])
            if rx.search(fold(full)): out.append({'ed': ed, 'to': tid, 'id': r['id'], 'unit': r['unit']}); stats['cand ' + ed] += 1
            else: stats['no name ' + ed] += 1
json.dump(out, open(sys.argv[1], 'w'))
print(dict(stats)); print(collections.Counter((c['ed'], c['to']) for c in out).most_common())
