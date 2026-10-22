// Check every link in the collection: cross-edition links, reverse links, cross-references, aliases, catalogue paths.
// Usage: node tools/check_links.js [viewer base URL]
// Static checks read the files. Browser checks open each edition once in Chromium and go to every link target.
// Serve the repository first (python -m http.server 8000). Needs Playwright with Chromium.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

const ROOT = path.dirname(__dirname), base = process.argv[2] || 'http://localhost:8000/';
const read = p => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const bad = [], note = (k, m) => bad.push(`${k}: ${m}`);
const cat = read('catalogue.json');
const ED = {};
for (const e of cat.editions) {
  const man = read(e.path + 'edition.json'), text = read(e.path + man.text);
  const units = Object.fromEntries(text.units.map(u => [u.id, u]));
  ED[e.id] = { e, man, units };
}
const shown = (ed, id) => ED[ed].units[id] && ED[ed].units[id].kind !== 'heading';
const known = new Set([...cat.editions.map(e => e.id), ...cat.texts.map(t => t.id)]);

// catalogue and reuse tables
const targets = {};          // edition -> Set of unit ids that other editions link to
const back = {};             // edition -> Set of unit ids linked from "reused in"
const rowIds = {};
for (const c of cat.reuse) {
  if (!fs.existsSync(path.join(ROOT, c.path))) { note('missing table', c.path); continue; }
  const t = read(c.path);
  if (t.from !== c.from || t.to !== c.to || t.rows.length !== c.rows) note('catalogue entry differs from table', c.path);
  if (!ED[c.from]) note('from is not an edition', c.path);
  if (!known.has(c.to)) note('to is not in the catalogue', c.path);
  for (const r of t.rows) {
    const k = c.from + ':' + r.id;
    if (rowIds[k]) note('duplicate row id', k); rowIds[k] = 1;
    const u = ED[c.from] && ED[c.from].units[r.unit];
    if (!u) { note('row unit missing', `${c.path} row ${r.id} ${r.unit}`); continue; }
    for (const [p, a, b] of r.at) {
      const s = p === 't' ? u.text : (u.notes || [])[Number(p.slice(1))]?.text;
      if (s === undefined || !(0 <= a && a < b && b <= s.length)) note('row span out of range', `${c.path} row ${r.id}`);
    }
    if (r.toUnit) {
      if (!ED[c.to]) note('toUnit but to is no edition', `${c.path} row ${r.id}`);
      else if (!shown(c.to, r.toUnit)) note('toUnit not shown in target edition', `${c.path} row ${r.id} ${r.toUnit}`);
      else { (targets[c.to] = targets[c.to] || new Set()).add(r.toUnit); (back[c.from] = back[c.from] || new Set()).add(r.unit); }
    }
  }
}
for (const [id, { man, units }] of Object.entries(ED)) {
  // cross-references inside the text
  for (const u of Object.values(units)) for (const x of [...(u.xr || []), ...(u.notes || []).flatMap(n => n.xr || [])])
    if (!shown(id, x[2])) note('cross-reference target missing or hidden', `${id} ${u.id} -> ${x[2]}`);
  // aliases point at shown units and do not shadow existing ids
  for (const [a, b] of Object.entries(man.aliases || {})) {
    if (units[a]) note('alias shadows an existing id', `${id} ${a}`);
    if (!shown(id, b)) note('alias target missing', `${id} ${a} -> ${b}`);
  }
  if (man.viewer && man.viewer.start && !shown(id, man.viewer.start)) note('start unit missing', id);
  for (const l of man.layers) {
    if (l.file && !fs.existsSync(path.join(ROOT, ED[id].e.path, l.file))) note('missing layer file', `${id} ${l.file}`);
    if (l.table && !cat.reuse.some(c => c.path === l.table && c.from === id)) note('layer table not in catalogue', `${id} ${l.table}`);
    if (l.kind === 'reuse' && !man.reuse.families.some(f => f.key === l.family)) note('layer family unknown', `${id} ${l.id}`);
    if (l.file) { const L = read(ED[id].e.path + l.file);
      for (const it of L.items || []) if (!units[it.unit]) note('layer item unit missing', `${id} ${l.id} ${it.unit}`);
      for (const u of Object.keys(L.units || {})) if (!units[u]) note('layer unit missing', `${id} ${l.id} ${u}`); }
  }
  if (!fs.existsSync(path.join(ROOT, ED[id].e.path, 'CHANGELOG.md'))) note('missing changelog', id);
  if (!man.version || !man.changed) note('missing version', id);
}
const fams = {};
for (const c of cat.reuse) for (const r of read(c.path).rows) (fams[c.from] = fams[c.from] || new Set()).add(r.family);
for (const [id, s] of Object.entries(fams)) for (const f of s)
  if (!ED[id].man.reuse.families.some(x => x.key === f)) note('row family not in manifest', `${id} ${f}`);

(async () => {
  // open each edition and go to every unit another edition links to, every unit that links out, and every alias
  const browser = await chromium.launch(); const errors = []; let opened = 0;
  for (const id of Object.keys(ED)) {
    const page = await browser.newPage(); page.on('pageerror', e => errors.push(`${id}: ${e}`));
    await page.goto(base + 'viewer/?ed=' + id);
    await page.waitForFunction(() => typeof SEC !== 'undefined' && SEC.length && document.querySelector('#page .sec'), null, { timeout: 60000 });
    const ids = [...(targets[id] || []), ...(back[id] || [])], al = Object.entries(ED[id].man.aliases || {});
    const res = await page.evaluate(([ids, al]) => {
      const out = [];
      for (const u of ids) { go(u); if (!document.getElementById(u) || location.hash !== '#' + u) out.push('unit ' + u); }
      for (const [a, b] of al) { go(a); if (location.hash !== '#' + b) out.push('alias ' + a); }
      return out;
    }, [ids, al]);
    res.forEach(m => note('viewer cannot open', `${id} ${m}`));
    opened += ids.length + al.length;
    // the links the viewer draws: every "reused in" and every row link must name a unit of the other edition
    const drawn = await page.evaluate(() => { const o = [];
      for (const s of SEC) for (const r of (IN[s.id] || [])) o.push(r.from + '#' + r.sec);
      for (const r of ROWS) if (r && r.toUnit) o.push(r.to + '#' + r.toUnit); return [...new Set(o)]; });
    for (const x of drawn) { const [e, u] = x.split('#'); if (!ED[e] || !shown(e, u)) note('viewer draws a dead link', `${id} -> ${x}`); }
    await page.close();
  }
  // one real click each way
  const page = await browser.newPage(); page.on('pageerror', e => errors.push(String(e)));
  const src = read('reuse/vattel-1773__burlamaqui-1747.json').rows.find(r => r.toUnit && r.status === 'match' && r.label !== 'commonplace');
  const t = src && src.toUnit;
  if (t) {
    await page.goto(base + 'viewer/?ed=vattel-1773#' + src.unit); await page.waitForSelector('#page .sec');
    await page.click(`#${src.unit.replace(/\./g, '\\.')} .dots`); await page.click(`#panel a.xed[href$="#${t}"]`);
    await page.waitForFunction(u => location.search.includes('burlamaqui-1747') && document.getElementById(u), t, { timeout: 60000 });
    await page.click(`#panel table.rt td.c-there a`);
    await page.waitForFunction(() => location.search.includes('vattel-1773') && document.querySelector('#page .sec'), null, { timeout: 60000 });
  }
  await browser.close();
  errors.forEach(e => note('page error', e));
  const n = Object.values(rowIds).length;
  console.log(bad.length ? 'PROBLEMS' : 'OK', `${cat.reuse.length} tables, ${n} rows, ${opened} link targets opened in the viewer`);
  bad.slice(0, 40).forEach(b => console.log('  ' + b));
  process.exit(bad.length ? 1 : 0);
})();
