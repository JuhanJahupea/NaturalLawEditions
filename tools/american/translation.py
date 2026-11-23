# translation.py <epub>: which English translation each American reuse follows. The EPUB is Google Books MRo2AQAAMAAJ
# (London, J. Newbery, 1760 and J. Coote, 1759; University of Michigan), whose OCR text it holds page by page; it is
# not kept in the repository. For each reuse, the share of its word 4-grams found anywhere in the 1760 text and in the
# section's 1797 text (the edition's English layer). Long s and f are folded on both sides. Writes en1760 and en1797
# into reports/data/vattel-american-reuse.json.
import os, re, sys, json, zipfile, html
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
z = zipfile.ZipFile(sys.argv[1])
full = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<head>.*?</head>', '', z.read(f).decode('utf-8', 'replace'), flags=re.S)))
                for f in sorted(n for n in z.namelist() if n.endswith('.xml') and 'content-' in n))
def norm(s):
    s = s.lower().replace('ſ', 's').replace('f', 's')
    s = re.sub(r'\bantient\b', 'ancient', s)
    return re.findall(r'[a-z]+', s)
grams = lambda w, n=4: {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}
G60 = grams(norm(full))
en = json.load(open(R + 'editions/vattel-1773/layers/english.json'))['units']
p = R + 'reports/data/vattel-american-reuse.json'
D = json.load(open(p))
for r in D['reuses']:
    a = grams(norm(r['american']))
    if len(a) < 4: r['en1760'] = r['en1797'] = None; continue
    r['en1760'] = round(len(a & G60) / len(a), 2)
    r['en1797'] = round(len(a & grams(norm(' '.join(en[r['unit']]['sents'])))) / len(a), 2)
D['translations'] = {'1760': 'The Law of Nations, London: J. Newbery et al., 1760 (vol. II: J. Coote, 1759); Google Books MRo2AQAAMAAJ, OCR text',
                     '1797': "The Law of Nations, London, 1797, as in the edition's English layer (ed. Kapossy and Whatmore)"}
json.dump(D, open(p, 'w'), ensure_ascii=False, indent=1)
print(sum(1 for r in D['reuses'] if r['en1760'] is not None and r['en1760'] > r['en1797'] + 0.1), 'follow 1760;',
      sum(1 for r in D['reuses'] if r['en1797'] is not None and r['en1797'] > r['en1760'] + 0.1), 'nearer 1797')
