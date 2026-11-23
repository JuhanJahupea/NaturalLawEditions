import json,glob,re,os
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
en=json.load(open(R+'editions/vattel-1773/layers/english.json'))['units']
items={}
for f in glob.glob('jb/*.json'):
    for it in json.load(open(f))['items']: items[it['id']]=it
L=lambda s:re.sub(r'[^a-z]','',s.lower())
def probe(a,b):
    a=L(a);b=L(b)
    if len(a)<40: return a in b
    ps=[a[i:i+32] for i in (0,len(a)//2-16,len(a)-32)]
    return sum(p in b for p in ps)>=2
M=[]
for f in sorted(glob.glob('jo/*.json')):
    for m in json.load(open(f))['matches']:
        it=items[m['id']]
        m['doc']=it['doc'];m['qA']=probe(m['passage'],it['passage']);m['qV']=probe(m['vattel'],' '.join(en[m['unit']]['sents']))
        m['offset']=it['char_start']+max(0,it['passage'].find(m['passage'][:30]))
        M.append(m)
json.dump(M,open('matches.json','w'),ensure_ascii=False,indent=1)
print(len(M),'matches; quote fails:',[(m['id'],m['unit'],m['qA'],m['qV']) for m in M if not (m['qA'] and m['qV'])])
for m in sorted(M,key=lambda m:(m['doc'],m['offset'])):
    print(m['id'],m['unit'],m['label'],m['confidence'],'named' if m['named'] else '-','|',m['doc'][:18],'|',m['document'][:90],'|',m['quoted_by'][:30])
