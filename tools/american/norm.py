# normalise OCR text: long s, f-for-s, hyphenation; write norm/<doc>.txt and a dictionary
import re,os,glob,collections,json
os.makedirs('norm',exist_ok=True)
def basic(t):
    t=t.replace('ſ','s').replace('­','')
    t=re.sub(r'(\w)[-¬]\s*\n\s*(\w)',r'\1\2',t)
    t=re.sub(r'[ \t]+',' ',t)
    return t
CUT={'sadams_v3':(0,16600),'jadams_works_v2':(0,22195),'jadams_works_v3':(22766,10**9),'jadams_works_v4':(0,12860)}
def rd(p):
    k=os.path.basename(p)[:-4];L=open(p,encoding='utf-8',errors='replace').read().split('\n')
    a,b=CUT.get(k,(0,10**9));return basic('\n'.join(L[a:b]))
docs={os.path.basename(p)[:-4]:rd(p) for p in glob.glob('raw/*.txt')}
# dictionary from clean modern-printed sources + Vattel English
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
en=json.load(open(R+'editions/vattel-1773/layers/english.json'))['units']
clean=' '.join(' '.join(u['sents']) for u in en.values())
for k in ('jcc_v1','jcc_v2','jcc_v3','jcc_v4','jcc_v5','jadams_works_v4','sadams_v1','sadams_v2','novanglus_massachusettensis_1774_1775'):
    clean+=' '+docs[k]
freq=collections.Counter(w.lower() for w in re.findall(r"[A-Za-z]+",clean))
def fix(w):
    lw=w.lower()
    if 'f' not in lw or freq.get(lw,0)>=3: return w
    idx=[i for i,c in enumerate(lw) if c=='f' and i<len(lw)-1]
    if not idx or len(idx)>4: return w
    best=(freq.get(lw,0),w)
    import itertools
    for r in range(1,len(idx)+1):
        for comb in itertools.combinations(idx,r):
            c=list(w)
            for i in comb: c[i]='s' if w[i]=='f' else 'S'
            v=''.join(c)
            if freq.get(v.lower(),0)>best[0]*3+2: best=(freq.get(v.lower(),0),v)
    return best[1]
n=0
for k,t in docs.items():
    t2=re.sub(r"[A-Za-z]+",lambda m:fix(m.group(0)),t)
    n+=sum(1 for a,b in zip(re.findall(r"[A-Za-z]+",t),re.findall(r"[A-Za-z]+",t2)) if a!=b)
    open('norm/%s.txt'%k,'w').write(t2)
print('docs',len(docs),'f->s fixes',n)
