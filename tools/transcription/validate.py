# validate.py <WORK>: structure checks on the page transcriptions.
# Flags: § numbers that do not follow (within a chapter), chapters that do not follow, running heads naming another chapter,
# missing scans, pages with no body that are not marked as such.
import sys, re, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus import WORKS, B, unroman
work = sys.argv[1]
for vol in WORKS[work]['vols']:
    files = sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol)))
    if not files: continue
    scans = [int(f[-9:-5]) for f in files]
    gaps = [s for s in range(1, max(scans) + 1) if s not in scans]
    print(vol, len(files), 'files; missing scans', gaps[:40], '...' if len(gaps) > 40 else '')
    livre = chap = para = 0
    for f in files:
        d = json.load(open(f)); s = d['scan']
        for m in re.finditer(r'<<\s*(LIVRE|CHAP|§)\s*(\d+)\s*>>', d.get('body', '')):
            k, n = m.group(1), int(m.group(2))
            if k == 'LIVRE':
                if n != livre + 1: print('  s%d LIVRE %d after %d' % (s, n, livre))
                livre, chap, para = n, 0, 0
            elif k == 'CHAP':
                if n != chap + 1: print('  s%d CHAP %d after %d' % (s, n, chap))
                chap, para = n, 0
            else:
                if n != para + 1: print('  s%d § %d after %d (chap %d)' % (s, n, para, chap))
                para = n
        h = re.sub(r'</?i>', '', d.get('head', '')).upper()
        hm = re.search(r'CH(?:AP)?\.\s*([IVXL]+)', h)
        if hm and chap and unroman(hm.group(1)) != chap and d.get('kind') == 'text':
            print('  s%d head says CH. %s, state chap %d' % (s, hm.group(1), chap))
        if not d.get('body', '').strip() and d.get('kind') == 'text': print('  s%d kind text but empty body' % s)
