# qc_wolff.py <pages.json> <drive text json>: each transcribed page against the Google Books OCR layer of the same PDF page
# (Drive's text of the PDF, "**Page N**" blocks). 8-letter sequences of the main text, accents folded, long s and f as one letter
# (the OCR reads long s as f), u/v and i/j as one letter. Drive gives the text of the first pages only; the last one it gives is cut.
import sys, json, re, unicodedata, statistics
P = json.load(open(sys.argv[1])); P = P['pages'] if isinstance(P, dict) else P
c = json.load(open(sys.argv[2]))['fileContent']
parts = re.split(r'\[\*\*Page (\d+)\*\*\]\(\)', c)
ocr = {int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)}
ocr.pop(max(ocr))  # Drive's text breaks off inside its last page
def norm(s):
    s = re.sub(r'<[^>]+>|<<[^>]*>>', ' ', s).replace('ſ', 's').replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('Œ', 'oe')
    s = unicodedata.normalize('NFKD', s.lower()); s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r'-\s*\n\s*', '', s); s = re.sub(r'[^a-z]', '', s)
    return s.replace('f', 's').replace('v', 'u').replace('j', 'i')
def sh(s, n=8): return {s[i:i + n] for i in range(len(s) - n + 1)}
out = []
for p in P:
    if p['scan'] not in ocr: continue
    t = sh(norm(p['body'])); o = sh(norm(ocr[p['scan']]))
    if len(t) < 50: continue
    out.append((len(t & o) / len(t), p['scan']))
out.sort()
print(len(out), 'pages; median share', round(statistics.median(x for x, _ in out), 3), '; lowest', [(s, round(x, 2)) for x, s in out[:6]],
      '; pages under 0.5:', sum(1 for x, _ in out if x < 0.5))
