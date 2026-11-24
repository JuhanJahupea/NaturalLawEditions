# fix_psr34.py: systematic fixes of the PSR34 page transcriptions, logged to <WORK>/tr/PSR34_fixes.json.
#  - a last body line that repeats the catchword is dropped (the readers often wrote the catchword twice);
#  - catchwords misread by the first readers, checked against the images: scan 427 "§. 492." (read "§. 491."),
#    511 "nim-" (read "anim-"), 575 "nimæ" (read "animæ").
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
CATCH = {427: '§. 492.', 511: 'nim-', 575: 'nimæ'}
log = []
for f in sorted(glob.glob(os.path.join(WORK, 'tr', 'PSR34', 's*.json'))):
    d = json.load(open(f)); s = int(d['scan']); ch = False
    if s in CATCH and d.get('catch') != CATCH[s]:
        log.append({'scan': s, 'fix': 'catch', 'old': d.get('catch'), 'new': CATCH[s]}); d['catch'] = CATCH[s]; ch = True
    c = (d.get('catch') or '').strip()
    lines = d['body'].rstrip().split('\n')
    strip = lambda t: re.sub(r'<[^>]+>', '', t).strip()
    if c and len(lines) > 1 and strip(lines[-1]) in (strip(c), strip(c).rstrip('-')):
        log.append({'scan': s, 'fix': 'catchword line dropped', 'old': lines[-1]})
        d['body'] = '\n'.join(lines[:-1]); ch = True
    if ch: json.dump(d, open(f, 'w'), ensure_ascii=False)
json.dump(log, open(os.path.join(WORK, 'tr', 'PSR34_fixes.json'), 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(x['fix'] for x in log))
