# find(): place a passage in a text exactly, with free whitespace, or by the best fuzzy block (>= 0.9).
import re, difflib

def find(hay, needle):
    """[start, end) of needle in hay: exact, then with free whitespace, then the best fuzzy block (>= 0.9 of the needle)."""
    if not needle: return None
    i = hay.find(needle)
    if i >= 0: return [i, i + len(needle), 1.0]
    toks = [re.escape(t) for t in re.findall(r'\w+|[^\w\s]', needle)]
    if toks:
        m = re.search(r'\s*'.join(toks), hay)
        if m: return [m.start(), m.end(), 1.0]
    sm = difflib.SequenceMatcher(None, hay, needle, autojunk=False)
    a, b, n = sm.find_longest_match(0, len(hay), 0, len(needle))
    if n >= 0.6 * len(needle):
        s = max(0, a - b); e = min(len(hay), s + len(needle))
        r = difflib.SequenceMatcher(None, hay[s:e], needle, autojunk=False).ratio()
        if r >= 0.9: return [s, e, round(r, 3)]
    return None
