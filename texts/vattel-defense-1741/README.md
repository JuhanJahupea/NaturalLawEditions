# Vattel, *Défense du système leibnitien contre les objections et les imputations de Mr. de Crousaz* (Leide, Jean Luzac, 1741)

Page transcription of the whole book: the title page, the dedication to the King of Prussia (10 pp.), the Préface (48 pp.), the text (pp. 1–592, paragraphs 1–409), and the fold-out table. The edition `editions/vattel-defense-1741/` will be built from it. The witness, the scan map and the errata are in `editions/vattel-defense-1741/provenance/`.

| File | Pages | Copy | Contents |
|---|---|---|---|
| `DEF41.json` | 652 | BCU Lausanne copy (earlier Biblioteka Peczarska), Google Books PDF of 708 scans supplied by the editor; the same copy is on archive.org as [dfensedusystmel00luzagoog](https://archive.org/details/dfensedusystmel00luzagoog) | title, dedication, Préface, pp. 1–592 without pp. 458–459, fold-out table |

## Method

- Claude Sonnet subagents, about 24 pages each, read each page image (at most 1300 × 1560 px, PDF annotations left out). Prompt: `tools/transcription/TRANSCRIBE_PROMPT_DEF41.md`. A pilot of 9 pages came first.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed, misprints kept; long s as `ſ`; quotation marks at the start of quoted lines kept; line breaks and line-end hyphens kept; italics as `<i>…</i>` (the dedication and the Préface are set in italics, with roman for emphasis).
- `body` has marker lines `<<PARTIE n>>`, `<<CHAP n>>`, `<<SECTION n>>` (Partie II, ch. VIII), `<<§ n>>` (the printed paragraph numbers), `<<DEDICACE>>` and `<<PREFACE>>`. Numbers in parentheses in the text, such as "(215)", are Vattel's cross-references to his paragraphs. `notes`: the footnotes, mostly lettered references.

## Checks and limits

- `tools/transcription/qc_def41.py`: every page of the scan map has a file; the paragraph numbers run 1–409 without a gap except at the missing leaf; the part, chapter and section markers are all present and in order; the printed page numbers agree with the scan map; catchwords lead into the next page except at the fold-out and on four pages where the catchword is misread by a letter.
- Agreement with Google's OCR of the same scans (words of six letters or more): 63 pages fall below 80 per cent, mostly the dark pages of the Préface, where the OCR is also poor.
- Second reading by Claude Opus against the images (prompt `tools/transcription/CHECK_PROMPT_DEF41.md`), corrections written into the pages and listed under `checked`:
  - 24 pages drawn across the book (4,236 words): 4 words, 2 long s, 8 accents, 3 italic boundaries; 3.3 errors of letters or accents per 1,000 words.
  - the 36 pages with the lowest OCR agreement (7,255 words): 15 words, 6 long s, 15 accents, 15 italic boundaries; 5.0 per 1,000.
  - Spacing before `,` `;` `:` `?` is not reliable: the first readers often dropped the space the print has, and the second readers corrected it on the pages they read only.
- `tools/transcription/fix_def41.py`: on 225 pages a reader had written the catchword as the last body line as well; that line is dropped. Curly apostrophes are made straight.
- Modernized spellings are rare. Against the OCR, the transcription keeps the print's "prémier", "voïons", "moïen", "aïant"; four times it has "première" where the OCR reads "prémière".
- Pages 458–459 (one leaf) are wanting in the Lausanne copy; neither scan has them. Paragraphs 345 and 346 begin there.
- The errata (`editions/vattel-defense-1741/provenance/errata.json`) are not applied here; the edition applies them.
