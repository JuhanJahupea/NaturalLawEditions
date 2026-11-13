// plain_fr.js <out> [viewer base URL]: each Burlamaqui unit's plain text as the viewer builds it (plainOf), for en_align.py.
// Serve the repository first (python -m http.server 8000). Needs Playwright with Chromium.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const base = process.argv[3] || 'http://localhost:8000/';
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto(base + 'viewer/?ed=burlamaqui-1747');
  await p.waitForFunction(() => typeof SEC !== 'undefined' && SEC.length > 0 && document.querySelector('#page .sec'), null, {timeout: 60000});
  const out = await p.evaluate(() => Object.fromEntries(SEC.map(s => [s.id, plainOf(s)])));
  fs.writeFileSync(process.argv[2], JSON.stringify(out)); console.log(Object.keys(out).length);
  await b.close();
})();
