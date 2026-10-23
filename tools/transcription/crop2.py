# crop2.py <SIGLUM> <page> <x0> <y0> <x1> <y1> [out.jpg]
# A region of a page image at high resolution. Coordinates are fractions (0-1) of the page image you were given
# (e.g. 0 0.6 0.5 1 = the lower left quarter). Prints the path of the crop; read it with the Read tool.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
import pymupdf as fitz
B = WORK + '/scans'
sig, page = sys.argv[1], int(sys.argv[2]); fx0, fy0, fx1, fy1 = map(float, sys.argv[3:7])
out = sys.argv[7] if len(sys.argv) > 7 else '%s/crops/%s_p%04d_%d_%d_%d_%d.jpg' % (B, sig, page, fx0 * 100, fy0 * 100, fx1 * 100, fy1 * 100)
os.makedirs(os.path.dirname(out), exist_ok=True)
c = json.load(open('%s/img/%s/clips.json' % (B, sig)))[str(page)]
d = fitz.open('%s/pdf/%s.pdf' % (B, sig)); pg = d[page - 1]
W, H = c[2] - c[0], c[3] - c[1]
clip = fitz.Rect(c[0] + fx0 * W, c[1] + fy0 * H, c[0] + fx1 * W, c[1] + fy1 * H)
sc = min(1560 / clip.width, 1560 / clip.height, 4 * 1300 / W)
pg.get_pixmap(matrix=fitz.Matrix(sc, sc), clip=clip, colorspace=fitz.csGRAY).save(out, jpg_quality=85)
print(out)
