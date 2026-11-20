# mdz_crop.py <siglum> <canvas> <x0> <y0> <x1> <y1>: a full-resolution crop of an MDZ page (fractions 0-1); prints its path.
import sys, os, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
B = WORK
SIG = {'PPU1': 'bsb10008634', 'PPU2': 'bsb10008635'}
sig, c = sys.argv[1], int(sys.argv[2]); x0, y0, x1, y1 = map(float, sys.argv[3:7])
out = os.path.join(B, 'crops', '%s_p%04d_%d_%d_%d_%d.jpg' % (sig, c, x0 * 100, y0 * 100, x1 * 100, y1 * 100))
url = 'https://api.digitale-sammlungen.de/iiif/image/v2/%s_%05d/pct:%.2f,%.2f,%.2f,%.2f/full/0/default.jpg' % (SIG[sig], c, x0 * 100, y0 * 100, (x1 - x0) * 100, (y1 - y0) * 100)
open(out, 'wb').write(urllib.request.urlopen(url, timeout=90).read()); print(out)
