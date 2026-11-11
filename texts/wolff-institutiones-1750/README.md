# Wolff, *Institutiones juris naturae et gentium* (Halle 1750)

Page transcription of the textbook, made from the scans for the reuse comparison with Vattel.

| File | Scans | Copy | Contents |
|---|---|---|---|
| `INST.json` | 782 pages (scans 30–811) | Google Books PDF (`Institutiones_juris_naturae_et_gentium_i.pdf`, 844 pages) | Pars I–IV, §§ 1–1246 |

Scan numbers are the PDF pages of the Google Books copy. The Vattel edition's Wolff rows cite these pages (`INST.pdf53` is scan 53).

## Method

- Claude Sonnet subagents, 24 pages each, read each page image (1300 px wide). Readers could crop the full-resolution page (about 2000 px) for zones they could not read. Prompt: `tools/transcription/TRANSCRIBE_PROMPT_WOLFF.md`.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed; long s as `ſ`; `&`, `æ`, `œ` as printed; line breaks and line-end hyphens kept; italics as `<i>…</i>`; small capitals as capitals.
- Uncertain or lost text: `[?]` one character, `[...]` lost words, `[word?]` a guess (57 and 11 places).
- The book has no footnotes. Wolff's references, such as "(§. 400.)", stay in the main text.
- After reading, two § markers were added at the top of scans 340 (§ 567) and 621 (§ 961). The readers had taken the § heading at the foot of the page before for a catchword.

## Page format

As in `texts/wolff-jus-gentium-1749/README.md`.

## Checks

- Structure: the § markers run 1–1246. A § whose heading falls at the foot of a page is marked on both pages. Three § numbers are misprinted in the book and kept as printed: 555 for 255 (scan 167), 1024 for 1124 (scan 729), 1048 for 1148 (scan 744).
- The Google Books OCR of the same PDF was compared page by page (8-letter sequences of the main text, accents folded, long s and f as one letter; `tools/transcription/qc_wolff.py`). Google Drive gives the OCR of the first 195 PDF pages only, so the check covers scans 30–194 (165 pages). The median page shares 90% of its sequences with the OCR. The lowest are scans 30 and 190 at 72%.
- No page has been read against the image by hand. The Google Books PDF is larger than the session could download.

## Known limits

- Italic and roman boundaries are approximate in places; readers flagged them in `notes_scan`.
- A reader can skip a word in a long line. The reuse passes match passages fuzzily, so a dropped word does not hide a match.
