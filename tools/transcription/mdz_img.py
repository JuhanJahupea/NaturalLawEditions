# mdz_img.py <bsb id> <first> <last> <out dir> [width]: MDZ IIIF page images (canvas numbers) as grayscale-free JPEGs, p<NNNN>.jpg.
import sys, os, urllib.request, concurrent.futures as cf
bid, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; w = sys.argv[5] if len(sys.argv) > 5 else '1300'
os.makedirs(out, exist_ok=True)
def get(i):
    p = os.path.join(out, 'p%04d.jpg' % i)
    if os.path.exists(p) and os.path.getsize(p) > 5000: return
    for t in range(4):
        try:
            data = urllib.request.urlopen('https://api.digitale-sammlungen.de/iiif/image/v2/%s_%05d/full/%s,/0/default.jpg' % (bid, i, w), timeout=90).read()
            open(p, 'wb').write(data); return
        except Exception as e:
            if t == 3: print('fail', i, e)
with cf.ThreadPoolExecutor(6) as ex: list(ex.map(get, range(a, b + 1)))
print(len([f for f in os.listdir(out) if f.endswith('.jpg')]))
