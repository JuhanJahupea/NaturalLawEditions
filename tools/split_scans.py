# Render the pages of a scanned volume for vision transcription and pack them in small zips.
# Usage: python split_scans.py <volume.pdf> <siglum> <output folder> [--width 1300] [--per-zip 20]
# Needs PyMuPDF (pip install pymupdf). Writes <siglum>_p0001-0020.zip ... and <siglum>_pages.json.
# Each zip holds p<NNNN>.jpg, numbered by PDF page (the page ids of the reuse tables: GRO24T1.p214 is PDF page 214).
# Pages are grayscale JPEG, 1300 px wide, the reading size of the Vattel and Burlamaqui transcriptions.
import argparse, io, json, os, zipfile
try:
    import pymupdf as fitz
except ImportError:
    import fitz

ap = argparse.ArgumentParser()
ap.add_argument('pdf'); ap.add_argument('siglum'); ap.add_argument('out')
ap.add_argument('--width', type=int, default=1300); ap.add_argument('--per-zip', type=int, default=20)
ap.add_argument('--quality', type=int, default=75)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
doc = fitz.open(a.pdf); n = doc.page_count; index = []
for start in range(1, n + 1, a.per_zip):
    end = min(n, start + a.per_zip - 1)
    name = '%s_p%04d-%04d.zip' % (a.siglum, start, end)
    with zipfile.ZipFile(os.path.join(a.out, name), 'w', zipfile.ZIP_STORED) as z:
        for p in range(start, end + 1):
            page = doc[p - 1]
            zoom = a.width / page.rect.width
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), colorspace=fitz.csGRAY)
            z.writestr('p%04d.jpg' % p, pix.tobytes('jpg', jpg_quality=a.quality))
    size = os.path.getsize(os.path.join(a.out, name))
    index.append({'zip': name, 'first': start, 'last': end, 'bytes': size})
    print(name, size)
json.dump({'pdf': os.path.basename(a.pdf), 'siglum': a.siglum, 'pages': n, 'width': a.width, 'zips': index},
          open(os.path.join(a.out, a.siglum + '_pages.json'), 'w'), indent=1)
big = [z for z in index if z['bytes'] > 5_000_000]
print('pages', n, 'zips', len(index), 'over 5 MB:', len(big))
