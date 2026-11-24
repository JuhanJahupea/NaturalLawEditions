# fix_psr34.py: systematic fixes of the PSR34 page transcriptions, logged to <WORK>/tr/PSR34_fixes.json.
#  - a last body line that repeats the catchword is dropped (the readers often wrote the catchword twice);
#  - catchwords misread by the first readers, checked against the images: scan 427 "§. 492." (read "§. 491."),
#    511 "nim-" (read "anim-"), 575 "nimæ" (read "animæ");
#  - a double s is printed as round s and long s ("esſe", "necesſe", "posſit"), never as two long s; the first
#    readers mostly wrote "ſſ". The second readers found "sſ" on every page they checked, in roman and in italic.
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
CATCH = {427: '§. 492.', 511: 'nim-', 575: 'nimæ'}
LOG = os.path.join(WORK, 'tr', 'PSR34_fixes.json')
log = json.load(open(LOG)) if os.path.exists(LOG) else []         # runs add to the log
n0 = len(log)
for f in sorted(glob.glob(os.path.join(WORK, 'tr', 'PSR34', 's*.json'))):
    d = json.load(open(f)); s = int(d['scan']); ch = False
    if s in CATCH and d.get('catch') != CATCH[s]:
        log.append({'scan': s, 'fix': 'catch', 'old': d.get('catch'), 'new': CATCH[s]}); d['catch'] = CATCH[s]; ch = True
    def ss(t): return t.replace('ſſ', 'sſ')
    n = d['body'].count('ſſ') + sum(m.get('text', '').count('ſſ') for m in d.get('margin', []) if isinstance(m, dict)) \
        + sum(x.get('text', '').count('ſſ') for x in d.get('notes', []) if isinstance(x, dict)) + (d.get('catch') or '').count('ſſ')
    if n:
        d['body'] = ss(d['body']); d['catch'] = ss(d.get('catch') or '')
        for m in d.get('margin', []):
            if isinstance(m, dict): m['text'] = ss(m.get('text', ''))
        for x in d.get('notes', []):
            if isinstance(x, dict): x['text'] = ss(x.get('text', ''))
        log.append({'scan': s, 'fix': 'ſſ to sſ', 'n': n}); ch = True
    c = (d.get('catch') or '').strip()
    lines = d['body'].rstrip().split('\n')
    strip = lambda t: re.sub(r'<[^>]+>', '', t).strip()
    if c and len(lines) > 1 and strip(lines[-1]) in (strip(c), strip(c).rstrip('-')):
        log.append({'scan': s, 'fix': 'catchword line dropped', 'old': lines[-1]})
        d['body'] = '\n'.join(lines[:-1]); ch = True
    if ch: json.dump(d, open(f, 'w'), ensure_ascii=False)
json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('this run:', Counter(x['fix'] for x in log[n0:]), sum(x.get('n', 0) for x in log[n0:]), 'double s')
