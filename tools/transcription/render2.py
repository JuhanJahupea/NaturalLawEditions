# render2.py <pdf> <outdir>: each page trimmed to its printed area and scaled to fit 1300 x 1560 px (grayscale JPEG),
# plus clips.json with the page-coordinate clip of each image, for crop2.py.
import sys, os, json
import pymupdf as fitz
pdf, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True); d = fitz.open(pdf); clips = {}
cj = os.path.join(out, 'clips.json')
if os.path.exists(cj): clips = json.load(open(cj))
for i, pg in enumerate(d, 1):
    p = os.path.join(out, 'p%04d.jpg' % i)
    if os.path.exists(p) and str(i) in clips: continue
    r = pg.rect; z = 400 / r.width
    pm = pg.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csGRAY)
    w, h, s = pm.width, pm.height, pm.samples
    cols = [0] * w; rows = [0] * h
    for y in range(h):
        row = s[y * pm.stride: y * pm.stride + w]
        for x, v in enumerate(row):
            if v < 150: cols[x] += 1; rows[y] += 1
    xs = [x for x in range(w) if cols[x] > 2]; ys = [y for y in range(h) if rows[y] > 2]
    if xs and ys:
        pad = 0.015 * w
        x0, x1, y0, y1 = max(0, xs[0] - pad), min(w, xs[-1] + 1 + pad), max(0, ys[0] - pad), min(h, ys[-1] + 1 + pad)
        clip = fitz.Rect(r.x0 + x0 / z, r.y0 + y0 / z, r.x0 + x1 / z, r.y0 + y1 / z)
    else:
        clip = r
    sc = min(1300 / clip.width, 1560 / clip.height)
    pg.get_pixmap(matrix=fitz.Matrix(sc, sc), clip=clip, colorspace=fitz.csGRAY).save(p, jpg_quality=82)
    clips[str(i)] = [clip.x0, clip.y0, clip.x1, clip.y1]
    if i % 50 == 0: json.dump(clips, open(cj, 'w'))
json.dump(clips, open(cj, 'w'))
print(pdf, d.page_count)
