# qc_psr34.py [--export]: checks of the PSR34 page transcriptions (Wolff, Psychologia rationalis, 1734; scans 413-605 =
# printed pp. 395-587, Sectio II-III, §§ 480-642), and with --export the pages into
# texts/wolff-psychologia-rationalis-1734/PSR34.json (nle-transcription/1).
#  - every scan has a file; printed page = scan - 18; the § markers run 480-642, each once, in order;
#  - SECTIO and CAPUT markers; NOTA markers per page;
#  - the catchword leads into the next page;
#  - agreement with archive.org's OCR of the same page in this copy or in bub_gb_szJNAAAAMAAJ, the better of the two (words of six letters or more, long s and f as one letter, u/v and
#    i/j as one letter, accents and ligatures folded).
import sys, os, re, json, glob, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
FIRST, LAST, OFF = 413, 605, 18
ITEM = 'bub_gb_vMM9AAAAcAAJ'
P = {}
for s in range(FIRST, LAST + 1):
    f = os.path.join(WORK, 'tr', 'PSR34', 's%04d.json' % s)
    if not os.path.exists(f): print('missing scan', s); continue
    try: P[s] = json.load(open(f))
    except Exception as e: print('bad json', s, e)
def fold(t):
    t = re.sub(r'<[^>]+>', '', t).replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('ſ', 's')
    t = unicodedata.normalize('NFD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    return t.replace('s', 'f').replace('v', 'u').replace('j', 'i')
OCR = {}                                   # the OCR of this copy (leaf = scan - 1) and of bub_gb_szJNAAAAMAAJ (leaf = page + 11)
of = os.path.join(WORK, 'def41', 'src', 'pages', ITEM + '.json')
o2 = os.path.join(WORK, 'def41', 'src', 'pages', 'bub_gb_szJNAAAAMAAJ.json')
if os.path.exists(of):
    A = json.load(open(of)); B2 = json.load(open(o2)) if os.path.exists(o2) else []
    for s in range(FIRST, LAST + 1):
        OCR[s] = [A[s - 1]['text']] + ([B2[s - OFF + 11]['text']] if B2 else [])
secs, low = [], []
for s, d in sorted(P.items()):
    if str(d.get('page', '')) != str(s - OFF): print('page number', s, repr(d.get('page')), 'expected', s - OFF)
    body = d.get('body', '')
    for m in re.finditer(r'<<(SECTIO|CAPUT|§) ?([^>]*)>>', body):
        if m.group(1) == '§': secs.append((int(re.sub(r'\D', '', m.group(2)) or 0), s))
        else: print('heading', s, m.group(0))
    if OCR.get(s):
        ws = set(re.findall(r'[a-z]{6,}', fold(body)))
        os_ = [re.sub(r'\s+', ' ', fold(t)) for t in OCR[s]]
        if ws:
            a = max(sum(1 for w in ws if w in o) / len(ws) for o in os_)
            if a < 0.6: low.append((s, round(a, 2)))
nums = [n for n, _ in secs]
exp = list(range(480, 643))
if nums != exp:
    print('§ sequence differs:', 'missing', sorted(set(exp) - set(nums)), 'extra', [n for n in nums if nums.count(n) > 1 or n not in exp])
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1] + 1: print('  break', nums[i - 1], '->', nums[i], 'at scan', secs[i][1])
else: print('§ markers 480-642, each once, in order')
print('NOTA markers', sum(d.get('body', '').count('<<NOTA>>') for d in P.values()))
for s in sorted(P):
    c = (P[s].get('catch') or '').strip()
    if c and s + 1 in P:
        first = re.sub(r'<<[^>]*>>|<[^>]+>', '', P[s + 1].get('body', ''))
        a, b = re.sub(r'[^a-z0-9]', '', fold(c)), re.sub(r'[^a-z0-9]', '', fold(first))
        if a and not b.startswith(a[:5]):
            print('catchword', s, repr(c), 'next begins', repr(' '.join(first[:3])))
print('pages below 60% OCR agreement:', low)
if '--export' in sys.argv:
    KEYS = ['scan', 'kind', 'page', 'head', 'margin', 'body', 'notes', 'catch', 'sig', 'notes_scan']
    pages = []
    for s, d in sorted(P.items()):
        p = {k: d.get(k, [] if k in ('margin', 'notes') else '') for k in KEYS}; p['scan'] = s
        p['margin'] = [m if isinstance(m, dict) else {'para': '', 'text': str(m)} for m in p['margin']]
        p['notes'] = [n if isinstance(n, dict) else {'mark': '', 'text': str(n)} for n in p['notes']]
        pages.append(p)
    out = {'format': 'nle-transcription/1', 'text': 'wolff-psychologia-rationalis-1734', 'volume': 'PSR34',
           'scan': {'source': 'archive.org', 'item': ITEM, 'url': 'https://archive.org/details/' + ITEM,
                    'pages': len(pages), 'note': 'scan numbers are the PDF pages of the item; printed page = scan - 18'},
           'pages': pages}
    d = os.path.join(ROOT, 'texts', 'wolff-psychologia-rationalis-1734'); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'PSR34.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
    print('exported', len(pages), 'pages')
