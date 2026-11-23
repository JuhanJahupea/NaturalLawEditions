import os
import json,re,collections
d=json.load(open('retr.json'));V=d['V'];W=d['W'];res=d['res']
byw=collections.defaultdict(list)
for r in res: byw[r['w']].append(r)
G=[('otis_rights_1764','authority of these legislators does not extend','I.34'),('otis_rights_1764','settles a colony there','I.210'),('otis_rights_1764','monstrous principle','III.201'),
('bradford_speeches_1765_1775','naturally becomes a part of the state, equally','I.210'),('bradford_speeches_1765_1775','does not extend so far as the fundamentals','I.34'),
('sadams_v2','tells us plainly','I.34'),('thacher_sentiments_1764','observed by Vattel','?'),('jadams_works_v2','Vattel, p. 230','?'),('sadams_v3','account a state a','Prelim.2'),
('novanglus_massachusettensis_1774_1775','best writers upon the law of nations tell','I.210'),('novanglus_massachusettensis_1774_1775','We are not told who these','I.210'),('boston_votes_1772','Locke and Vatel','?'),('sadams_v2','Lock and Vatel','?'),('sadams_v2','Mr. Vattel, law of nature','?')]
for doc,ph,u in G:
    t=open('norm/%s.txt'%doc).read()
    for m in list(re.finditer(r"\s+".join(map(re.escape,ph.split())),t))[:2]:
        ws=[i for i,w in enumerate(W) if w['doc']==doc and w['c0']-600<=m.start()<=w['c1']+600]
        hits=sorted([r for i in ws for r in byw.get(i,[])],key=lambda r:-r['z'])
        units=[(V[r['v']]['unit'],r['z'],r['sh']) for r in hits][:6]
        print(doc[:22],'|',ph[:30],'| want',u,'| got',units)
