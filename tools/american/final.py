import os
import json,re
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
V={r['key']:r for r in json.load(open('verified.json'))}
DOCS={
 'thacher-1764':('Oxenbridge Thacher','The Sentiments of a British American (Boston, 1764)','1764'),
 'otis-1764':('James Otis','The Rights of the British Colonies Asserted and Proved (Boston, 1764): the memorial of the House and its notes','1764'),
 'jadams-1765':('John Adams','Diary, 27 December 1765','1765-12-27'),
 'bland-1766':('Richard Bland','An Inquiry into the Rights of the British Colonies (Williamsburg, 1766)','1766'),
 'house-1768a':('Massachusetts House of Representatives (Samuel Adams)','Letter to the Earl of Shelburne, 15 January 1768','1768-01-15'),
 'house-1768b':('Massachusetts House of Representatives (Samuel Adams)','Letter to Lord Camden, 29 January 1768','1768-01-29'),
 'sadams-1771a':('Samuel Adams','"Vindex", Boston Gazette, 21 January 1771','1771-01-21'),
 'house-1771':('Massachusetts House of Representatives (Samuel Adams)','Letter to Benjamin Franklin, 29 June 1771','1771-06-29'),
 'sadams-1771b':('Samuel Adams','"Candidus", Boston Gazette, 19 August 1771','1771-08-19'),
 'sadams-1771c':('Samuel Adams','"Candidus", Boston Gazette, 14 October 1771','1771-10-14'),
 'sadams-1771d':('Samuel Adams','"Valerius Poplicola", Boston Gazette, 28 October 1771','1771-10-28'),
 'sadams-1772':('Samuel Adams','"Candidus", Boston Gazette, 27 January 1772','1772-01-27'),
 'boston-1772':('Boston town meeting (Samuel Adams)','The State of the Rights of the Colonists, 20 November 1772','1772-11-20'),
 'hutchinson-1773':('Thomas Hutchinson','Speech to the two Houses, 6 January 1773','1773-01-06'),
 'house-1773a':('Massachusetts House of Representatives','Answer to the Governor, 26 January 1773','1773-01-26'),
 'house-1773b':('Massachusetts House of Representatives','Answer to the Governor, 2 March 1773','1773-03-02'),
 'leonard-1775':('Daniel Leonard','"Massachusettensis", Massachusetts Gazette, 9 January 1775','1775-01-09'),
 'jadams-1775':('John Adams','"Novanglus" no. VII, Boston Gazette, 6 March 1775','1775-03-06')}
MAP={'V37':'thacher-1764','V17':'otis-1764','V19':'otis-1764','V18':'otis-1764','V20':'otis-1764','V09':'jadams-1765','V10':'jadams-1765','V11':'jadams-1765',
 'V00':'bland-1766','V01':'bland-1766','V04':'house-1768a','V21':'house-1768a','V22':'house-1768b','V23':'house-1768b','V24':'sadams-1771a','V25':'sadams-1771a','V26':'sadams-1771a',
 'V27':'sadams-1771c','V28':'sadams-1771d','V29':'sadams-1771d','V30':'sadams-1772','V31':'sadams-1772','V02':'boston-1772','V03':'boston-1772','V33':'boston-1772','V32':None,
 'V05':'hutchinson-1773','V06':'house-1773a','V34':'house-1773a','V07':'house-1773a','V35':'house-1773a','V08':'house-1773b','V36':'house-1773b',
 'V16':'leonard-1775','V13':'leonard-1775','V12':'jadams-1775','V14':'jadams-1775','V15':'jadams-1775'}
# for duplicated documents, which witness to keep (prefer the author's own edition)
PREF={'house-1768a':'V21','house-1773a':None,'jadams-1775':'V12','leonard-1775':'V16','boston-1772':'V33'}
REPORTED={('thacher-1764','I.24'),('otis-1764','I.210'),('otis-1764','I.34'),('otis-1764','III.201'),('jadams-1765','II.282'),('jadams-1765','II.292'),('jadams-1765','II.297'),
 ('sadams-1771d','I.220'),('sadams-1771d','I.223'),('sadams-1772','I.34'),('hutchinson-1773','I.210'),('house-1773a','I.34'),('house-1773a','II.265'),('house-1773b','I.34'),('leonard-1775','I.210'),('jadams-1775','I.210')}
rows={}
for k,v in V.items():
    d=MAP.get(k)
    if not d or v['verdict']=='reject': continue
    key=(d,v['unit'])
    r=rows.get(key)
    cand={'doc':d,'unit':v['unit'],'label':v['label'],'named':bool(v['named']),'american':v['passage'],'vattel_1797':v['vattel'],'french':v['french'],'relation':v['relation'],
          'sources':v['source'] if isinstance(v['source'],list) else [],'volume':v['doc'],'page':v['page'],'note':v['note'],'found_by':'retrieval','key':k}
    if r is None: rows[key]=cand; continue
    # keep the stronger/longer witness; merge relation info
    if len(cand['american'])>len(r['american']): cand['relation']=r['relation'] if r['relation'] in('own','other','against-wolff') and cand['relation']=='wolff' and d=='sadams-1771a' else cand['relation']; rows[key]=cand
# Vindex I.30: two stretches, one 'other', one 'own'
rows[('sadams-1771a','I.30')]['relation']='other+own'
# Candidus Oct 1771 I.34: silence clause (own) and English example (other)
rows[('sadams-1771c','I.34')]['relation']='own+other'
ADD=[('house-1771','I.34','close paraphrase',False,"If ever the provincial assemblies should be voluntarily silent, on the Parliament's taking upon themselves a power thus to violate our constitutional and Charter Rights, it might be considered as an approbation of it, or at least a tacit consent","if the parliament entered into a deliberation to make so important a change, and the whole nation was voluntarily silent upon it, this would be considered as an approbation of the act of its representatives","Mais si le parlement délibéroit de faire un changement si considérable , & que la nation entiere gardât volontairement le silence , elle seroit censée approuver le fait de ses réprésentans.",'own','sadams_v2','178',"The House applies the silence clause to the provincial assemblies and concludes: 'It is therefore our duty to declare our Rights'."),
 ('sadams-1771b','I.34','close paraphrase',False,"If therefore we are voluntarily silent while the single duty on tea is continued, or do any act, however innocent, simply considered, which may be construed by the tools of administration ... as an acquiescence in the measure, we are in extreme hazard","if the parliament entered into a deliberation to make so important a change, and the whole nation was voluntarily silent upon it, this would be considered as an approbation of the act of its representatives","Mais si le parlement délibéroit de faire un changement si considérable , & que la nation entiere gardât volontairement le silence , elle seroit censée approuver le fait de ses réprésentans.",'own','sadams_v2','202',"Adams applies the silence clause to the remaining tea duty: silence would be construed as acquiescence."),
 ('house-1773a','II.265','quotation',False,"The celebrated author, whom your Excellency has quoted, tells us, that, \" neither the one or the other of the interested, or contracting powers, hath a right to interpret at pleasure.\"","Neither the one nor the other of the parties interested in the contract has a right to interpret the deed or treaty according to his own fancy.","ni l'un ni l'autre des intéressés, ou des contractans n'est en droit d'interpréter à son gré l'acte, ou le traité.",'wolff','sadams_v2','410',"The House turns the Governor's author against him: Parliament, even as a party to the charter, could not interpret it at pleasure. The wording is not the 1797 translation's.")]
for d,u,lab,named,am,ve,fr,rel,vol,pg,note in ADD:
    srcs=[{'text':'wolff-jus-gentium-1749','locus':'§ 375','label':'close paraphrase'}] if u=='II.265' else []
    rows[(d,u)]={'doc':d,'unit':u,'label':lab,'named':named,'american':am,'vattel_1797':ve,'french':fr,'relation':rel,'sources':srcs,'volume':vol,'page':pg,'note':note,'found_by':'search','key':None}
out=[]
for (d,u),r in sorted(rows.items(),key=lambda x:(DOCS[x[0][0]][2],x[0][1])):
    a,t,dt=DOCS[d]
    r.update({'author':a,'document':t,'date':dt,'in_studies':(d,u) in REPORTED})
    out.append(r)
json.dump(out,open('final.json','w'),ensure_ascii=False,indent=1)
import collections
print(len(out),'reuses in',len({r['doc'] for r in out}),'documents; new',sum(not r['in_studies'] for r in out))
print(collections.Counter(r['relation'] for r in out))
for r in out: print(r['date'],r['doc'],r['unit'],r['label'],r['relation'],'NEW' if not r['in_studies'] else '',r['volume'],r['page'])

# second step: one Boston sentence counts once (under I.1); readable editions and pages
X=json.load(open('final.json'))
X=[r for r in X if not (r['doc']=='boston-1772' and r['unit']=='Prelim.1')]
ED={'otis_rights_1764':'Otis, Rights (Boston, 1764)','thacher_sentiments_1764':'Thacher, Sentiments (Boston, 1764)','jadams_works_v2':'Works of John Adams, ed. C. F. Adams, II (1850)',
 'bland_inquiry_1766':'Bland, Inquiry (Williamsburg, 1766; repr. 1922)','bradford_speeches_1765_1775':'Bradford, Speeches of the Governors (1818)','sadams_v1':'Writings of Samuel Adams, ed. Cushing, I (1904)',
 'sadams_v2':'Writings of Samuel Adams, ed. Cushing, II (1906)','novanglus_massachusettensis_1774_1775':'Novanglus, and Massachusettensis (Boston, 1819)'}
PG={('house-1768a','I.34'):'Bradford 140; Cushing I, 158',('hutchinson-1773','I.210'):'Bradford 337',('house-1773a','I.34'):'Cushing II, 421–422; Bradford 362',('house-1773a','II.265'):'Cushing II, 410; Bradford 356',
 ('house-1773a','II.283'):'Cushing II, 411; Bradford 356',('house-1773b','I.34'):'Cushing II, 452; Bradford 395',('leonard-1775','I.210'):'1819, 170',('jadams-1775','I.210'):'1819, 80',
 ('bland-1766','I.2'):'[10]',('bland-1766','III.290'):'[27]',('otis-1764','I.210'):'106, 110',('otis-1764','I.34'):'109',('otis-1764','III.201'):'111–112'}
for r in X:
    r['edition']=ED.get(r['volume'],r['volume'])
    r['pages']=PG.get((r['doc'],r['unit'])) or ('%s, %s'%(r['edition'].split(',')[0] if 'Cushing' not in r['edition'] else 'Cushing '+r['edition'].split(', ')[-1].split(' ')[0],r['page']))
    if r['doc']=='jadams-1775': r['label']='quotes Leonard'
X.sort(key=lambda r:(r['date'],r['unit']))
json.dump(X,open('final.json','w'),ensure_ascii=False,indent=1)
