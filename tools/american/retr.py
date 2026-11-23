import re,json,glob,os,collections,numpy as np
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
ps=PorterStemmer();_c={}
def stem(w):
    if w not in _c:_c[w]=ps.stem(w)
    return _c[w]
STOP=set("the of and to a in that is it be as by for or which this with not their they his are on an have he from but all its so may at no we our if any them can than when been were has such those these shall should would one more there what must who will other into only itself same him then upon itself nor do does".split())
def toks(t): return [(m.group(0).lower(),m.start(),m.end()) for m in re.finditer(r"[A-Za-z]+",t)]
# Vattel windows: sentence windows within each unit
en=json.load(open(R+'editions/vattel-1773/layers/english.json'))['units']
V=[]
for u,x in en.items():
    s=x['sents'];i=0
    while i<len(s):
        j=i;n=0;buf=[]
        while j<len(s) and (n<60 or j==i):
            buf.append(s[j]);n+=len(s[j].split());j+=1
        V.append({'unit':u,'s0':i,'s1':j,'text':' '.join(buf)})
        if j>=len(s):break
        i=max(i+1,j-1)
print('vattel windows',len(V))
# corpus windows
W=[]
for p in sorted(glob.glob('norm/*.txt')):
    doc=os.path.basename(p)[:-4];t=open(p).read();tk=toks(t)
    for a in range(0,max(1,len(tk)-20),40):
        b=min(len(tk),a+90)
        W.append({'doc':doc,'c0':tk[a][1],'c1':tk[b-1][2],'text':t[tk[a][1]:tk[b-1][2]]})
print('corpus windows',len(W))
def an(t): return [stem(w) for w,_,_ in toks(t) if w not in STOP and len(w)>2]
vec=TfidfVectorizer(analyzer=lambda t:(lambda a:a+[a[i]+' '+a[i+1] for i in range(len(a)-1)])(an(t)),sublinear_tf=True,min_df=2,max_df=0.05)
vec.fit([v['text'] for v in V]+[w['text'] for w in W[::5]])
XV=vec.transform([v['text'] for v in V]);XW=vec.transform([w['text'] for w in W])
# shared word 5-grams (unstemmed, lowercase), rare in Vattel
def grams(t,n=5):
    w=[x for x,_,_ in toks(t)]
    return {' '.join(w[i:i+n]) for i in range(len(w)-n+1)}
gV=collections.defaultdict(set)
for i,v in enumerate(V):
    for g in grams(v['text']): gV[g].add(i)
gW=collections.Counter()
for w in W:
    for g in grams(w['text']): gW[g]+=1
res=[]
B=2000
XVt=XV.T.tocsc()
for a in range(0,len(W),B):
    S=(XW[a:a+B]@XVt).toarray()
    mu=S.mean(1,keepdims=True);sd=S.std(1,keepdims=True)+1e-9;Z=(S-mu)/sd
    for r in range(S.shape[0]):
        i=a+r;top=np.argsort(-S[r])[:3]
        sh=collections.Counter()
        for g in grams(W[i]['text']):
            if g in gV and len(gV[g])<=3 and gW[g]<=6:
                for j in gV[g]: sh[j]+=1
        cand=set(int(j) for j in top if Z[r,j]>=6 and S[r,j]>=0.12)|{j for j,c in sh.items() if c>=2}
        for j in cand:
            res.append({'w':i,'v':int(j),'cos':round(float(S[r,j]),3),'z':round(float(Z[r,j]),2),'sh':sh.get(j,0)})
json.dump({'V':V,'W':[{k:w[k] for k in ('doc','c0','c1')} for w in W],'res':res},open('retr.json','w'))
print('pairs',len(res))
