# shared.py: runs of words an edition unit shares with a source part, in order (accents folded, long s as s).
# runs(a_tokens, b_index) -> list of (start in a, length, part key). A run counts when it has >= N words
# and at least C words of 4+ letters, so stock strings of particles do not count.
import re, unicodedata
N, C = 5, 3
W = re.compile(r"[a-z0-9]+")

def fold(s):
    s = s.replace('ſ', 's').replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('Œ', 'oe')
    s = re.sub(r'<[^>]+>', ' ', s)
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'-\s*\n\s*', '', s)  # line-end hyphen
    return s

def toks(s):
    return [(m.group(), m.start()) for m in W.finditer(fold(s))]

def index(parts):
    """parts: list of (key, text). Returns {5-gram: [(key, pos)]} and token lists."""
    idx, T = {}, {}
    for key, text in parts:
        t = [w for w, _ in toks(text)]; T[key] = t
        for i in range(len(t) - N + 1):
            idx.setdefault(tuple(t[i:i + N]), []).append((key, i))
    return idx, T

def runs(a, idx, T):
    """a: token list of the unit. Maximal runs, one per (part, a-start)."""
    out, seen = [], set()
    for i in range(len(a) - N + 1):
        for key, j in idx.get(tuple(a[i:i + N]), ()):
            if (key, i - j) in seen and i > 0 and j > 0 and a[i - 1] == T[key][j - 1]: continue
            L = N
            while i + L < len(a) and j + L < len(T[key]) and a[i + L] == T[key][j + L]: L += 1
            seen.add((key, i - j))
            run = a[i:i + L]
            if sum(len(w) >= 4 for w in run) >= C: out.append((i, L, key, j))
    best = {}
    for i, L, key, j in out:
        if (key, i - j) not in best or best[(key, i - j)][1] < L: best[(key, i - j)] = (i, L, key, j)
    return sorted(best.values())
