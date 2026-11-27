# Source transcription and reuse passes

The scripts that made the vision transcriptions in `texts/` and the later passes in `editions/<edition>/passes/`. They read and write a working folder outside the repository: `NLE_WORK`, default `work/` at the repository root (git ignores it). Language-model steps run as agents, one batch each, with the prompts in this folder. `<WORK>` and `<TOOLS>` in a prompt stand for the working folder and this folder.

Needs Python 3, PyMuPDF and NLTK (French Snowball stemmer).

## 1. Scans

- `render2.py <pdf> <WORK>/scans/img/<SIGLUM>`: every page trimmed to its printed area, at most 1300 × 1560 px, grayscale, with `clips.json` for the crops. PDF annotations (a reader's highlights) are not drawn. The PDF is the archive.org item's PDF; page numbers are PDF pages.
- `crop2.py <SIGLUM> <page> <x0> <y0> <x1> <y1>`: a region of a page at high resolution, for the small type of notes and margins.
- archive.org's OCR of the same item (`<item>_hocr_pageindex.json.gz`, `<item>_hocr_searchtext.txt.gz`) goes to `<WORK>/scans/ocr/<SIGLUM>_…`. It serves the checks only.

## 2. Transcription

- Agent prompt `TRANSCRIBE_PROMPT.md`, ten scans per agent: "Your range: SIGLUM <SIGLUM>, scans <a> to <b>." Each page goes to `<WORK>/tr/<SIGLUM>/s<NNNN>.json`. An agent skips pages already written, so a batch cut short is run again as it was.
- `TRANSCRIBE_PROMPT_DEVOIRS.md`: the same for Pufendorf's *Devoirs* (1756), twenty scans per agent: one-column pages, lettered Latin glosses in the margin, and the kinds of the other works in vol. II.
- `TRANSCRIBE_PROMPT_WOLFF.md`: the prompt of the earlier Wolff run (*Jus gentium*, *Institutiones*; 24 scans per agent, Google Books scans). Its paths are those of that run.
- `validate.py <work>` (`GRO24`, `PUF34`): the § and chapter markers run in sequence; running heads agree with the chapter; no scan is missing.
- `fix_markers.py <SIGLUM>… [--write]`: where a § or chapter marker is missing, puts it before the printed "§. ROMAN." or "CHAPITRE ROMAN" line. Without `--write` it only lists the changes.
- `qc_ocr.py <SIGLUM>…` and `qc_shingle.py <SIGLUM>…`: each page against archive.org's OCR of the same scan (words of five letters or more; 8-letter sequences). `ocr_index.py` finds the leaf offset between OCR and scans (the OCR of a Toronto scan counts its colour card).
- `qc_wolff.py <pages> <drive text>`: the Wolff pages against the Google Books OCR of the same PDF, as Google Drive gives it (the first pages only).
- `export_tr.py <text id> <SIGLUM>…`: the pages, one file per volume, into `texts/<text id>/<SIGLUM>.json`.
- Vattel's *Défense* (DEF41): `TRANSCRIBE_PROMPT_DEF41.md`, `CHECK_PROMPT_DEF41.md` (second reading), `qc_def41.py`, `fix_def41.py`, `export_def41.py`; units `def41_data.py`; gold set of citations `GOLD_PROMPT_DEF41.md`, `gold_def41.py`.
- Wolff's *Psychologia rationalis* (PSR34): `TRANSCRIBE_PROMPT_PSR34.md`, `CHECK_PROMPT_PSR34.md`, `fix_psr34.py` (catchword lines, double s, space before comma; logged), `qc_psr34.py [--export]`.
- `ROQUES_QUOTES_PROMPT.md` and `roques_quoted.py <data.json> <reader outputs>…`: Roques's letters as Vattel quotes them in the *Défense*, Partie II ch. VIII (`texts/roques-lettres-1737-1739/`).
- Défense reuse pass (step 4): `def41_cand.py <data.json> <out> [10] [0.06]` (candidates and judge batches), `DEF41_JUDGE_PROMPT.md` (Sonnet judges), `def41_checkbatch.py` and `DEF41_CHECK_PROMPT.md` (Opus check of doubtful rows), `def41_merge.py <batches> <judge> <check>` (rows into `editions/vattel-defense-1741/provenance/reuse/`).
- Défense divergences (step 5): `def41_div.py <batches> <out> [12]` (screen batches: units reusing Leibniz or Wolff, with the segments their rows name), `DEF41_DIV_SCREEN_PROMPT.md` (Sonnet), `def41_div_verify.py` and `DEF41_DIV_VERIFY_PROMPT.md` (Opus), `def41_div_write.py <batches> <verify>` (`editions/vattel-defense-1741/provenance/divergences.json`).
- `crousaz_ocr.py`: Crousaz's *Examen* (1737) and *Commentaire* (1738) by printed page from the Google OCR text layer of the PDFs in `<WORK>/scans/pdf/` (`texts/crousaz-examen-1737/`, `texts/crousaz-commentaire-1738/`).
- `theodicee_text.py <epub> <vol I leaves> <vol II leaves> <out>`: Leibniz's *Théodicée* by section from the Wikisource EPUB, each section linked to its leaf in the 1734 edition (`texts/leibniz-theodicee-1734/`).

## 3. Corpus

- `corpus.py <work>`: the pages of a work in reading form (long s as s, line-end hyphens joined, tags dropped) with a locus for every stretch of main text, margin note and footnote ("Liv. II ch. XV § 8", "…, n. 4", "Discours préliminaire § 17"). Front matter is set by scan in `WORKS`. Writes `<WORK>/corpus/<work>.json`.

## 4. Reuse pass

- `retrieve.py <edition> <work> <old table> <out>`: candidate pages for every unit. Stemmed French skip-bigrams and tf-idf, z-scored per unit; the top two pages, the best skip-bigram page, and the pages the old table's rows name.
- `shared_scan.py <edition> <work> <out>`: every unit against every part of the source: runs of five or more words in common (accents folded), kept when one of their 5-word strings occurs at most twice in the source and twice in the edition (`shared.py`).
- `prep_shared.py <candidates> <shared> <judge dir or -> <new candidates> <recheck>`: adds to a unit's candidates the pages it shares a long run with (one run of 7+ words, or 11+ in all; at most three); for units already judged, lists the pages with runs no match covers.
- `build_judge.py <edition> <work> <candidates> <dir> [10] [shared or -] [earlier]`: judge batches of ten consecutive units with their pages, each page cut into parts (text, margin, notes with their author). With the shared file, each item lists its runs on its candidate pages, for the judge to check. With the earlier file, each item lists the pairs an earlier pass found.
- Agent prompt `JUDGE_PROMPT.md`, one batch per agent: matches with exact passages on both sides, a label and a confidence.
- `build_expand.py <edition> <work> <judge dirs> <candidates files> <out> [hints]` (lists comma-separated): the second pass. Pages a unit cites (by book, chapter and §, each reference given to the author named nearest before it), pages judges named for an item they could not match (hints), the source § nearest the unit by tf-idf when its cosine reaches 0.30 (0.40 for a unit already matched), and, for units with no match, the pages next to a neighbour's match. At most three new pages per unit.
- `merge.py <edition> <work> <judge dirs, comma-separated> <old table> <first id> <out>`: places every passage in the edition and the source part (exact, free whitespace, or fuzzy ≥ 0.9), sets locus, family (Bb for Barbeyrac's notes), links and status (match ≥ 0.5, possible 0.3–0.5), drops rows under 0.3 and duplicates, and carries `earliest` over from an old row on the same span.
- `cmp_old.py <old table> <rows>`: how many old rows the new rows cover.
- `map_old.py <old table> <work> <out>`: for an old table whose page ids the corpus does not have (the *Devoirs* vol. II OCR came in chunks), the corpus page that shares most 8-letter sequences with each row's source passage.
- `prep_earlier.py <old table> <rows> <candidates> <earlier>`: the old match rows no new row overlaps, as candidates and pointers for a recheck batch (`build_judge.py … - <earlier>`).
- `build_review.py <edition> <work> <rows> <dir> [15]`: the rows at status possible, each with the edition part and the source part that hold its passages, for a second judge. `keys.json` ties each verdict to the row's unit, page and passages.
- Agent prompt `REVIEW_PROMPT.md`, one batch per agent: keep (with a label and a confidence), commonplace, or drop.
- `apply_review.py <rows> <review dirs, comma-separated> <out>`: drop removes the row; commonplace sets the label and leaves the row possible; keep sets the label and the second judge's confidence (match ≥ 0.5, possible 0.3–0.5, gone under 0.3). Each reviewed row keeps the verdict in `review`.
- `make_pass.py <edition> <text id> <rows> <step label> <text layer>`: writes `editions/<edition>/passes/<text id>.json`.

## 5. Divergences

- `build_div.py <work> <rows> <candidates> <dir> [edition]`: for each § of the edition (default `vattel-1773`) with a match, the source §§ it reuses and the nearest other §. Item keys carry the author's name (`vattel_id`, `burlamaqui_id`).
- Agent prompt `DIV_SCREEN_PROMPT_<work>.md` (`GRO24`, `PUF34`; `GRO24_BURLAMAQUI`, `PUF34_BURLAMAQUI`, `DEV56_BURLAMAQUI` for Burlamaqui): does the source answer the same question, and does the edition answer it differently.
- `div_already.py <batch dir> <divergence pass> <field>`: adds to each screen or verify item the notes an earlier pass holds for its unit (the *Devoirs* screen gets the DNG notes as `dng_notes` and leaves out what they record).
- `build_verify.py <screen dir> <dir>`: the flagged pairs with the whole source § and Barbeyrac's notes. A pair the screen names outside its candidates can be added by hand as an extra screen file.
- Agent prompt `DIV_VERIFY_PROMPT_<work>.md`: keep or reject, relation, severity and a comment.
- `write_div.py <work> <screen dir> <verify dir> <text id> <out> [date]`: writes `editions/<edition>/passes/divergences-<text id>.json`.
- Essai (all seven sources in one pass): `essai_div.py <dir>` builds the screen batches (each § with the source sections its reuse rows and its neighbours' use, and the two nearest by vocabulary per French source; `<dir>/sections.json` holds every source section for the readers' own searches). Agent prompt `ESSAI_DIV_SCREEN_PROMPT.md`. `essai_div_verify.py <screen dir> <dir>` takes the flagged pairs to `ESSAI_DIV_VERIFY_PROMPT.md`. `essai_div_write.py <screen dir> <verify dir> <date> --write` writes one `passes/divergences-<text id>.json` per source.

## 6. Attributions

- `attr_cand.py <out>`: the reuse rows of both editions (not citation, not commonplace) whose unit names the source's author or work anywhere in text, notes or margin. Name patterns per source text, accents folded.
- `build_attr.py <candidates> <dir> [30]`: batches of about 30 rows, grouped by unit; each unit with its margin, text and notes. `keys.json` ties each key to the row.
- Agent prompt `ATTRIBUTION_PROMPT.md`, one batch per agent: does the author name the source for this passage (its sentence, the sentence that introduces it, a note called there, the margin beside it); form quotation or reference; the words that name it.
- `write_attr.py <dir> [date]`: the attributed verdicts whose cue is found in the unit go to `editions/<edition>/passes/attributions.json`. The converters copy each onto its row as `attributed`.

- Agent prompt `ATTRIBUTION_VERIFY_PROMPT.md` (Claude Opus, about 16 rows per agent): a second reading of each attribution with the whole unit; correct, wrong or unsure.
- `apply_attr.py <items> <dir>`: wrong items leave `attributions.json`; kept items take the second reader's form and cue and carry the verdict in `review`. Unsure items stay for a decision by hand.

## 7. Footnotes on the wrong section (Vattel)

- `note_clusters.py <out>`: the sections whose number of footnote calls differs from their number of notes, grouped with their neighbours on shared printed pages, with the MDZ scan of each page.
- Agent prompt `NOTE_PAGE_PROMPT.md`, about 20 pages per agent: for each note, the page at whose foot it stands and the call it answers.
- `note_moves.py <dir> <corrections>`: the certain answers whose two sections share a page become `noteMoves` in `editions/vattel-1773/corrections.json`.
- `migrate_notes.py <data.json> <edition> [--since K] [--write]`: remaps the later-pass files that point into notes (pass rows, attributions, divergence items) to the corrected numbering. Run once after the corrections change.

## 8. English of Burlamaqui

- `en_extract.py <pdf> <out>`: Nugent's translation from the Liberty Fund PDF, by section, with Burlamaqui's notes; the editor's notes and their calls are left out.
- `en_align.py <units_en> <plain_fr> <text.json> <out>`: sentence alignment with the 1747 French, chapter by chapter (Gale–Church lengths; Nugent's § numbers as anchors). Writes `layers/english.json`. `plain_fr` is each unit's plain text as the viewer builds it (`plain_fr.js <out>`).

- `en_flags.py batches <layer> <plain_fr> <dir>` and `en_flags.py merge <layer> <dir>`: the translation check. Agent prompt `TRANSLATE_CHECK_PROMPT_BURLAMAQUI.md`, 28 units per agent: mistranslation, shift, omission, addition, terminology and false friends that matter to an intellectual historian. The merge keeps the flags whose phrases stand in their pair.

## 9. Audits

- `prec_sample.py`: the random sample of the precision audit (`audit/`). Agent prompt `PRECISION_PROMPT.md` (Claude Opus): right, weak or wrong, and whether the label fits.
- Agent prompt `REJUDGE_PROMPT.md` (Claude Opus, 25 rows per agent): the same task for every match row of a table, with a note that Vattel often follows Wolff or Grotius where Pufendorf or Burlamaqui say the same.
- `label_overlap.py`: the word overlap of each row's passage and source passage (French sources), for the label check. Agent prompt `LABEL_CHECK_PROMPT.md` (Claude Opus, 30 rows per agent): the label that fits.
- `apply_rejudge.py <work> <repo> <vattel data.json> <burlamaqui data.json> [--write]`: re-judge verdicts go in `audit` (weak match rows become possible, wrong rows `rejected`), label-check changes in `labelCheck`. Pass rows are edited in their pass files, working rows through `corrections.json` (`rowEdits`). Run once.
- `demote_weak.py <repo> [--write]`: match rows an audit rated weak become possible.
- `prec2_sample.py <dir>` and `prec2_stats.py <dir>`: the second precision sample (match rows no audit had read) and its estimate. Agent prompt `PRECISION_PROMPT.md`.
- `wolff_loci.py <work>`: places each Wolff row's source passage in the transcription and compares the § it stands in with the row's locus.
- `apply_checks2.py <work> <repo> <vattel data.json> <burlamaqui data.json> [--write]`: applies the second sample, the locus corrections (`locusCheck`) and the rows the recall readers judged wrong.
- `src_pages.py <out>`: reading-form pages of Wolff's *Jus gentium*, *Institutiones*, *Philosophia practica universalis* I, *Theologia naturalis* I and *Discursus praeliminaris* (long s as s, hyphens joined) with the offset where each § starts, for the readers below.
- `add_cand.py <work> <out>`: the weak rows whose audit reason names a passage of Wolff or Grotius that the section has no row for, in batches by section. Agent prompt `ADDITIONS_PROMPT.md` (Claude Opus, about 14 sections per agent).
- `recall_cand.py <out> [n]`: a random sample of Vattel's sections with their rows and the source pages cited nearby. Agent prompt `RECALL_PROMPT.md` (Claude Opus, 3 sections per agent). `rec_stats.py <dir>`: the share of found reuse that rows cover.
- `add_merge.py <work> <first id> <date> <out> A:<dir> C:<dir> V:<dir> [--append]`: the rows the additions, recall and 1773-additions readers wrote become `editions/vattel-1773/passes/additions.json`, each placed on its unit and its source page, duplicates left out; `--append` keeps the rows already there.
- `add73_cand.py <out> [per]`: the passages Vattel added in 1773 (layer `changes-1773`, additions with text), with their sections and the rows that already overlap them. Agent prompt `ADDITIONS_1773_PROMPT.md` (Claude Opus, 8 additions per agent; sources JG, INST, GRO24, PUF34 and BUR47). The readers also list the sources Vattel names there that the corpus lacks (`audit/additions-1773-2026-11-20.json`).

## 10. Vattel, Essai sur le fondement du droit naturel (1747)

- Transcription: the Loisir philosophique PDF rendered by `render2.py`; Claude Sonnet, 17 pages per agent, prompt `TRANSCRIBE_PROMPT_LOISIR.md`. Wolff's *Philosophia practica universalis* I from MDZ: `mdz_img.py` (page images), `mdz_ocr.py` (MDZ OCR, used to map the chapters), `mdz_crop.py` (full-resolution crops for the readers); Claude Sonnet, about 24 pages per agent, prompt `TRANSCRIBE_PROMPT_PPU.md`.
- `essai_data.py <LOI47.json> <data.json>`: the working edition (sections by printed paragraph number, page breaks, footnotes on the section that calls them). `tools/convert_vattel_essai_1747.py <data.json>` converts it.
- English: `en_extract_essai.py <pdf> <out>` (Liberty Fund 2008, pp. 747–772), `plain_ed.js <edition> <out>` (each unit's plain text as the viewer builds it), `en_align_essai.py` (sentence alignment over the whole essay). Translation check: `en_flags.py` with `TRANSLATE_CHECK_PROMPT_ESSAI.md` (Claude Opus, 10 sections per agent).
- Reuse: `src_pages.py` (reading pages of Wolff, with the offset of each §), `essai_cand.py <work> <out>` (each section with the 8 nearest pages of each French source), readers with `ESSAI_REUSE_PROMPT.md` (Claude Opus, 4 sections per agent; they search Wolff's Latin themselves with the index of his marginal summaries), `essai_merge.py <work> <dir> <date> --write` (pass files and `attributions.json`).
- Second reading: `essai_verify.py <out> [status]` (every match row, or every row of another status, batches of 25), readers with `VERIFY_PROMPT_ESSAI.md` (Claude Opus), `essai_apply_verify.py <dir> <date> --write`.
- Second copy: the Zürich copy on e-rara; readers with `PAGE_CHECK_PROMPT_LOISIR.md` (Claude Sonnet, 17 pages per agent) compare each page image with the transcription.
- Wolff's *Theologia naturalis* I (§§ 948–1006) and *Discursus praeliminaris* (§§ 1–171) from MDZ, as the *Philosophia practica*: prompts `TRANSCRIBE_PROMPT_TN1.md` and `TRANSCRIBE_PROMPT_LOG40.md`. Readers with `ESSAI_WOLFF2_PROMPT.md` (Claude Opus, about 10 sections per agent), then `essai_merge.py <work> <dir> <date> --write --only TN1,LOG40`.

- Full pass (2026-11-21): `full_cand.py <out> [chars]` (every section with its Jus gentium §§ and Pufendorf pages, batches by size), readers with `FULL_PASS_PROMPT.md` (Claude Opus), `add_merge.py <work> <first id> <date> <out> F:<dir> --append`. Second reading: `fullpass_check.py <dir> <out> [n match] [n possible]` (rows the readers judged wrong and a random sample of the new rows), readers with `PRECISION_PROMPT.md`, `fullpass_apply.py <dir> <date> <vattel data.json> --write`. The added rows of earlier steps: `addv_items.py <out>`, `addv_apply.py <dir> <date> --write`.
- `wolff_loci2.py <work>`: places Wolff rows whose source passage comes from the old text layer (et/&, ae, j/i, v/u folded) and lists those whose locus names another §.

## 11. Text corrections and offsets

- `remap_text.py <edition> <old text.json> [--base <layer>=<json>] [--layers a,b] [--write]`: after a change to an edition's text, moves the offsets of pass rows, attributions and static layers to the new text through a character diff of each part, and reads each passage again from the new text.
- `tools/migrate_pb_spaces.py <data.json> <edition> '<old page-break template>'` (2026-11-20, once): the working editions of Vattel 1773 and Burlamaqui dropped the space between the two words around a page break; this restores it in data.json and moves the English sentence spans.

## 12. Translations of foreign-language passages

- `gloss_cand.py <out>`: a character-trigram model of Latin (Wolff's transcriptions), French (the editions) and English (the English layers) marks runs of three or more words that read as Latin or English, and any Greek letter; units with candidates go in batches of about 40 stretches. Readers with `GLOSS_PROMPT.md` (Claude Opus) fix each passage's extent, its language and an English translation, and skip references and French. `gloss_merge.py <dir> <date> --write`: `editions/<ed>/layers/glosses.json` and the layer's entry in `edition.json`.

The converters then rebuild the editions from their working `data.json` and the pass files (`tools/convert_*.py`, `tools/nle.py`); `tools/check_all.sh` checks both.
