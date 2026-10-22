// Shared viewer for every edition in catalogue.json: viewer/?ed=<edition id>#<unit id>
// Everything edition-specific (labels, layers, families, citations) comes from the edition's manifest.
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fill=(t,o)=>String(t??'').replace(/\{(\w+)\}/g,(m,k)=>o[k]??'');
const QS=new URLSearchParams(location.search);
let VIEW=QS.get('view')==='list'?'list':'text',LTAB='out';
let CAT=null,ED='',BASE='',M=null,V={},RU={},DIVS={},TITLES={},FAMS=[],FAMI={},FN={},st={};
const LAYS=[],LAY={},MAN={};
const SEC=[],ROWS=[],byId={},rowsBySec={},CH=[],chOf={},IN={},INROWS=[];
function save(){try{localStorage.setItem('nle:'+ED,JSON.stringify({src:st.src,pos:st.pos,layers:st.layers,widths:st.widths,fams:st.fams,chap:st.chap,sel:st.sel}))}catch(e){}}
async function getJSON(u){const r=await fetch(u);if(!r.ok)throw new Error(u+' ('+r.status+')');return r.json()}
function fail(h){$('page').innerHTML=`<div class="msg">${h}</div>`}
const edEntry=id=>CAT.editions.find(e=>e.id===id);
const prepMan=m=>(m._divs=Object.fromEntries(m.divisions.map(d=>[d.key,d])),m);

// ---------- loading ----------
async function load(){
 fail('Loading…');
 CAT=await getJSON('../catalogue.json');
 ED=QS.get('ed')||(CAT.editions.length===1?CAT.editions[0].id:'');
 edMenu();
 const E=edEntry(ED);
 if(!E){fail('Choose an edition:'+CAT.editions.map(e=>`<a href="?ed=${encodeURIComponent(e.id)}">${esc(e.author)}, ${esc(e.short||e.title)}</a>`).join(''));return false}
 BASE='../'+E.path;
 M=prepMan(await getJSON(BASE+'edition.json'));V=M.viewer||{};RU=M.reuse||{};MAN[ED]=M;
 const out=(CAT.reuse||[]).filter(t=>t.from===ED),inc=(CAT.reuse||[]).filter(t=>(t.to===ED||t.repeats===ED)&&t.from!==ED),files=M.layers.filter(l=>l.file);
 const linked=[...new Set([...inc.map(t=>t.from),...out.map(t=>t.to),...out.map(t=>t.repeats)])].filter(id=>id&&id!==ED&&edEntry(id));
 const got=await Promise.all([getJSON(BASE+M.text),...files.map(l=>getJSON(BASE+l.file)),...out.map(t=>getJSON('../'+t.path)),...inc.map(t=>getJSON('../'+t.path)),
  ...linked.map(id=>getJSON('../'+edEntry(id).path+'edition.json'))]);
 let k=1;const T=got[0],data={};files.forEach(l=>data[l.id]=got[k++]);const outT=out.map(()=>got[k++]),incT=inc.map(()=>got[k++]);linked.forEach(id=>MAN[id]=prepMan(got[k++]));
 build(T,data,outT,incT);return true}
const pageLink=p=>{const vol=(V.volumes||{})[p.vol]||{};return V.pageLink?fill(V.pageLink.url,Object.assign({},vol,p)):''};
function famColors(fams){const L=fams.map(f=>`--f${f.key}:${f.color}`).join(';'),D=fams.map(f=>`--f${f.key}:${f.dark||f.color}`).join(';');
 const s=document.createElement('style');s.textContent=`:root{${L}}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){${D}}}:root[data-theme="dark"]{${D}}`;document.head.appendChild(s)}
// a reuse row in the viewer's internal shape
function rowObj(r,tb){const o={id:r.id,sec:r.unit,fam:r.family,work:r.work,locus:r.locus,page:r.page,note:r.inNote,label:r.label,conf:r.confidence,status:r.status,vp:r.passage,sp:r.source,reason:r.reason,links:r.links||[],
  where:r.at.length?r.at[0][0]:r.where==='margin'?'m':'',step:r.step};
 if(r.french)o.fr=r.french;if(r.earliest)o.ew=r.earliest;if(r.nearer)o.near=r.nearer;if(r.quoting)o.qa=r.quoting;if(r.noteRef)o.noteref=r.noteRef;if(r.sourcePart)o.part=r.sourcePart;
 o.to=tb.to;if(r.toUnit)o.toUnit=r.toUnit;if(r.repeats)o.rep=r.repeats;return o}
function build(T,data,tables,incoming){
 TITLES=T.titles||{};DIVS=M._divs;
 const fams=RU.families||[];FAMS=fams.map(f=>[f.key,f.label]);FAMI=Object.fromEntries(fams.map(f=>[f.key,f]));FN=Object.fromEntries(FAMS);famColors(fams);
 const marks={},extra={};
 const mk=(u,kind,p)=>{const m=marks[u]=marks[u]||{reuse:{},vars:{},old:{}};return m[kind][p]=m[kind][p]||(kind==='old'?{}:[])};
 const ex=u=>extra[u]=extra[u]||{vars:[],div:[],added:new Set()};
 tables.forEach(tb=>tb.rows.forEach(r=>{const o=rowObj(r,tb);ROWS[r.id]=o;(rowsBySec[r.unit]=rowsBySec[r.unit]||[]).push(o);
  r.at.forEach(([p,a,b])=>mk(r.unit,'reuse',p).push([a,b,r.id]))}));
 // rows of other texts' tables that point into this edition
 incoming.forEach(tb=>tb.rows.forEach(r=>{
  // a row of another edition whose source is this edition, or a later text that repeats this edition's unit
  let u=tb.to===ED?r.toUnit:null,via='';
  if(!u&&r.repeats&&r.repeats.edition===ED){u=r.repeats.unit;via=textShort(tb.to)+' '+(((CAT.texts||[]).find(x=>x.id===tb.to)||{}).date||'')}
  if(!u)return;const o=Object.assign(rowObj(r,tb),{from:tb.from,toUnit:u,via});INROWS.push(o);(IN[u]=IN[u]||[]).push(o)}));
 const EN={};
 M.layers.forEach(l=>{const L=data[l.id];LAYS.push(l);if(!LAY[l.kind])LAY[l.kind]=l;
  if(l.kind==='variants')L.items.forEach(v=>{const e=ex(v.unit);
   e.vars.push({id:v.id,type:v.type,content:v.content,passage:v.passage,otherPassage:v.otherPassage,otherPages:v.otherPages,otherLink:v.otherLink,placed:v.placed});
   (v.at||[]).forEach(([p,a,b])=>mk(v.unit,'vars',p).push([a,b,v.id]));(v.wholeNotes||[]).forEach(n=>e.added.add(n));
   (v.otherReadings||[]).forEach(([p,pos,txt])=>{const o=mk(v.unit,'old',p);(o[pos]=o[pos]||[]).push(`<span class="old" data-v="${v.id}" title="${Compose.esc(l.otherTitle)}">${Compose.esc(txt)}</span>`)})});
  if(l.kind==='comments')L.items.forEach(d=>{const o={w:d.locus,wid:d.sourceId,rel:d.relation,sev:d.severity,c:d.comment,lat:d.sourcePassage,vp:d.passage,conf:d.confidence,q:d.question,link:d.links||[]};
   Object.defineProperty(o,'src',{value:textShort(d.text),enumerable:false});ex(d.unit).div.push(o)});
  if(l.kind==='translation')Object.assign(EN,L.units)});
 const order={},cited={};T.units.forEach((u,i)=>order[u.id]=i);
 T.units.forEach(u=>[...(u.xr||[]),...(u.notes||[]).flatMap(n=>n.xr||[])].forEach(x=>(cited[x[2]]=cited[x[2]]||new Set()).add(u.id)));
 const famOf=id=>ROWS[id].fam;
 T.units.forEach((u,i)=>{const e=extra[u.id]||{vars:[],div:[],added:new Set()};const c=Compose.composeUnit(u,marks[u.id]||{},famOf,V.pageBreak);
  const s={id:u.id,i,book:u.div,chap:u.chap,para:u.n,margin:u.margin||'',kind:u.kind,unnum:!!u.unnumbered,html:c.html,
   notes:c.notes.map((n,k)=>({mark:n.mark,html:n.html,added:e.added.has(k)})),pages:(u.pages||[]).map(p=>Object.assign({},p,{z:pageLink(p)})),
   vars:e.vars,citedBy:[...(cited[u.id]||[])].sort((a,b)=>order[a]-order[b])};
  if(e.div.length)s.div=e.div;
  const en=EN[u.id];if(en){s.en={s:en.sents,g:en.align,p:en.page,f:en.flags||[]};s.fs=en.fr}
  SEC.push(s);byId[s.id]=s});
 SEC.forEach(s=>{if(s.kind==='heading')return;const d=DIVS[s.book]||{};const k=d.chapters?s.book+'.'+s.chap:s.book;let c=CH[CH.length-1];if(!c||c.key!==k){c={key:k,book:s.book,chap:s.chap,secs:[]};CH.push(c)}c.secs.push(s);chOf[s.id]=c});
 st={src:true,pos:false,layers:{},fams:Object.fromEntries(FAMS.map(f=>[f[0],true])),chap:null,sel:null};
 LAYS.forEach(l=>{if(l.kind==='reuse'){if(l.default===false)st.fams[l.family]=false}else st.layers[l.id]=l.default!==false});
 try{const s=JSON.parse(localStorage.getItem('nle:'+ED)||'{}');Object.assign(st,s,{fams:Object.assign(st.fams,s.fams||{}),layers:Object.assign(st.layers,s.layers||{})})}catch(e){}
 LAYS.forEach(l=>{if(l.toggle===false)st.layers[l.id]=true})}
const layerOn=kind=>!!LAY[kind]&&!!st.layers[LAY[kind].id];
// unit labels from the id and the manifest's divisions: <div>.<n> or <div>.<chap>.<n>
function unitLabel(man,id){const p=id.split('.'),d=man&&man._divs[p[0]];return d?fill(d.unitLabel,{n:p[p.length-1],chap:p.length>2?p[1]:''}):id}
const lbl=id=>unitLabel(M,id);
// the surname of a source text's author, from the catalogue
const textShort=id=>{const t=(CAT.texts||[]).find(x=>x.id===id)||edEntry(id)||{};return t.authorShort||String(t.author||id).split(' ').pop()};
// a source text that repeats a unit of an edition: link to that unit
const repLink=r=>r.rep&&MAN[r.rep.edition]?` <span class="via" title="${esc(textShort(r.to))}'s passage repeats this unit (${r.rep.route}, ${r.rep.score})">repeats</span> ${xref(r.rep.edition,r.rep.unit)}`:'';
const edShort=id=>{const e=edEntry(id)||{};return e.authorShort||e.short||id};
const xref=(ed,u)=>`<a class="xed" href="?ed=${encodeURIComponent(ed)}#${u}" title="Open in the ${esc((edEntry(ed)||{}).short||ed)} edition">${esc(edShort(ed))} ${esc(unitLabel(MAN[ed],u))}</a>`;
// sort key from a unit id: division order, then its numbers
const unitKey=(man,id)=>{const p=id.split('.'),d=man.divisions.findIndex(x=>x.key===p[0]);return [d<0?99:d,...p.slice(1).map(Number)]};
const cmpKey=(a,b)=>{for(let i=0;i<Math.max(a.length,b.length);i++){const x=a[i]??-1,y=b[i]??-1;if(x!==y)return x<y?-1:1}return 0};
const visIn=r=>st.src&&((r.status==='match'&&r.label!=='commonplace')||st.pos);
const ctitle=c=>{const d=DIVS[c.book]||{};return d.chapters?(TITLES[c.key]||''):(d.chapterTitle||'')};
const visRow=r=>st.src&&st.fams[r.fam]&&((r.status==='match'&&r.label!=='commonplace')||st.pos);
function famDots(s){const c={};(rowsBySec[s.id]||[]).filter(visRow).forEach(r=>c[r.fam]=(c[r.fam]||0)+1);return FAMS.filter(f=>c[f[0]]).map(f=>`<span style="--c:var(--f${f[0]})" title="${esc(f[1])}: ${c[f[0]]}">${f[0]} ${c[f[0]]}</span>`).join('')}
// edition menu
function edMenu(){const s=$('edSel');s.innerHTML=CAT.editions.map(e=>`<option value="${esc(e.id)}" title="${esc(e.author+', '+e.title+', '+e.date)}"${e.id===ED?' selected':''}>${esc((e.authorShort||e.author)+' '+e.date)}</option>`).join('');const E=edEntry(ED);if(E)s.title=`${E.author}, ${E.title} (${E.date})`;
 if(!edEntry(ED))s.insertAdjacentHTML('afterbegin','<option value="" selected>Choose an edition</option>');
 $('brand').textContent=CAT.title||'Natural Law Editions';
 s.onchange=()=>{if(!s.value)return;const q=new URLSearchParams(location.search);q.set('ed',s.value);location.href='?'+q.toString()+location.hash}}
// rail
function rail(){let h='',last='';CH.forEach(c=>{if(c.book!==last){h+=`<h3>${esc(DIVS[c.book].label)}</h3>`;last=c.book}
 const t=ctitle(c);h+=`<a href="#${c.secs[0].id}" data-ch="${c.key}" data-t="${esc(t)}"><span class="n">${DIVS[c.book].chapters?'ch. '+c.chap:''}</span><span>${esc(t)}</span><span class="meter"><b></b></span></a>`});$('rail').innerHTML=h;meters()}
const secOn=s=>(rowsBySec[s.id]||[]).some(visRow)||(layerOn('comments')&&(s.div||[]).length>0)||(layerOn('variants')&&(s.vars||[]).length>0);
function meters(){const parts=['sources'].filter(()=>st.src).concat(['comments','variants'].filter(layerOn).map(k=>LAY[k].label));
 document.querySelectorAll('.rail a[data-t]').forEach(a=>{const c=CH.find(x=>x.key===a.dataset.ch);const n=c.secs.length,m=c.secs.filter(secOn).length;a.querySelector('.meter b').style.width=Math.round(100*m/n)+'%';a.title=`${a.dataset.t} · ${m} of ${n} ${V.unitsWord||'units'} with ${parts.join(', ')||'nothing'} shown by the current filters`})}
// render chapter
function cite(s){const d=DIVS[s.book]||{},pg=s.pages[0];
 return fill(d.cite,{prefix:V.citePrefix,n:s.para,chap:s.chap,unnum:s.unnum?V.citeUnnumbered:'',page:pg?fill(V.citePage,{vol:((V.volumes||{})[pg.vol]||{}).label||pg.vol,printed:pg.printed||'?'}):''})}
function secHTML(s){const vars=s.vars||[];const unplaced=vars.filter(v=>!v.placed);const LV=LAY.variants||{},LC=LAY.comments||{};
 const pages=s.pages.map(p=>`<a href="${p.z}" title="${esc(fill(V.pageLink&&V.pageLink.title,p))}">${p.vol?p.vol+' ':''}p. ${esc(p.printed||'s'+p.scan)}</a>`).join(' ');
 const cb=s.citedBy.length?`<span>cited at ${s.citedBy.map(x=>`<a href="#${x}">${lbl(x)}</a>`).join(', ')}</span>`:'';
 const vt=vars.length?`<span>${esc(LV.label)}: ${vars.length}</span>`:'';
 const inc=IN[s.id]?[...new Set(IN[s.id].filter(visIn).map(r=>r.from+'#'+r.sec))]:[];
 const ri=inc.length?`<span class="rin">reused in ${inc.map(x=>{const [e,u]=x.split('#');return xref(e,u)}).join(', ')}</span>`:'';
 const notes=s.notes.length?`<div class="notes">${s.notes.map(n=>`<div class="note${n.added?' added':''}"><span class="mk">${esc(n.mark)}</span>${n.html}</div>`).join('')}</div>`:'';
 const dvs=(s.div||[]).length?`<div class="dvs">${s.div.map((d,i)=>`<details class="dv ${d.rel}" id="dv-${s.id}-${i}"><summary><span class="wm">${esc(LC.chip)} ${esc(d.src)}</span><span class="q">${esc(d.q||'')}</span><span>${esc(d.w)}${d.rel==='partly'?' · partly':''}</span></summary><div class="dvb">${esc(d.c)}${d.lat?`<div class="q la"><small>${esc(d.src||LC.sourceTag)}</small>${esc(d.lat)}</div>`:''}${d.vp?`<div class="q fr"><small>${esc(LC.baseTag)}</small>${esc(d.vp)}</div>`:''}<div class="lk">${(d.link||[]).map(([t,u])=>`<a href="${u}">${esc(t)}</a>`).join(' ')}${d.conf?` · confidence ${Number(d.conf).toFixed(2)}`:''}</div></div></details>`).join('')}</div>`:'';
 const del=unplaced.map(v=>`<div class="del"><b style="font:12px var(--ui)">${esc(v.type)}</b> · ${esc(v.content)}${v.otherPassage?`<br>${esc(LV.otherTag)}: <i>${esc(v.otherPassage)}</i>`:''}${v.otherLink?` · <a href="${v.otherLink}">${esc(LV.otherLinkLabel)}</a>`:''}</div>`).join('');
 return `<section class="sec" id="${s.id}"><div class="sh">${s.para?`<span class="no">${esc((DIVS[s.book]||{}).unitMark||'')} ${s.para}</span>`:''}${s.unnum?`<span class="unn" title="${esc(V.unnumberedTitle)}">${esc(V.unnumberedLabel)}</span>`:''}${(s.div||[]).length?`<button class="dvc" data-dv="${s.id}" title="${esc(LC.chipTitle)}: ${s.div.length}">${esc(LC.chip)} ${s.div.length}</button>`:''}<button class="dots" data-s="${s.id}" aria-label="Show sources for ${lbl(s.id)}">${famDots(s)}</button>
 <span class="tools">${s.en?`<button data-en="${s.id}">${esc(LAY.translation.label)}</button>`:''}<button data-copy="${s.id}">Copy citation</button><button data-link="${s.id}">Link</button></span>${s.margin?`<span class="marg">${esc(s.margin)}</span>`:''}</div>
 <div class="tx">${s.html}</div>${notes}${dvs}${del}<div class="foot">${pages}${cb}${vt}${ri}</div></section>`}
function layerClasses(){const p=$('page');p.classList.toggle('chg',layerOn('variants'));p.classList.toggle('nodiv',!layerOn('comments'));p.classList.toggle('noen',!layerOn('translation'))}
function show(chKey,target,keep){const c=CH.find(x=>x.key===chKey)||CH[0];st.chap=c.key;save();
 document.querySelectorAll('.rail a').forEach(a=>a.classList.toggle('on',a.dataset.ch===c.key));
 const d=DIVS[c.book]||{};const t=d.pageTitle||ctitle(c);
 const h=`<div class="chead">${esc(d.label)}${d.chapters?' · '+esc(V.chapterWord)+' '+c.chap:''}</div><h1 class="ctitle">${esc(t)}</h1>`+c.secs.map(secHTML).join('');
 $('page').innerHTML=h;layerClasses();applyFilters();
 if(target){const el=$(target);if(el){el.scrollIntoView({block:'start'});el.classList.add('flash');setTimeout(()=>el.classList.remove('flash'),1300);if(!keep)select(target)}}else $('read').scrollTop=0;
 if(innerWidth<=760)$('rail').dataset.open='false'}
function applyFilters(){if(VIEW==='list')listView();document.querySelectorAll('#page .u').forEach(u=>{const ids=u.dataset.m.split(',').map(Number).filter(i=>visRow(ROWS[i]));u.classList.toggle('off',!ids.length);u.classList.toggle('multi',new Set(ids.map(i=>ROWS[i].fam)).size>1);u.classList.toggle('poss',ids.length>0&&ids.every(i=>ROWS[i].status!=='match'||ROWS[i].label==='commonplace'));if(ids.length)u.style.setProperty('--c',`var(--f${ROWS[ids[0]].fam})`)});
 document.querySelectorAll('#page .dots').forEach(b=>b.innerHTML=famDots(byId[b.dataset.s]));meters()}
// panel
function ewHTML(ew){const C=RU.earliest||{},w=ew.witness,wl=(C.witnessLabels||{})[w]??w;
 const loc=ew.locus&&!(C.hideLocusFor||[]).includes(w)&&(!C.locusNeedsLatin||ew.latin);
 let h=`<div class="ew"><b>Earliest witness:</b> ${esc(wl)}${loc?' · '+esc(ew.locus):''}`;
 if(ew.passage)h+=`<div class="q src"><small>earlier text</small>${esc(ew.passage)}</div>`;
 if(ew.latin&&ew.latin!==ew.passage)h+=`<div class="q src"><small>${esc(C.latinLabel||'Latin')}</small>${esc(ew.latin)}</div>`;
 if(C.nearestPrefix&&ew.nearest&&ew.nearest!=='n/a'){const nl=C.nearestLabels||{};h+=`<div class="why">${esc(C.nearestPrefix)}${esc(nl[ew.nearest]||nl['*']||ew.nearest)}</div>`}
 if(C.showReason&&ew.reason)h+=`<div class="why">${esc(ew.reason)}</div>`;
 return h+'</div>'}
function rowHTML(r,hl){const l=r.links.map(([t,u])=>`<a href="${u}">${esc(t)}</a>`).join('');const N=RU.nearer||{},P=RU.partLabels||{};
 const near=r.near&&N.title?`<div class="ew"><b>${esc(N.title)}</b> ${esc(N.prefix)}${esc((N.labels||{})[r.near]||(N.labels||{})['*']||r.near)}</div>`:'';
 return `<div class="m${hl?' hl':''}" style="--c:var(--f${r.fam})" id="r${r.id}"><div class="mh"><span class="fam">${r.fam}</span><b>${esc(r.work)}</b>${r.locus?`<span>${esc(r.locus)}</span>`:''}${r.toUnit&&MAN[r.to]?xref(r.to,r.toUnit):''}${repLink(r)}${r.noteref?`<span>${esc(r.noteref)}</span>`:''}${r.note?`<span>${esc(RU.noteLabel||'(note)')}</span>`:''}${r.part&&P[r.part]?`<span>${esc(P[r.part])}</span>`:''}${r.qa?`<span>quoting ${esc(r.qa)}</span>`:''}<span class="lab">${esc(r.label)}</span><span style="color:var(--mut)">${r.conf.toFixed(2)}${r.status==='possible'?' · possible':''}</span></div>
 <div class="q"><small>${esc(RU.baseTag)}</small>${esc(r.vp)}</div><div class="q src"><small>${esc((FAMI[r.fam]||{}).sourceLabel||RU.sourceLabel)}</small>${esc(r.sp)}</div>${r.fr?`<div class="q src"><small>${esc(RU.frenchLabel||'working French')}</small>${esc(r.fr)}</div>`:''}${r.ew?ewHTML(r.ew):''}${near}<div class="why">${esc(r.reason)}</div><div class="lk">${l}<span style="color:var(--mut)">${esc(r.page)}</span></div></div>`}
function select(sid,ids){const s=byId[sid];if(!s)return;st.sel=sid;save();document.querySelectorAll('.sec.sel').forEach(e=>e.classList.remove('sel'));const el=$(sid);if(el)el.classList.add('sel');
 const focus=ids&&ids.length;
 const all=(rowsBySec[sid]||[]).filter(visRow);
 const rs=(focus?all.filter(r=>ids.includes(r.id)):all).sort((a,b)=>b.conf-a.conf);
 const hidden=focus?0:(rowsBySec[sid]||[]).length-rs.length;
 const more=focus&&all.length>rs.length?`<p><button class="btn" data-all="${sid}">All ${all.length} sources for this section</button></p>`:'';
 const LV=LAY.variants||{};const vars=(s.vars||[]).map(v=>`<div class="m" style="--c:var(--add-line)"><div class="mh"><span class="fam" style="--c:var(--add-line)">${esc(LV.tag)}</span><b>${esc(v.type)}</b>${v.otherLink?`<a href="${v.otherLink}">${esc(LV.otherLinkLabel)}</a>`:''}</div><div class="why" style="color:var(--fg)">${esc(v.content)}</div></div>`).join('');
 const ins=focus?[]:(IN[sid]||[]).filter(visIn);
 const inH=ins.length?`<h3 class="ph">Reused in other editions</h3>`+rowsTable('in:'+sid,ins,['there','label','conf','theirs']):'';
 panel(`<h2>${lbl(s.id)}</h2><div class="sub">${esc(s.margin)}</div>${rs.length?rs.map(r=>rowHTML(r,false)).join(''):'<p class="empty">No source shown for this section with the current filters.</p>'}${more}${hidden?`<p class="empty">${hidden} more hidden by filters (possible matches, commonplaces or a switched-off source).</p>`:''}${focus?'':vars}${inH}`);
 if(innerWidth<=1100&&ids)$('panel').dataset.open='true'}
function panel(h){$('panel').innerHTML=`<button class="btn only-narrow" data-close style="float:right">Close</button>${h}${verLine()}`;$('panel').scrollTop=0}
// the edition's version, at the foot of every panel
const verLine=()=>`<p class="ver">${esc(M.short)} · version ${esc(M.version||'?')}${M.changed?' of '+esc(M.changed):''} · <a href="${BASE}CHANGELOG.md">changes</a></p>`;
function edInfo(){const n=SEC.filter(s=>s.kind!=='heading').length;
 panel(`<h2>${esc(M.short)}</h2><div class="sub">${esc(M.author)}, ${esc(M.title)}. ${esc(M.imprint)}.</div><p class="lsub">${n} units · ${ROWS.filter(Boolean).length} reuse rows${INROWS.length?` · ${INROWS.length} rows of other editions reuse it`:''}</p>`)}
// a sortable table of reuse rows; the list view and the panel's 'reused in' use it
const COLS={
 unit:{label:'Unit',key:r=>unitKey(M,r.sec),html:r=>`<a href="#${r.sec}" data-row="${r.id}">${esc(lbl(r.sec))}</a>`},
 source:{label:'Source',key:r=>r.work+' '+r.locus,html:r=>`<span class="fam" style="--c:var(--f${r.fam})">${esc(r.fam)}</span> ${esc(r.work)}${r.locus?' · '+esc(r.locus):''}${r.toUnit&&MAN[r.to]?' '+xref(r.to,r.toUnit):''}${repLink(r)}`},
 label:{label:'Label',key:r=>r.label,html:r=>esc(r.label)},
 conf:{label:'Conf.',key:r=>-r.conf,html:r=>r.conf.toFixed(2)+(r.status==='possible'?' <span class="poss">possible</span>':'')},
 passage:{label:'Passage',key:r=>r.vp,html:r=>`<span class="pas">${esc(r.vp)}</span>`},
 here:{label:'Unit',key:r=>unitKey(M,r.toUnit),html:r=>`<a href="#${r.toUnit}">${esc(lbl(r.toUnit))}</a>`},
 there:{label:'Reused in',key:r=>[r.from,...unitKey(MAN[r.from],r.sec)],html:r=>xref(r.from,r.sec)+(r.via?` <span class="via">through ${esc(r.via)}</span>`:'')},
 theirs:{label:'Passage reused',key:r=>r.sp,html:r=>`<span class="pas">${esc(r.sp)}</span>`},
};
const TBL={};
function rowsTable(id,rows,cols){const t=TBL[id]=TBL[id]||{sort:cols[0],dir:1};t.rows=rows;t.cols=cols;
 const K=COLS[t.sort].key,v=rows.map(r=>[K(r),r]);
 v.sort((a,b)=>{const x=a[0],y=b[0];const c=Array.isArray(x)?cmpKey(x,y):x<y?-1:x>y?1:0;return c*t.dir||a[1].id-b[1].id});
 return `<div class="rtw"><table class="rt" data-t="${esc(id)}"><thead><tr>${cols.map(c=>`<th data-sort="${c}" aria-sort="${t.sort===c?(t.dir>0?'ascending':'descending'):'none'}">${COLS[c].label}</th>`).join('')}</tr></thead>
 <tbody>${v.map(([,r])=>`<tr>${cols.map(c=>`<td class="c-${c}">${COLS[c].html(r)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`}
// list view: viewer/?ed=<id>&view=list
function viewChrome(){const q=new URLSearchParams(location.search),v=VIEW;if(v==='list')q.set('view','list');else q.delete('view');
 history.replaceState(null,'','?'+q.toString()+(v==='text'&&st.sel?'#'+st.sel:''));$('vText').setAttribute('aria-pressed',v==='text');$('vList').setAttribute('aria-pressed',v==='list');
 document.body.classList.toggle('listing',v==='list')}
function setView(v){VIEW=v;viewChrome();if(v==='list')listView();else go(st.sel&&byId[st.sel]?st.sel:V.start||CH[0].secs[0].id)}
function listView(){const all=ROWS.filter(Boolean),out=all.filter(visRow),inc=INROWS.filter(visIn),isIn=LTAB==='in'&&INROWS.length>0;
 const tabs=INROWS.length?`<div class="seg" role="group"><button data-ltab="out" aria-pressed="${!isIn}">Sources used (${out.length})</button><button data-ltab="in" aria-pressed="${isIn}">Reused in other editions (${inc.length})</button></div>`:'';
 const n=isIn?`${inc.length} of ${INROWS.length} rows`:`${out.length} of ${all.length} rows`;
 $('page').innerHTML=`<div class="chead">${esc(M.short)}</div><h1 class="ctitle">Reuse, row by row</h1>${tabs}<p class="lsub">${n} shown. The filters in the top bar apply. Click a column head to sort, a unit to read it.</p>`+
  (isIn?rowsTable('list:in',inc,['here','there','label','conf','theirs']):rowsTable('list:out',out,['unit','source','label','conf','passage']));
 document.querySelectorAll('.rail a').forEach(a=>a.classList.remove('on'))}
function resort(th){const tb=th.closest('table'),id=tb.dataset.t,t=TBL[id],c=th.dataset.sort;if(t.sort===c)t.dir=-t.dir;else{t.sort=c;t.dir=1}tb.outerHTML=rowsTable(id,t.rows,t.cols)}
// translation layer
let enMode='tr';try{enMode=localStorage.getItem('nleEnMode')||'tr'}catch(e){}
function txOffset(tx,node,off){const w=document.createTreeWalker(tx,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.parentElement.closest('.old,.pb')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});let pos=0,n;
 if(node.nodeType!==3){const r=document.createRange();r.setStart(tx,0);r.setEnd(node,off);const f=r.cloneContents();const d=document.createElement('div');d.appendChild(f);d.querySelectorAll('.old,.pb').forEach(x=>x.remove());return d.textContent.length}
 while(n=w.nextNode()){if(n===node)return pos+off;pos+=n.data.length}return pos}
function selIdx(){if(!layerOn('translation'))return null;const sel=getSelection();if(!sel.rangeCount||sel.isCollapsed)return null;const r=sel.getRangeAt(0);const tx=r.commonAncestorContainer.nodeType===1?r.commonAncestorContainer.closest('.tx'):r.commonAncestorContainer.parentElement.closest('.tx');
 if(!tx)return null;const sec=tx.closest('.sec');const s=byId[sec.id];if(!s||!s.en)return null;
 const a=txOffset(tx,r.startContainer,r.startOffset),b=txOffset(tx,r.endContainer,r.endOffset);
 const idx=s.fs.map((sp,i)=>sp[0]<b&&sp[1]>a?i:-1).filter(i=>i>=0);return idx.length?{sid:sec.id,idx,rect:r.getBoundingClientRect()}:null}
function markPhrase(text,phrases){let h=esc(text);phrases.forEach(f=>{if(!f.ph)return;const e=esc(f.ph);const i=h.indexOf(e);if(i>=0)h=h.slice(0,i)+`<mark class="tf s${f.sev}" title="${esc(f.type+': '+f.note)}">${e}</mark>`+h.slice(i+e.length)});return h}
function showEN(sid,idx){const s=byId[sid];if(!s||!s.en)return;const E=s.en,L=LAY.translation;const frT=i=>{const sp=s.fs[i];return plainOf(s).slice(sp[0],sp[1])};
 const gs=E.g.map((g,k)=>({k,f:g[0],e:g[1]})).filter(g=>!idx||g.f.some(i=>idx.includes(i)));
 const fl=k=>(E.f||[]).filter(f=>f.k===k);
 const tl=t=>({mistranslation:'Mistranslation',shift:'Shift',omission:'Omission',addition:'Addition',terminology:'Term','false friend':'False friend'}[t]||t);
 const flagHTML=k=>fl(k).map(f=>`<div class="tfl"><b>${tl(f.type)}${f.sev>=3?' · major':''}</b> · <i>${esc(f.fr)}</i>${f.en?` → “${esc(f.en)}”`:' → (not translated)'}. ${esc(f.note)}</div>`).join('');
 let body='';
 if(enMode==='tr'){body=`<div class="ent">${gs.map(g=>markPhrase(g.e.map(j=>E.s[j]).join(' '),fl(g.k).map(f=>({ph:f.en,sev:f.sev,type:tl(f.type),note:f.note})))).join(' ')}</div>`;const n=gs.reduce((a,g)=>a+fl(g.k).length,0);if(n)body+=`<p class="enhd">${n} translation ${n>1?'problems':'problem'} in this passage. Underlined; see Compare.</p>`}
 else body=gs.map(g=>`<div class="cmp"><div class="fr">${markPhrase(g.f.map(frT).join(' '),fl(g.k).map(f=>({ph:f.fr,sev:f.sev,type:tl(f.type),note:f.note})))}</div><div class="en">${markPhrase(g.e.map(j=>E.s[j]).join(' ')||'—',fl(g.k).map(f=>({ph:f.en,sev:f.sev,type:tl(f.type),note:f.note})))}</div>${flagHTML(g.k)}</div>`).join('');
 const all=idx&&gs.length<E.g.length?`<button class="btn" data-enall="${sid}">Whole section</button>`:'';
 panel(`<h2>${lbl(s.id)} · ${esc(L.label)}</h2><div class="sub">${esc(fill(L.panelNote,{page:E.p}))}</div>
 <div class="seg" role="group"><button data-enmode="tr" aria-pressed="${enMode==='tr'}">Translation</button><button data-enmode="cmp" aria-pressed="${enMode==='cmp'}">Compare</button></div> ${all}${body}`);
 $('panel').dataset.open='true';enState={sid,idx}}
let enState=null;const plainCache={};
function plainOf(s){if(!plainCache[s.id]){const d=document.createElement('div');d.innerHTML=s.html;d.querySelectorAll('.old,.pb').forEach(x=>x.remove());plainCache[s.id]=d.textContent}return plainCache[s.id]}
const onSelEnd=e=>{if(e.target.closest('#enPop'))return;setTimeout(()=>{const r=selIdx();const pop=$('enPop');if(!r){pop.hidden=true;return}pop.hidden=false;pop.style.left=Math.min(innerWidth-90,r.rect.right+6)+'px';pop.style.top=Math.max(4,r.rect.top-30)+'px';pop.onclick=ev=>{ev.stopPropagation();pop.hidden=true;showEN(r.sid,r.idx)}},10)};
document.addEventListener('mouseup',onSelEnd);document.addEventListener('touchend',e=>setTimeout(()=>onSelEnd(e),250));
$('read').addEventListener('scroll',()=>{$('enPop').hidden=true},{passive:true});
// search, and go to a unit by the patterns in the manifest
let plain=null;
let lastQ='';
function gotoId(q){for(const g of V.goto||[]){const m=q.match(new RegExp(g.re,'i'));if(m)return g.id.replace(/\{(\d)\}/g,(x,k)=>g.upper?m[k].toUpperCase():m[k])}return null}
function doSearch(q){q=q.trim();if(!q){return}lastQ=q;
 let id=gotoId(q);if(id&&M.aliases&&M.aliases[id]&&!byId[id])id=M.aliases[id];if(id&&byId[id]){go(id);return}
 if(!plain){const d=document.createElement('div');plain=SEC.map(s=>{d.innerHTML=s.html+' '+s.notes.map(n=>n.html).join(' ');return d.textContent})}
 const ql=q.toLowerCase();const res=[];SEC.forEach((s,i)=>{const t=plain[i];const j=t.toLowerCase().indexOf(ql);if(j>=0&&s.kind!=='heading')res.push([s,t.slice(Math.max(0,j-60),j+q.length+80),j])});
 panel(`<h2>Search</h2><div class="sub">${res.length} sections contain “${esc(q)}”${res.length>300?' (first 300 shown)':''}</div><div class="res">${res.slice(0,300).map(([s,t])=>`<a href="#${s.id}" data-hit="${s.id}"><b>${lbl(s.id)}</b>${esc(t).replace(new RegExp(esc(q).replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'ig'),x=>`<mark>${x}</mark>`)}</a>`).join('')}</div>`);
 $('panel').dataset.open='true'}
function resolve(id){if(!byId[id]&&M.aliases&&M.aliases[id])id=M.aliases[id];if(!byId[id]){const k=CH.find(x=>x.key===id);if(k)id=k.secs[0].id}return chOf[id]?id:null}
function go(id,keep){id=resolve(id);if(!id)return;if(VIEW==='list'){VIEW='text';viewChrome()}const c=chOf[id];if(st.chap===c.key&&$(id)){$(id).scrollIntoView({block:'start'});$(id).classList.add('flash');setTimeout(()=>$(id).classList.remove('flash'),1300);if(!keep)select(id)}else show(c.key,id,keep);if(location.hash.slice(1)!==id)history.replaceState(null,'','#'+id)}
function hitRanges(root,q){const ranges=[];if(!root||!q)return ranges;const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.parentElement.closest('.old,.pb,.mk')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});const nodes=[];let txt='',n;while(n=w.nextNode()){nodes.push([n,txt.length]);txt+=n.data}
 const low=txt.toLowerCase(),ql=q.toLowerCase();let i=low.indexOf(ql);
 const at=pos=>{let k=nodes.length-1;while(k>0&&nodes[k][1]>pos)k--;return [nodes[k][0],pos-nodes[k][1]]};
 while(i>=0&&ranges.length<50){const r=document.createRange();const [a,ao]=at(i),[b,bo]=at(i+ql.length-1);r.setStart(a,ao);r.setEnd(b,bo+1);ranges.push(r);i=low.indexOf(ql,i+ql.length)}
 return ranges}
function markHits(id,q){if(window.CSS&&CSS.highlights)CSS.highlights.delete('shl');const rs=hitRanges($(id),q);if(!rs.length)return;
 if(window.CSS&&CSS.highlights&&window.Highlight)CSS.highlights.set('shl',new Highlight(...rs));
 const sel=getSelection();sel.removeAllRanges();sel.addRange(rs[0].cloneRange());
 const r=rs[0].getBoundingClientRect(),rd=$('read');rd.scrollTop+=r.top-rd.getBoundingClientRect().top-rd.clientHeight/3}
function toast(t){const e=document.createElement('div');e.className='toast';e.textContent=t;document.body.appendChild(e);setTimeout(()=>e.remove(),1600)}
function copy(t){(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>toast('Copied')).catch(()=>{const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');toast('Copied')}catch(e){toast(t)}ta.remove()})}
// events
document.addEventListener('click',e=>{if(e.target.closest('[data-close]')){$('panel').dataset.open='false';return}const u=e.target.closest('.u:not(.off)');if(u){e.preventDefault();document.querySelectorAll('.u.hit').forEach(x=>x.classList.remove('hit'));u.classList.add('hit');const sec=u.closest('.sec');select(sec.id,u.dataset.m.split(',').map(Number).filter(i=>visRow(ROWS[i])));return}
 const th=e.target.closest('th[data-sort]');if(th){resort(th);return}
 const lt=e.target.closest('[data-ltab]');if(lt){LTAB=lt.dataset.ltab;listView();return}
 const rl=e.target.closest('a[data-row]');if(rl){e.preventDefault();const id=rl.getAttribute('href').slice(1);go(id,true);select(id,[Number(rl.dataset.row)]);$('panel').dataset.open='true';return}
 const al=e.target.closest('[data-all]');if(al){select(al.dataset.all);return}
 const en=e.target.closest('[data-en]');if(en){showEN(en.dataset.en,null);return}
 const ea=e.target.closest('[data-enall]');if(ea){showEN(ea.dataset.enall,null);return}
 const em=e.target.closest('[data-enmode]');if(em){enMode=em.dataset.enmode;try{localStorage.setItem('nleEnMode',enMode)}catch(x){}if(enState)showEN(enState.sid,enState.idx);return}
 const d=e.target.closest('.dots');if(d){select(d.dataset.s);if(innerWidth<=1100)$('panel').dataset.open='true';return}
 const dv=e.target.closest('[data-dv]');if(dv){if(!layerOn('comments')){setLayer(LAY.comments,true)}document.querySelectorAll(`#${CSS.escape(dv.dataset.dv)} details.dv`).forEach((x,i)=>{x.open=true;if(!i)x.scrollIntoView({block:'nearest'})});return}
 const c=e.target.closest('[data-copy]');if(c){copy(cite(byId[c.dataset.copy]));return}
 const l=e.target.closest('[data-link]');if(l){copy(location.href.split('#')[0]+'#'+l.dataset.link);return}
 const hit=e.target.closest('[data-hit]');if(hit){e.preventDefault();document.querySelectorAll('.res a.on').forEach(x=>x.classList.remove('on'));hit.classList.add('on');go(hit.dataset.hit,true);markHits(hit.dataset.hit,lastQ);return}
 const a=e.target.closest('a[href^="#"]');if(a){e.preventDefault();go(a.getAttribute('href').slice(1));return}
 const sec=e.target.closest('.sec');if(sec&&!e.target.closest('a')){if(getSelection().toString().trim())return;if(window.CSS&&CSS.highlights)CSS.highlights.delete('shl');select(sec.id)}});
$('q').addEventListener('keydown',e=>{if(e.key==='Enter')doSearch(e.target.value)});
// filters: Sources and Possible matches, one checkbox per layer, one button per source family
function setLayer(l,on){if(l.kind==='reuse'){setFams({[l.family]:on});return}
 st.layers[l.id]=on;layerClasses();meters();if(l.kind==='translation'&&!on)$('enPop').hidden=true;
 const cb=document.querySelector(`#lays input[data-l="${CSS.escape(l.id)}"]`);if(cb)cb.checked=on;save()}
// families: switch some on or off, then redraw everything that shows them
function setFams(ch){Object.assign(st.fams,ch);save();applyFilters();if(st.sel&&VIEW==='text')select(st.sel);srcPop();
 LAYS.filter(l=>l.kind==='reuse').forEach(l=>{const cb=document.querySelector(`#lays input[data-l="${CSS.escape(l.id)}"]`);if(cb)cb.checked=!!st.fams[l.family]})}
// the Sources menu: one line per family with its colour, the rows it has under the current settings, a bar, and "only"
function srcPop(){const n={};ROWS.forEach(r=>{if(r&&((r.status==='match'&&r.label!=='commonplace')||st.pos))n[r.fam]=(n[r.fam]||0)+1});
 const fs=FAMS.map(([k,l])=>({k,l,n:n[k]||0})).sort((a,b)=>b.n-a.n),max=Math.max(1,...fs.map(f=>f.n)),on=fs.filter(f=>st.fams[f.k]);
 $('srcDots').innerHTML=on.slice(0,12).map(f=>`<i style="--c:var(--f${f.k})"></i>`).join('');$('srcN').textContent=`${on.length}/${fs.length}`;
 $('srcBtn').classList.toggle('dim',!st.src);
 $('srcPop').innerHTML=`<div class="sph"><label class="tg"><input type="checkbox" id="tSrc"${st.src?' checked':''}> Show sources in the text</label><span class="spa"><button class="btn" data-fa="all">All</button><button class="btn" data-fa="none">None</button></span></div>
 <ul>${fs.map(f=>`<li class="${st.fams[f.k]?'':'off'}" style="--c:var(--f${f.k})"><label title="${esc(f.l)}"><input type="checkbox" data-f="${f.k}"${st.fams[f.k]?' checked':''}><i></i><span>${esc(f.l)}</span></label><span class="mb"><b style="width:${Math.round(100*f.n/max)}%"></b></span><span class="n">${f.n}</span><button class="only" data-only="${f.k}">only</button></li>`).join('')}</ul>
 <p class="spn">Rows per source${st.pos?', possible matches included':', confident matches'}.</p>`}
function filters(){const hasRows=ROWS.length>0;$('srcW').hidden=$('lPos').hidden=!hasRows;
 $('tPos').checked=st.pos;
 $('tPos').onchange=e=>{st.pos=e.target.checked;save();applyFilters();if(st.sel&&VIEW==='text')select(st.sel);srcPop()};
 $('lays').innerHTML=LAYS.filter(l=>l.toggle!==false).map(l=>`<label class="tg" title="${esc(l.tooltip||'')}"><input type="checkbox" data-l="${esc(l.id)}"${(l.kind==='reuse'?st.fams[l.family]:st.layers[l.id])?' checked':''}> ${esc(l.label)}</label>`).join('');
 $('lays').onchange=e=>{const l=LAYS.find(x=>x.id===e.target.dataset.l);if(l)setLayer(l,e.target.checked)};
 const LV=LAY.variants;if(LV)document.documentElement.style.setProperty('--old-tag',JSON.stringify((LV.otherTag||'')+' '));
 if(LAY.comments&&LAY.comments.family)document.documentElement.style.setProperty('--cmt',`var(--f${LAY.comments.family})`);
 srcPop();
 const pop=$('srcPop'),btn=$('srcBtn'),open=o=>{pop.hidden=!o;btn.setAttribute('aria-expanded',o)};
 btn.onclick=e=>{e.stopPropagation();open(pop.hidden)};
 pop.onclick=e=>{e.stopPropagation();const o=e.target.closest('[data-only]'),a=e.target.closest('[data-fa]');
  if(o)setFams(Object.fromEntries(FAMS.map(([k])=>[k,k===o.dataset.only])));
  if(a)setFams(Object.fromEntries(FAMS.map(([k])=>[k,a.dataset.fa==='all'])))};
 pop.onchange=e=>{const c=e.target;if(c.id==='tSrc'){st.src=c.checked;save();applyFilters();if(st.sel&&VIEW==='text')select(st.sel);srcPop();return}
  if(c.dataset.f)setFams({[c.dataset.f]:c.checked})};
 document.addEventListener('click',e=>{if(!pop.hidden&&!e.target.closest('#srcW'))open(false)});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!pop.hidden){open(false);btn.focus()}})}
function init(){
 document.title=(M.short||M.title)+' · '+(CAT.title||'');$('q').placeholder=V.searchPlaceholder||'Search';
 if(LAY.translation)$('enPop').textContent=LAY.translation.label;
 filters();
 $('filtBtn').onclick=()=>{$('filt').dataset.open=$('filt').dataset.open==='true'?'false':'true'};
 $('railBtn').onclick=()=>{$('rail').dataset.open=$('rail').dataset.open==='true'?'false':'true'};
 $('panelBtn').onclick=()=>{$('panel').dataset.open=$('panel').dataset.open==='true'?'false':'true'};
 addEventListener('hashchange',()=>{const h=decodeURIComponent(location.hash.slice(1));if(h)go(h)});
 $('vText').onclick=()=>{if(VIEW!=='text')setView('text')};$('vList').onclick=()=>{if(VIEW!=='list'){setView('list');edInfo()}};
 applyW();rail();
 const h0=resolve(decodeURIComponent(location.hash.slice(1)));
 if(VIEW==='list'){if(h0)st.sel=h0;setView('list');edInfo()}
 else if(h0)go(h0);else if(st.sel&&byId[st.sel])go(st.sel);else go(V.start||CH[0].secs[0].id);
 if(innerWidth>1100){$('panel').dataset.open='true'}}
// resizable frames
function applyW(){const a=$('app');if(st.widths){if(st.widths.r)a.style.setProperty('--wr',st.widths.r+'px');if(st.widths.p)a.style.setProperty('--wp',st.widths.p+'px')}}
document.querySelectorAll('.gut').forEach(g=>g.addEventListener('pointerdown',e=>{e.preventDefault();g.setPointerCapture(e.pointerId);g.classList.add('drag');document.body.classList.add('resizing');
 const side=g.dataset.g;const mv=ev=>{st.widths=st.widths||{};if(side==='r')st.widths.r=Math.max(150,Math.min(520,ev.clientX));else st.widths.p=Math.max(260,Math.min(innerWidth*0.6,innerWidth-ev.clientX));applyW()};
 const up=()=>{g.classList.remove('drag');document.body.classList.remove('resizing');g.removeEventListener('pointermove',mv);g.removeEventListener('pointerup',up);save()};
 g.addEventListener('pointermove',mv);g.addEventListener('pointerup',up)}));
document.querySelectorAll('.gut').forEach(g=>g.addEventListener('dblclick',()=>{st.widths={};$('app').style.removeProperty('--wr');$('app').style.removeProperty('--wp');save()}));
load().then(ok=>{if(ok)init()}).catch(e=>fail(`Could not load the edition: ${esc(e.message)}`));
