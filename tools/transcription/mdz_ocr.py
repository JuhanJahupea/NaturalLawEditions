# mdz_ocr.py <bsb id> <n canvases> <out dir>: fetch MDZ hOCR for every canvas and save plain text per page (ocr_line order).
import sys, os, re, html, urllib.request, concurrent.futures as cf
bid, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]; os.makedirs(out, exist_ok=True)
def get(i):
    p = os.path.join(out, '%04d.txt' % i)
    if os.path.exists(p): return
    for t in range(4):
        try:
            h = urllib.request.urlopen('https://api.digitale-sammlungen.de/ocr/%s/%d' % (bid, i), timeout=60).read().decode('utf-8', 'replace'); break
        except Exception as e:
            if t == 3: print('fail', i, e); return
    lines = []
    for m in re.finditer(r"<span class=['\"]ocr_line['\"][^>]*>(.*?)</span>\s*(?=<span class=['\"]ocr_line|</p>|</div>)", h, re.S):
        w = re.sub(r'<[^>]+>', ' ', m.group(1)); lines.append(re.sub(r'\s+', ' ', html.unescape(w)).strip())
    if not lines: lines = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h)))]
    open(p, 'w').write('\n'.join(lines))
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(get, range(1, n + 1)))
print(len(os.listdir(out)))
