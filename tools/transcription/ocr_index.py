# ocr_index.py: archive.org's OCR of a volume (hOCR page index and search text) and the leaf offset between the OCR
# and the scans. The OCR can hold leaves the scans lack (a colour card first): ocr page = scan - 1 + offset.
import sys, os, json, gzip, glob, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
B = WORK
def fold(s):
    s = re.sub(r'<[^<>\n]{0,20}>|\[[^\[\]\n]{0,40}\]', ' ', s); out = []
    for ch in s.lower():
        c = unicodedata.normalize('NFD', ch)[0]
        if c in 'ſf': c = 's'
        out.append(c if 'a' <= c <= 'z' else ' ')
    return ''.join(out)
def words(s): return {w for w in fold(s).split() if len(w) >= 5}
def load(vol):
    """(page texts by OCR index, offset)."""
    pi = json.loads(gzip.open('%s/scans/ocr/%s_hocr_pageindex.json.gz' % (B, vol)).read())
    tx = gzip.open('%s/scans/ocr/%s_hocr_searchtext.txt.gz' % (B, vol)).read().decode('utf-8')
    pages = [tx[p[0]:p[1]] for p in pi]
    files = sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol)))
    sample = [json.load(open(f)) for f in files[len(files) // 3::max(1, len(files) // 12)]][:8]
    def fit(off):
        sc = []
        for d in sample:
            g = words(d.get('body', '')); i = d['scan'] - 1 + off
            if g and 0 <= i < len(pages): sc.append(len(g & words(pages[i])) / len(g))
        return sorted(sc)[len(sc) // 2] if sc else 0
    return pages, max(range(-3, 4), key=fit)
