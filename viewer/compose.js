// Build a unit's display HTML from its plain text and standoff marks.
// Runs of characters with the same marks become one element, as in the original build (build_data.py).
(function (root) {
  const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;' };
  const esc = s => String(s).replace(/[&<>"']/g, c => ESC[c]);

  // part: {text, i:[[a,b]], xr:[[a,b,target]]}
  // reuse: [[a,b,rowId]]; vars: [[a,b,variantId]]; breaks: {pos: html}; famOf: rowId -> family key
  function renderPart(part, reuse, vars, breaks, famOf) {
    const t = part.text, n = t.length;
    const ital = new Uint8Array(n), ref = new Array(n).fill(''), addv = new Array(n).fill('');
    const cover = new Array(n);
    for (const [a, b] of part.i || []) for (let k = a; k < b && k < n; k++) ital[k] = 1;
    for (const [a, b, x] of part.xr || []) for (let k = a; k < b && k < n; k++) ref[k] = x;
    for (const [a, b, v] of vars) for (let k = a; k < b && k < n; k++) addv[k] = v;
    for (const [a, b, id] of reuse) for (let k = a; k < b && k < n; k++) (cover[k] = cover[k] || []).push(id);
    const ckey = new Array(n);
    for (let k = 0; k < n; k++) ckey[k] = cover[k] ? cover[k].sort((x, y) => x - y).join(',') : '';
    const sig = k => ckey[k] + '|' + addv[k] + '|' + ref[k] + '|' + ital[k];
    let out = '', i = 0;
    while (i < n) {
      if (breaks[i] !== undefined) out += breaks[i];
      let j = i + 1;
      const s = sig(i);
      while (j < n && breaks[j] === undefined && sig(j) === s) j++;
      let h = esc(t.slice(i, j));
      if (ital[i]) h = `<i>${h}</i>`;
      if (ref[i]) h = `<a class="xr" href="#${ref[i]}">${h}</a>`;
      if (ckey[i]) {
        const fams = [...new Set(cover[i].map(famOf))].sort().join(' ');
        h = `<span class="u" data-m="${ckey[i]}" data-f="${fams}">${h}</span>`;
      }
      if (addv[i]) h = `<span class="var" data-v="${addv[i]}">${h}</span>`;
      out += h; i = j;
    }
    if (breaks[n] !== undefined) out += breaks[n];
    return out;
  }

  // unit: a record of text.json; marks: {reuse:{part:[[a,b,id]]}, vars:{part:[[a,b,vid]]}, old:{part:{pos:[html]}}}
  // pageBreak: HTML template for a page break, with {vol}, {scan} and {printed}
  const PB = '<span class="pb" data-pg="{vol}:{scan}"> {vol} p. {printed} </span>';
  function composeUnit(unit, marks, famOf, pageBreak) {
    const get = (o, p) => (o && o[p]) || [];
    const tb = {};
    const add = (b, pos, h) => { b[pos] = (b[pos] || '') + h; };
    for (const k of unit.para || []) if (k > 0 && k < unit.text.length) add(tb, k, '<span class="para"></span>');
    const oldT = (marks.old && marks.old.t) || {};
    const pbAt = {};
    for (const [at, vol, scan, printed] of unit.pb || [])
      pbAt[at] = (pageBreak || PB).replace(/\{(vol|scan|printed)\}/g, (m, k) => k === 'printed' ? esc(printed) : k === 'vol' ? vol : scan);
    const pos = new Set([...Object.keys(oldT), ...Object.keys(pbAt)].map(Number));
    for (const p of pos) { for (const h of oldT[p] || []) add(tb, p, h); if (pbAt[p]) add(tb, p, pbAt[p]); }
    const html = renderPart(unit, get(marks.reuse, 't'), get(marks.vars, 't'), tb, famOf);
    const notes = (unit.notes || []).map((nt, ni) => {
      const p = 'n' + ni, nb = {};
      const oldN = (marks.old && marks.old[p]) || {};
      for (const q of Object.keys(oldN)) for (const h of oldN[q]) add(nb, Number(q), h);
      return { mark: nt.mark, html: renderPart(nt, get(marks.reuse, p), get(marks.vars, p), nb, famOf) };
    });
    return { html, notes };
  }

  const api = { esc, renderPart, composeUnit };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Compose = api;
})(this);
