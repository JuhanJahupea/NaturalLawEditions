# Wolff, *Philosophia practica universalis, methodo scientifica pertractata*, pars prior (1738)

Page transcription of the first part of Wolff's universal practical philosophy, made for the reuse comparison with Vattel's *Essai sur le fondement du droit naturel* (1747). Vattel cites it as "Wolf. Phil. Pract. univ. p. 1." (§§ 118, 119, 132, 137).

| File | Scans | Copy | Contents |
|---|---|---|---|
| `PPU1.json` | 317 pages (MDZ canvases 25–341) | Bayerische Staatsbibliothek, MDZ [bsb10008634](https://www.digitale-sammlungen.de/en/view/bsb10008634): Halle, Renger, 1744 | Prolegomena and cap. I–IV, §§ 1–415 (printed pp. 1–317) |

The first edition is Frankfurt and Leipzig, Renger, 1738. The Halle issue of 1744 has the same collation ([12] Bl., 592 pp.). The page breaks of the MDZ copy match those of a Google Books copy of the 1738 edition (Google Drive copy, OCR of its first 157 PDF pages; see Checks), so the text is that of 1738. Canvas numbers are printed page + 24. Cap. V (De conscientia, from § 417) and cap. VI (De imputatione, from § 526) are not transcribed.

## Method

- Claude Sonnet subagents, about 24 pages each, read each MDZ page image at 1300 px wide. Readers could fetch a full-resolution crop of a zone from the MDZ IIIF server (`tools/transcription/mdz_crop.py`). Prompt: `tools/transcription/TRANSCRIBE_PROMPT_PPU.md`.
- Diplomatic rules as for the *Jus gentium* (`texts/wolff-jus-gentium-1749/README.md`): spelling, accents, capitals and punctuation as printed; long s as `ſ`; line breaks and line-end hyphens kept; italics as `<i>…</i>`; small capitals as capitals.
- Page format as `JG.json`: `body` with `<<§ n>>` marker lines, `margin` with Wolff's marginal summaries and the § they stand beside, `notes`, `catch`, `notes_scan`.

## Checks

- Structure: the § markers run 1–415, each once. Where a § heading falls at the foot of a page, the marker is on the page where the text begins. Misprints are kept as printed: page numbers "37" (p. 73) and "259" (p. 295); running heads "Cap. I. Pars II." and "De Obligatio".
- The Google Books OCR of a 1738 copy (Google Drive gives the OCR of its first 157 PDF pages) was compared page by page with the transcription (8-letter sequences of the main text, accents folded, long s and f as one letter, u/v and i/j as one letter). 128 pages could be compared. The median page shares 96% of its sequences with the 1738 OCR. The lowest, scan 152 (38%), is a page whose OCR the connector returned only in part.

## Known limits

- The left margin of many odd pages is in the gutter shadow. On them the readers read some line-initial letters from context; `notes_scan` names the pages.
- Some marginal summaries run over two pages and are split between them.
- Italic and roman boundaries are approximate in places.
