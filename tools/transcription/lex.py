# Lexical tools for French text reuse: normalisation, stemmed tokens, skip-bigrams, z-scored retrieval.
import re, unicodedata, math, collections
from nltk.stem.snowball import FrenchStemmer

_st = FrenchStemmer()
STOP = set('''a au aux avec ce ces cet cette ceux celle celles celui ci comme dans de des du elle elles en est et etre eux il ils
je la le les leur leurs lui ma mais me meme mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses si son sont
sur ta te tes toi ton tu un une vos votre vous y c d j l m n s t qu ont ete fait avoit avait etoit etait sont sera seroit serait
cela ainsi aussi bien car donc dont meme plus point tout tous toute toutes tres sans sous entre lors autre autres quelque chose
peut doit cest quil quils quon dun dune'''.split())

def norm(s):
    s = s.replace('ſ', 's').replace('&', ' et ').replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'AE').replace('Œ', 'OE')
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', s)
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r"oi(t|ent|s)\b", r"ai\1", s)
    return re.sub(r'\s+', ' ', s)

_cache = {}
def stem(w):
    if w not in _cache: _cache[w] = _st.stem(w)
    return _cache[w]

def toks(s):
    return [stem(w) for w in re.findall(r'[a-z]{2,}', norm(s)) if w not in STOP]

def skipbigrams(t, win=4):
    out = set()
    for i, a in enumerate(t):
        for b in t[i + 1:i + 1 + win]: out.add((a, b))
    return out

def zscores(vals):
    n = len(vals)
    if n < 2: return [0.0] * n
    m = sum(vals) / n; sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1)) or 1.0
    return [(v - m) / sd for v in vals]

class Index:
    """Pages of one source: skip-bigram sets and tf-idf vectors."""
    def __init__(self, pages):  # pages: [(page_id, text)]
        self.ids = [p for p, _ in pages]
        self.T = [toks(t) for _, t in pages]
        self.SB = [skipbigrams(t) for t in self.T]
        df = collections.Counter(w for t in self.T for w in set(t)); N = len(self.T)
        self.idf = {w: math.log(N / (1 + c)) + 1 for w, c in df.items()}
        self.V = [self.vec(t) for t in self.T]
    def vec(self, t):
        c = collections.Counter(t); v = {w: n * self.idf.get(w, 1.0) for w, n in c.items()}
        nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / nrm for w, x in v.items()}
    def score(self, text):
        t = toks(text); sb = skipbigrams(t); v = self.vec(t)
        sk = [len(sb & s) / max(1, min(len(sb), len(s))) for s in self.SB]
        tf = [sum(x * V.get(w, 0) for w, x in v.items()) for V in self.V]
        zs, zt = zscores(sk), zscores(tf)
        return [(self.ids[i], zs[i], zt[i], (zs[i] + zt[i]) / 2) for i in range(len(self.ids))]
