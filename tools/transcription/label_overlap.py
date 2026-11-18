# label_overlap.py: word-sequence overlap between a row's passage and its source passage (French sources), for the label check.
import sys, os, json, re, glob, unicodedata, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
def fold(s):
    s = unicodedata.normalize('NFD', s.replace('ſ', 's').replace('&', 'et')); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    s = re.sub(r"[^a-z' ]", ' ', s).replace('y', 'i')   # old spellings: loix/lois, foy/foi
    return [w for w in re.split(r"[ ']+", s) if w]
def overlap(a, b):
    A, B = fold(a), fold(b)
    if not A or not B: return 0.0, 0.0
    m = difflib.SequenceMatcher(None, A, B, autojunk=False)
    seq = sum(x.size for x in m.get_matching_blocks()) / max(1, min(len(A), len(B)))
    longest = max((x.size for x in m.get_matching_blocks()), default=0)
    return round(seq, 3), longest
LAT = ('wolff', 'cicero', 'seneca', 'digest', 'leclerc', 'bynkershoek-quaestiones', 'hutcheson')
def rows():
    cat = json.load(open(R + '/catalogue.json'))
    for c in cat['reuse']:
        if any(c['to'].startswith(x) for x in LAT): continue
        for r in json.load(open(R + '/' + c['path']))['rows']:
            yield c['from'], c['to'], r
