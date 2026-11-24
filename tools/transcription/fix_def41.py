# fix_def41.py: two systematic corrections of the DEF41 page files, logged to <WORK>/tr/DEF41_fixes.json.
#  - a last body line that repeats the catchword is dropped (the readers often wrote the catchword twice);
#  - curly apostrophes become straight ones, as in the rest of the transcription.
import os, re, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
def norm(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()
log = {'catch_dropped': [], 'apostrophes': []}
for f in sorted(glob.glob(os.path.join(WORK, 'tr', 'DEF41', 's*.json'))):
    d = json.load(open(f)); ch = False
    lines = d.get('body', '').rstrip('\n').split('\n')
    c = norm(d.get('catch', ''))
    if c and lines and norm(lines[-1]) == c and len(lines) > 1:
        log['catch_dropped'].append({'scan': d['scan'], 'line': lines[-1]}); lines = lines[:-1]; d['body'] = '\n'.join(lines); ch = True
    for k in ('body', 'head', 'catch', 'catch_notes'):
        if '’' in d.get(k, ''): d[k] = d[k].replace('’', "'"); ch = True; log['apostrophes'].append({'scan': d['scan'], 'zone': k})
    for n in d.get('notes', []):
        if isinstance(n, dict) and '’' in n.get('text', ''): n['text'] = n['text'].replace('’', "'"); ch = True; log['apostrophes'].append({'scan': d['scan'], 'zone': 'notes'})
    if ch: json.dump(d, open(f, 'w'), ensure_ascii=False)
json.dump(log, open(os.path.join(WORK, 'tr', 'DEF41_fixes.json'), 'w'), ensure_ascii=False, indent=1)
print('catchword lines dropped:', len(log['catch_dropped']), '| zones with curly apostrophes:', len(log['apostrophes']))
