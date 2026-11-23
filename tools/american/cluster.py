import os
import json,collections
d=json.load(open('retr.json'));V=d['V'];W=d['W'];res=d['res']
# group by (doc, unit), merge windows whose char spans overlap or are within 300 chars
g=collections.defaultdict(list)
for r in res: g[(W[r['w']]['doc'],V[r['v']]['unit'])].append(r)
items=[]
for (doc,u),rs in g.items():
    rs.sort(key=lambda r:W[r['w']]['c0'])
    cur=None
    for r in rs:
        w=W[r['w']]
        if cur and w['c0']<=cur['c1']+300:
            cur['c1']=max(cur['c1'],w['c1']);cur['z']=max(cur['z'],r['z']);cur['sh']=max(cur['sh'],r['sh']);cur['cos']=max(cur['cos'],r['cos']);cur['n']+=1;cur['vs'].add(r['v'])
        else:
            cur={'doc':doc,'unit':u,'c0':w['c0'],'c1':w['c1'],'z':r['z'],'sh':r['sh'],'cos':r['cos'],'n':1,'vs':{r['v']}};items.append(cur)
for it in items: it['vs']=sorted(it['vs'])
print('items',len(items))
C=collections.Counter(it['doc'] for it in items);print(C.most_common())
import numpy as np
for th in (6,8,10,12,15):print('z>=',th,sum(1 for it in items if it['z']>=th or it['sh']>=3))
json.dump(items,open('items.json','w'))
