# Source transcription and reuse passes

The scripts that made the vision transcriptions in `texts/` and the later passes in `editions/<edition>/passes/`. They read and write a working folder outside the repository: `NLE_WORK`, default `work/` at the repository root (git ignores it). Language-model steps run as agents, one batch each, with the prompts in this folder. `<WORK>` and `<TOOLS>` in a prompt stand for the working folder and this folder.

Needs Python 3, PyMuPDF and NLTK (French Snowball stemmer).

## 1. Scans

- `render2.py <pdf> <WORK>/scans/img/<SIGLUM>`: every page trimmed to its printed area, at most 1300 × 1560 px, grayscale, with `clips.json` for the crops. The PDF is the archive.org item's PDF; page numbers are PDF pages.
- `crop2.py <SIGLUM> <page> <x0> <y0> <x1> <y1>`: a region of a page at high resolution, for the small type of notes and margins.
- archive.org's OCR of the same item (`<item>_hocr_pageindex.json.gz`, `<item>_hocr_searchtext.txt.gz`) goes to `<WORK>/scans/ocr/<SIGLUM>_…`. It serves the checks only.

## 2. Transcription

- Agent prompt `TRANSCRIBE_PROMPT.md`, ten scans per agent: "Your range: SIGLUM <SIGLUM>, scans <a> to <b>." Each page goes to `<WORK>/tr/<SIGLUM>/s<NNNN>.json`. An agent skips pages already written, so a batch cut short is run again as it was.
- `validate.py <work>` (`GRO24`, `PUF34`): the § and chapter markers run in sequence; running heads agree with the chapter; no scan is missing.
- `qc_ocr.py <SIGLUM>…` and `qc_shingle.py <SIGLUM>…`: each page against archive.org's OCR of the same scan (words of five letters or more; 8-letter sequences). `ocr_index.py` finds the leaf offset between OCR and scans (the OCR of a Toronto scan counts its colour card).
- `export_tr.py <text id> <SIGLUM>…`: the pages, one file per volume, into `texts/<text id>/<SIGLUM>.json`.

## 3. Corpus

- `corpus.py <work>`: the pages of a work in reading form (long s as s, line-end hyphens joined, tags dropped) with a locus for every stretch of main text, margin note and footnote ("Liv. II ch. XV § 8", "…, n. 4", "Discours préliminaire § 17"). Front matter is set by scan in `WORKS`. Writes `<WORK>/corpus/<work>.json`.

## 4. Reuse pass

- `retrieve.py <edition> <work> <old table> <out>`: candidate pages for every unit. Stemmed French skip-bigrams and tf-idf, z-scored per unit; the top two pages, the best skip-bigram page, and the pages the old table's rows name.
- `build_judge.py <edition> <work> <candidates> <dir> [10]`: judge batches of ten consecutive units with their pages, each page cut into parts (text, margin, notes with their author).
- Agent prompt `JUDGE_PROMPT.md`, one batch per agent: matches with exact passages on both sides, a label and a confidence.
- `build_expand.py <edition> <work> <judge dir> <candidates> <out> [hints]`: the second pass. Pages a unit cites (by book, chapter and §, each reference given to the author named nearest before it), pages judges named for an item they could not match (hints), the source § nearest the unit by tf-idf when its cosine reaches 0.30 (0.40 for a unit already matched), and, for units with no match, the pages next to a neighbour's match. At most three new pages per unit.
- `merge.py <edition> <work> <judge dirs, comma-separated> <old table> <first id> <out>`: places every passage in the edition and the source part (exact, free whitespace, or fuzzy ≥ 0.9), sets locus, family (Bb for Barbeyrac's notes), links and status (match ≥ 0.5, possible 0.3–0.5), drops rows under 0.3 and duplicates, and carries `earliest` over from an old row on the same span.
- `cmp_old.py <old table> <rows>`: how many old rows the new rows cover.
- `make_pass.py <edition> <text id> <rows> <step label> <text layer>`: writes `editions/<edition>/passes/<text id>.json`.

## 5. Divergences

- `build_div.py <work> <rows> <candidates> <dir>`: for each Vattel § with a match, the source §§ it reuses and the nearest other §.
- Agent prompt `DIV_SCREEN_PROMPT.md`: does the source answer the same question, and does Vattel answer it differently.
- `build_verify.py <screen dir> <dir>`: the flagged pairs with the whole source § and Barbeyrac's notes.
- Agent prompt `DIV_VERIFY_PROMPT.md`: keep or reject, relation, severity and a comment.
- `write_div.py <screen dir> <verify dir> <text id> <out>`: writes `editions/vattel-1773/passes/divergences-<text id>.json`.

The converters then rebuild the editions from their working `data.json` and the pass files (`tools/convert_*.py`, `tools/nle.py`); `tools/check_all.sh` checks both.
