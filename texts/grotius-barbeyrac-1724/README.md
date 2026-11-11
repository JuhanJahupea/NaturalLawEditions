# Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac (Amsterdam 1724)

Page transcription of both volumes, made from the scans for the reuse comparison with Vattel and Burlamaqui.

| File | Scans | archive.org item | Contents |
|---|---|---|---|
| `GRO24T1.json` | 573 | [le-droit-de-la-guerre-t-1-grotius](https://archive.org/details/le-droit-de-la-guerre-t-1-grotius) | Épître, Préface du traducteur, Discours préliminaire, Liv. I, Liv. II ch. I–XVI |
| `GRO24T2.json` | 526 | [le-droit-de-la-guerre-t-2](https://archive.org/details/le-droit-de-la-guerre-t-2) | Liv. II ch. XVII–XXVI, Liv. III, tables (not transcribed), errata (not transcribed) |

Scan numbers are the PDF pages of these items. They equal the page numbers of the copies in the Zotero library.

## Method

- Claude Sonnet subagents, 10 scans each, read each page image trimmed to the printed area (at most 1300 × 1560 px). Note columns and margins in small type were read from high-resolution crops.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed; long s as `ſ`; `&`, `æ`, `œ` as printed; line breaks kept; italics as `<i>…</i>`; small capitals as capitals.
- Uncertain or lost text: `[?]` one character, `[...]` lost words, `[word?]` a guess. Greek the readers could not read at the scan's resolution is `[Greek, n words]` (4,759 places, almost all in the notes).
- Indexes, tables of contents, errata and blank pages carry `kind` only.

## Page format

```json
{"scan": 214, "kind": "text", "page": "160", "head": "running head", "margin": [{"mark": "(a)", "text": "..."}],
 "body": "<<§ 5>>\n§. V. ...", "notes": [{"mark": "(22)", "sec": "§. III", "by": "", "text": "..."}],
 "catch": "de", "catch_notes": "", "sig": "TOM. I. X", "notes_scan": "reader's remarks"}
```

- `body`: the main text. Marker lines show where the structure starts: `<<LIVRE n>>`, `<<CHAP n>>`, `<<§ n>>`.
- `margin`: marginal summaries (mark "") and Grotius's lettered references.
- `notes`: footnotes in reading order. `sec` is the group label printed before them. `mark` `cont` is a note continued from the previous page. `by` is `author` for a note Grotius signed; Barbeyrac's own notes have `by` "".
- `kind`: text, preface, title, toc, index, errata, blank, plate, other.

## Checks

- Structure: the § and chapter markers run in sequence through both volumes.
- archive.org's OCR of the same scans was compared page by page (8-letter sequences of the main text, accents folded). The median page shares 80% of its sequences with the OCR (`tools/transcription/qc_shingle.py`). The pages that share less are pages where the OCR is garbled; where the OCR is legible the two agree.
- One scan (T1 214) was read against the image by hand: the main text agrees line for line.

## Known limits

- Greek is mostly not transcribed. Latin `æ`/`œ` in small italic, accents in note type and some digits in references are uncertain; readers flagged them in `notes_scan`.
- Readers worked page by page. A note split over two pages may carry `by: author` on one page only. The corpus build in `tools/transcription/corpus.py` sets it on both.
