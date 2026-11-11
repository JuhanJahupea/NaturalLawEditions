# Wolff, *Jus gentium methodo scientifica pertractatum* (Halle 1749)

Page transcription of the treatise, made from the scans for the reuse comparison with Vattel.

| File | Scans | Copy | Contents |
|---|---|---|---|
| `JG.json` | 849 pages (scans 28–876) | Google Books PDF (`Ius_Gentium_Methodo_Scientifica_Pertract.pdf`, 895 pages) | Prolegomena and cap. I–IX, §§ 1–1068 |
| `WJG_praef_prol.json` | 27 units (scans 17–45) | MDZ [bsb10008059](https://www.digitale-sammlungen.de/en/view/bsb10008059) | Praefatio (one unit) and Prolegomena §§ 1–26 |

Scan numbers in `JG.json` are the PDF pages of the Google Books copy. The Vattel edition's Wolff rows cite these pages (`JG.pdf34` is scan 34).

## Method

- `JG.json`: Claude Sonnet subagents, 24 pages each, read each page image (1300 px wide). Readers could crop the full-resolution page (about 2000 px) for zones they could not read. Prompt: `tools/transcription/TRANSCRIBE_PROMPT_WOLFF.md`.
- `WJG_praef_prol.json`: an earlier pass on the MDZ copy with the same rules. The Prolegomena were read by the session model, the Praefatio by Claude Sonnet. The pages were then cut into units: the Praefatio as one unit, the Prolegomena by §.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed; long s as `ſ`; `&`, `æ`, `œ` as printed; line breaks and line-end hyphens kept; italics as `<i>…</i>`; small capitals as capitals.
- Uncertain or lost text: `[?]` one character, `[...]` lost words, `[word?]` a guess (8 and 5 places).
- The book has no footnotes. Wolff's references, such as "(§. 23. part. 1. Jur. nat.)", stay in the main text.

## Page format (`JG.json`)

```json
{"scan": 28, "kind": "text", "page": "", "head": "JURIS GENTIUM\nPROLEGOMENA.",
 "margin": [{"para": "§. 1.", "text": "Definitio Ju-\nris Gentium."}],
 "body": "<<§ 1>>\nPer <i>Jus Gentium</i> intelligimus ...", "notes": [], "catch": "tem", "notes_scan": "reader's remarks"}
```

- `body`: the main text. A marker line `<<§ n>>` shows where § n starts.
- `margin`: Wolff's marginal summaries; `para` is the § they stand beside.
- `catch`: the catchword. `notes_scan`: the reader's remarks on the scan.

## Unit format (`WJG_praef_prol.json`)

`{"id": "WJG.Prol.3", "part": "Prol", "para": 3, "pages": ["WJG:s27", "WJG:2"], "margin": "...", "text": "...", "notes": []}`. In `pages`, `s27` is MDZ scan 27 and a bare number is a printed page.

## Checks

- Structure: the § markers run 1–1068. 1,089 markers mark 1,067 §§: a § whose heading falls at the foot of a page is marked on both pages. The book prints § 392 twice (scans 341 and 343) and has no § 393; the transcription keeps the numbers as printed.
- The Google Books OCR of the same PDF was compared page by page (8-letter sequences of the main text, accents folded, long s and f as one letter; `tools/transcription/qc_wolff.py`). Google Drive gives the OCR of the first 172 PDF pages only, so the check covers scans 28–171 (144 pages). The median page shares 96% of its sequences with the OCR. The lowest is scan 133 at 87%.
- No page has been read against the image by hand. The Google Books PDF is larger than the session could download.

## Known limits

- Italic and roman boundaries are approximate in places; readers flagged them in `notes_scan`.
- A reader can skip a word in a long line. The reuse passes match passages fuzzily, so a dropped word does not hide a match.
