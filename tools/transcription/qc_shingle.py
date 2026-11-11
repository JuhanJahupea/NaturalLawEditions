# qc_shingle.py <SIGLUM>...: share of a page's 8-letter sequences (main text, accents folded, long s and f as one letter,
# u and v as one) found anywhere on archive.org's OCR of the same scan.
import os, json, glob, statistics, sys, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
from ocr_index import load
B = WORK
def fold(s):
    s = re.sub(r'<[^<>\n]{0,20}>|\[[^\[\]\n]{0,40}\]', '', s); out = []
    for ch in s.lower():
        c = unicodedata.normalize('NFD', ch)[0]
        if c in 'ſf': c = 's'
        if c in 'uv': c = 'u'
        if 'a' <= c <= 'z': out.append(c)
    return ''.join(out)
res = []
for vol in sys.argv[1:]:
    pages, off = load(vol)
    for f in sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol))):
        d = json.load(open(f)); s = d['scan']; mine = fold(d.get('body', ''))
        if len(mine) < 300 or not 0 <= s - 1 + off < len(pages): continue
        o = fold(pages[s - 1 + off]); O = {o[i:i + 8] for i in range(len(o) - 7)}
        M = [mine[i:i + 8] for i in range(0, len(mine) - 7, 4)]
        res.append((round(sum(m in O for m in M) / len(M), 2), vol, s))
    print(vol, 'offset', off)
res.sort()
print(len(res), 'pages; median', statistics.median(r[0] for r in res))
print('lowest', res[:15])
