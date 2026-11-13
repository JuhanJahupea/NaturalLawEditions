// Check that the viewer rebuilds a working edition's data.json exactly from the collection files.
// Usage: node tools/check_edition.js <edition id> <path to the original data.json> [viewer base URL]
// Serve the repository first (python -m http.server 8000). Needs Playwright with Chromium.
const fs = require('fs');
const { chromium } = require('playwright');

const [ed, dataPath, base = 'http://localhost:8000/'] = process.argv.slice(2);
const D = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
// the viewer uses neutral names where the Vattel working edition used the years
const norm = h => h.replace(/class="v73"/g, 'class="var"').replace(/class="d58"/g, 'class="old"');
D.sections.forEach(s => {
  s.html = norm(s.html); s.notes.forEach(n => { n.html = norm(n.html); });
  if (s.vars) s.vars = s.vars.map(v => ({ id: v.id, type: v.type, content: v.content, passage: v.p1773, otherPassage: v.p1758, otherPages: v.pages1758, otherLink: v.link1758, placed: v.placed }));
});
// corrections (editions/<ed>/corrections.json, noteMoves): footnotes the working edition attached to the wrong section.
// The converter moves them (tools/nle.py apply_note_moves); the same moves are made here on data.json before comparing.
function applyNoteMoves(D, moves) {
  const by = Object.fromEntries(D.sections.map(s => [s.id, s])), order = Object.fromEntries(D.sections.map((s, i) => [s.id, i]));
  const take = {}, back = {}, fwd = {}, dest = {}, cites = new Set();
  for (const m of moves) {
    const src = by[m.from], idx = [m.note, ...(m.cont || [])];
    if (src.notes[m.note].mark !== m.mark) throw new Error('correction: mark ' + JSON.stringify(m));
    (take[m.from] = take[m.from] || new Set()); idx.forEach(i => take[m.from].add(i));
    const notes = idx.map(i => src.notes[i]);
    notes.forEach(n => { for (const x of n.html.matchAll(/data-m="([\d,]+)"/g)) x[1].split(',').forEach(id => { dest[+id] = m.to }); for (const x of n.html.matchAll(/href="#([^"]+)"/g)) cites.add(x[1]) });
    // a 1773 change marked inside the moved note goes with it
    const vids = new Set(notes.flatMap(n => [...n.html.matchAll(/data-v="([^"]+)"/g)].map(x => x[1])));
    for (const vid of vids) { const k = (src.vars || []).findIndex(v => v.id === vid); if (k >= 0) { const v = src.vars.splice(k, 1)[0]; (by[m.to].vars = by[m.to].vars || []).push(v) } }
    const box = order[m.to] < order[m.from] ? back : fwd; (box[m.to] = box[m.to] || []).push([m.from, m.note, notes]);
  }
  const sortk = (a, b) => order[a[0]] - order[b[0]] || a[1] - b[1];
  const touched = new Set([...Object.keys(take), ...Object.keys(back), ...Object.keys(fwd)]), oldNotes = {};
  touched.forEach(sid => { oldNotes[sid] = by[sid].notes.slice() });
  for (const sid of touched) {
    const s = by[sid], keep = s.notes.filter((n, i) => !(take[sid] && take[sid].has(i)));
    s.notes = [...(fwd[sid] || []).sort(sortk).flatMap(x => x[2]), ...keep, ...(back[sid] || []).sort(sortk).flatMap(x => x[2])];
  }
  const sec0 = new Map(D.rows.map(r => [r, r.sec]));
  // rows anchored in a note record its index in 'where'
  const pos = new Map(); touched.forEach(sid => by[sid].notes.forEach((n, i) => pos.set(n, [sid, i])));
  D.rows.forEach(r => { const m = /^n(\d+)$/.exec(r.where || ''); const s0 = sec0.get(r);
    if (!m || !oldNotes[s0]) return; const p = pos.get(oldNotes[s0][+m[1]]); if (p) { r.sec = p[0]; r.where = 'n' + p[1] } });
  // a moved note can carry a cross-reference: the cited sections' "cited at" lists change with it
  for (const t of cites) if (by[t]) by[t].citedBy = D.sections.filter(s => s.id !== t && [s.html, ...s.notes.map(n => n.html)].some(h => h.includes('href="#' + t + '"'))).map(s => s.id);
}
// fields the collection adds to a row
const ADDED = ['to', 'toUnit', 'relation', 'rep', 'attr'];
// later passes (editions/<ed>/passes/): rows of data.json they replace are skipped; their own rows and divergence items
// are compared with the pass files instead
const root = __dirname + '/../editions/' + ed + '/';
const readDir = d => fs.existsSync(d) ? fs.readdirSync(d).filter(f => f.endsWith('.json')).map(f => JSON.parse(fs.readFileSync(d + f, 'utf8'))) : [];
const HAS_EN = D.sections.some(s => s.en);
const SUPERSEDED = new Set(readDir(root + 'provenance/superseded/').flatMap(t => t.rows.map(r => r.id)));
const PASSES = readDir(root + 'passes/');
const CORR = fs.existsSync(root + 'corrections.json') ? JSON.parse(fs.readFileSync(root + 'corrections.json', 'utf8')) : null;
if (CORR) applyNoteMoves(D, CORR.noteMoves || []);
const PASS_ROWS = PASSES.flatMap(p => p.rows || []);
const PASS_DIV = PASSES.flatMap(p => p.items || []);
const PASS_DIV_IDS = new Set(PASS_DIV.map(d => d.unit + '|' + d.sourceId));
// attributions (passes/attributions.json): each marks exactly one published row
const ATTR = PASSES.flatMap(p => p.attributions || []);
// collection row field -> viewer row field
const FIELD = { unit: 'sec', family: 'fam', work: 'work', locus: 'locus', page: 'page', inNote: 'note', label: 'label', confidence: 'conf',
                status: 'status', step: 'step', passage: 'vp', source: 'sp', reason: 'reason', links: 'links', earliest: 'ew', quoting: 'qa' };

(async () => {
  const browser = await chromium.launch();
  const grab = async url => {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(url);
    await page.waitForFunction(() => typeof SEC !== 'undefined' && SEC.length > 0 && document.querySelector('#page .sec'), null, { timeout: 60000 });
    const got = await page.evaluate(() => ({
      sec: SEC.map(s => ({ id: s.id, fs: s.fs, book: s.book, chap: s.chap, para: s.para, margin: s.margin, html: s.html, notes: s.notes,
                           pages: s.pages, vars: s.vars, unnum: s.unnum, citedBy: s.citedBy, en: s.en, div: s.div, plain: s.en ? plainOf(s) : undefined })),
      rows: ROWS.map(r => r),
    }));
    await page.close();
    got.errors = errors;
    return got;
  };
  // 1. the edition as the working edition built it (later passes swapped back for the rows they replaced): exact rebuild of data.json
  const got = await grab(base + 'viewer/?ed=' + ed + '&asbuilt=1');
  // 2. the edition as published: the rows of later passes
  const pub = PASSES.length ? await grab(base + 'viewer/?ed=' + ed) : null;
  await browser.close();

  const bad = {};
  const fail = (k, id) => { (bad[k] = bad[k] || []).push(id); };
  if (got.sec.length !== D.sections.length) fail('count', got.sec.length + ' vs ' + D.sections.length);
  D.sections.forEach((s, i) => {
    const g = got.sec[i] || {};
    for (const k of ['id', 'chap', 'para', 'margin', 'html', 'citedBy', 'pages'])
      if (!same(s[k], g[k])) fail(k, s.id);
    if ('book' in s && s.book !== g.book) fail('book', s.id);
    if ('part' in s && s.part !== (Number(String(g.book).slice(1)) || 0)) fail('part', s.id);
    for (const k of ['vars', 'unnum'])
      if (k in s && !same(s[k], g[k])) fail(k, s.id);
    if (!same(s.notes.map(n => [n.mark, n.html, !!n.added]), (g.notes || []).map(n => [n.mark, n.html, !!n.added]))) fail('notes', s.id);
    // a translation layer added after the working edition (Burlamaqui's English) is not in data.json
    if ((HAS_EN || 'en' in s) && !same(s.en, g.en)) fail('en', s.id);
    if (s.en && !same(s.fs, g.fs)) fail('fs', s.id);
    if (g.en && (!g.fs || g.fs.some(([a, b]) => a < 0 || b > (g.plain || '').length || a >= b))) fail('en spans', s.id);
    const gdiv = (g.div || []).filter(d => !PASS_DIV_IDS.has(s.id + '|' + d.wid));
    if (!same(s.div, gdiv.length ? gdiv : undefined)) fail('div', s.id);
  });
  D.rows.forEach(r => {
    const g = got.rows[r.id];
    if (!g) return fail('row missing', r.id);
    for (const k of Object.keys(r)) if (!same(r[k], g[k])) fail('row.' + k, r.id);
    for (const k of Object.keys(g)) if (!(k in r) && !ADDED.includes(k)) fail('row extra.' + k, r.id);
  });
  if (got.rows.filter(Boolean).length !== D.rows.length) fail('row count', got.rows.length);
  if (got.errors.length) fail('page errors', got.errors.join(' | '));
  if (pub) {
    PASS_ROWS.forEach(r => {
      const g = pub.rows[r.id];
      if (!g) return fail('pass row missing', r.id);
      for (const [k, v] of Object.entries(FIELD)) if (!same(r[k], g[v])) fail('pass row.' + k, r.id);
      if (g.where !== (r.at.length ? r.at[0][0] : r.where === 'margin' ? 'm' : '')) fail('pass row.where', r.id);
      const s = pub.sec.find(s => s.id === r.unit) || { html: '', notes: [] };
      const html = r.at.length ? (r.at[0][0] === 't' ? s.html : (s.notes[Number(r.at[0][0].slice(1))] || {}).html || '') : null;
      if (html !== null && !new RegExp(`data-m="(?:[\\d,]*,)?${r.id}(?:,[\\d,]*)?"`).test(html)) fail('pass row not marked', r.id);
    });
    if (pub.rows.filter(Boolean).length !== D.rows.length - SUPERSEDED.size + PASS_ROWS.length) fail('published row count', pub.rows.filter(Boolean).length);
    const n = pub.sec.reduce((a, s) => a + (s.div || []).length, 0);
    if (n !== D.sections.reduce((a, s) => a + (s.div || []).length, 0) + PASS_DIV.length) fail('published divergence count', n);
    if (pub.errors.length) fail('published page errors', pub.errors.join(' | '));
    ATTR.forEach(a => {
      const hits = pub.rows.filter(r => r && r.to === a.text && r.sec === a.unit && r.page === a.page && r.vp === a.passage && r.sp === a.source);
      if (hits.length !== 1 || !hits[0].attr || hits[0].attr.cue !== a.cue) fail('attribution not on its row', a.unit + ' ' + a.text);
    });
    if (pub.rows.filter(r => r && r.attr).length !== ATTR.length) fail('attributed row count', pub.rows.filter(r => r && r.attr).length + ' vs ' + ATTR.length);
  }
  const n = Object.keys(bad).length;
  console.log(n ? 'MISMATCH' : 'OK', `${ed}: ${D.sections.length} units, ${D.rows.length} reuse rows compared with data.json` +
    (PASSES.length ? `; ${PASS_ROWS.length} rows, ${PASS_DIV.length} divergence items and ${ATTR.length} attributions of ${PASSES.length} later pass file(s), replacing ${SUPERSEDED.size} rows` : ''));
  for (const [k, ids] of Object.entries(bad)) console.log(' ', k, ids.length, ids.slice(0, 8).join(' '));
  process.exit(n ? 1 : 0);
})();
