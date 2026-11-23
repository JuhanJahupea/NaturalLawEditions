import json,glob,os,collections
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
M=json.load(open('matches.json'))
en=json.load(open(R+'editions/vattel-1773/layers/english.json'))['units']
T={u['id']:u for u in json.load(open(R+'editions/vattel-1773/text.json'))['units']}
rows=collections.defaultdict(list)
for f in glob.glob(R+'reuse/vattel-1773__*.json'):
    tid=os.path.basename(f)[13:-5]
    for r in json.load(open(f))['rows']:
        if r['status']!='rejected': rows[r['unit']].append({'text':tid,'locus':r['locus'],'label':r['label'],'status':r['status'],'confidence':r['confidence'],'in_note':r['inNote'],'vattel_french':r['passage'],'source':r['source'][:400]})
dv=collections.defaultdict(list)
for x in json.load(open(R+'editions/vattel-1773/layers/divergences.json'))['items']: dv[x['unit']].append({'text':x['text'],'locus':x['locus'],'severity':x.get('severity'),'comment':x['comment']})
out=[]
for k,m in enumerate(M):
    t=open('norm/%s.txt'%m['doc']).read();o=m['offset']
    u=T[m['unit']]
    out.append({'key':'V%02d'%k,'match':{x:m[x] for x in ('id','unit','passage','vattel','label','confidence','named','document','quoted_by','reason')},'doc':m['doc'],
      'context':t[max(0,o-2500):o+1500],'vattel_english':' '.join(en[m['unit']]['sents']),'vattel_french':u['text'],'vattel_french_notes':[n['text'] for n in u.get('notes',[])],
      'source_rows':rows.get(m['unit'],[]),'divergences':dv.get(m['unit'],[])})
os.makedirs('vb',exist_ok=True)
h=(len(out)+1)//2
json.dump({'items':out[:h]},open('vb/v0.json','w'),ensure_ascii=False,indent=0);json.dump({'items':out[h:]},open('vb/v1.json','w'),ensure_ascii=False,indent=0)
print(len(out),h)
