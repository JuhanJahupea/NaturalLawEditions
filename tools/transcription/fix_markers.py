# fix_markers.py <SIGLUM>... [--write]: find § and chapter markers the readers left out and insert them where the
# printed heading stands ("§. VII." at a line start; "CHAPITRE VII." for a chapter). Dry run unless --write.
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
from corpus import roman, unroman
B = WORK
write = '--write' in sys.argv
MK = re.compile(r'<<\s*(LIVRE|CHAP|§)\s*(\d+)\s*>>')
for vol in [a for a in sys.argv[1:] if not a.startswith('--')]:
    files = sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol)))
    pages = [(f, json.load(open(f))) for f in files]
    chap = para = 0; since = []  # pages since the last marker
    fixes = []
    for f, d in pages:
        body = d.get('body', '')
        for m in MK.finditer(body):
            kind, n = m.group(1), int(m.group(2))
            if kind == 'CHAP':
                for k in range(chap + 1, n) if chap and n > chap + 1 else []:
                    fixes.append(('CHAP', k, since + [(f, d)]))
                chap, para = n, 0
            elif kind == '§':
                for k in range(para + 1, n) if n > para + 1 else []:
                    fixes.append(('§', k, since + [(f, d)]))
                para = max(para, n)
            elif kind == 'LIVRE': chap = para = 0
            since = []
        since.append((f, d))
    done = set()
    for kind, k, cands in fixes:
        pat = re.compile(r'^\s*(?:<i>)?§\.?\s*%s\s*\.' % roman(k)) if kind == '§' else re.compile(r'^\s*CHAPITRE\s+%s\b' % roman(k))
        hit = None
        for f, d in cands:
            lines = d['body'].split('\n')
            for i, l in enumerate(lines):
                if pat.match(l) and not (i and MK.fullmatch(lines[i - 1].strip() or 'x')):
                    hit = (f, d, i); break
            if hit: break
        if not hit: print(vol, kind, k, 'not found near', os.path.basename(cands[-1][0])); continue
        f, d, i = hit
        print(vol, kind, k, '->', os.path.basename(f), 'line', i, repr(d['body'].split('\n')[i][:40]))
        if write and (f, i) not in done:
            lines = d['body'].split('\n'); lines.insert(i, '<<%s %d>>' % (kind, k)); d['body'] = '\n'.join(lines)
            json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1); done.add((f, i))
