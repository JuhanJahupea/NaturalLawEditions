import json,re,collections,os
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
items=json.load(open('items.json'));d=json.load(open('retr.json'));V=d['V']
en=json.load(open(R+'editions/vattel-1773/layers/english.json'))['units']
TITLE={l.split('\t')[0]:l.split('\t')[1].strip() for l in open('items.tsv')}
sel=[i for i in items if i['cos']>=0.15 or i['sh']>=3]
# merge into passages per doc
sel.sort(key=lambda i:(i['doc'],i['c0']))
P=[]
for it in sel:
    if P and P[-1]['doc']==it['doc'] and it['c0']<=P[-1]['c1']+200:
        p=P[-1];p['c1']=max(p['c1'],it['c1']);p['units'][it['unit']]=max(p['units'].get(it['unit'],0),it['cos'])
    else: P.append({'doc':it['doc'],'c0':it['c0'],'c1':it['c1'],'units':{it['unit']:it['cos']}})
texts={}
out=[]
for k,p in enumerate(P):
    t=texts.setdefault(p['doc'],open('norm/%s.txt'%p['doc']).read())
    a=max(0,p['c0']-700);b=min(len(t),p['c1']+700)
    us=sorted(p['units'],key=lambda u:-p['units'][u])[:4]
    out.append({'id':'P%03d'%k,'doc':p['doc'],'volume':TITLE.get(p['doc'],p['doc']),'char_start':a,
      'before':t[max(0,a-1500):a][-1500:],'passage':t[a:b],
      'candidates':[{'unit':u,'english_1797':' '.join(en[u]['sents'])[:7000]} for u in us]})
os.makedirs('jb',exist_ok=True)
B=12
for i in range(0,len(out),B):
    json.dump({'items':out[i:i+B]},open('jb/batch%02d.json'%(i//B),'w'),ensure_ascii=False,indent=0)
print('passages',len(out),'batches',(len(out)+B-1)//B, 'unit-cands',sum(len(o['candidates']) for o in out))
