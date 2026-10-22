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
// fields the collection adds to a row
const ADDED = ['to', 'toUnit', 'relation', 'rep'];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + 'viewer/?ed=' + ed);
  await page.waitForFunction(() => typeof SEC !== 'undefined' && SEC.length > 0 && document.querySelector('#page .sec'), null, { timeout: 60000 });
  const got = await page.evaluate(() => ({
    sec: SEC.map(s => ({ id: s.id, fs: s.fs, book: s.book, chap: s.chap, para: s.para, margin: s.margin, html: s.html, notes: s.notes,
                         pages: s.pages, vars: s.vars, unnum: s.unnum, citedBy: s.citedBy, en: s.en, div: s.div })),
    rows: ROWS.map(r => r),
  }));
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
    if (!same(s.en, g.en)) fail('en', s.id);
    if (s.en && !same(s.fs, g.fs)) fail('fs', s.id);
    if (!same(s.div, g.div)) fail('div', s.id);
  });
  D.rows.forEach(r => {
    const g = got.rows[r.id];
    if (!g) return fail('row missing', r.id);
    for (const k of Object.keys(r)) if (!same(r[k], g[k])) fail('row.' + k, r.id);
    for (const k of Object.keys(g)) if (!(k in r) && !ADDED.includes(k)) fail('row extra.' + k, r.id);
  });
  if (got.rows.filter(Boolean).length !== D.rows.length) fail('row count', got.rows.length);
  if (errors.length) fail('page errors', errors.join(' | '));
  const n = Object.keys(bad).length;
  console.log(n ? 'MISMATCH' : 'OK', `${ed}: ${D.sections.length} units, ${D.rows.length} reuse rows compared`);
  for (const [k, ids] of Object.entries(bad)) console.log(' ', k, ids.length, ids.slice(0, 8).join(' '));
  process.exit(n ? 1 : 0);
})();
