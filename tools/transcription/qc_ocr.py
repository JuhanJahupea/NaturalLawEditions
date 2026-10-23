# qc_ocr.py <SIGLUM>...: compare each transcribed page with archive.org's OCR of the same scan.
# Score: share of the transcription's words of 5+ letters (accents folded, long s and f as one letter) found in the OCR page.
# A page transcribed from the image scores high even with OCR noise; a page written without the image scores low.
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
from ocr_index import load, words
B = WORK
low = []
for vol in sys.argv[1:]:
    pages, off = load(vol); scores = []
    for f in sorted(glob.glob('%s/tr/%s/s*.json' % (B, vol))):
        d = json.load(open(f)); s = d['scan']
        mine = d.get('body', '') + ' '.join(n['text'] for n in d.get('notes', [])) + ' '.join(m['text'] if isinstance(m, dict) else str(m) for m in d.get('margin', []))
        g = words(mine)
        if len(g) < 30 or not 0 <= s - 1 + off < len(pages): continue
        sc = len(g & words(pages[s - 1 + off])) / len(g)
        scores.append((sc, s))
        if sc < 0.6: low.append((vol, s, round(sc, 2)))
    scores.sort()
    print(vol, 'offset', off, ';', len(scores), 'pages; median', round(scores[len(scores) // 2][0], 2), '; lowest', [(s, round(x, 2)) for x, s in scores[:8]])
print('below 0.6:', len(low))
