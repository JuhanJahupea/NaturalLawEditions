# Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac (Amsterdam 1734)

Page transcription of both volumes, made from the scans for the reuse comparison with Vattel and Burlamaqui.

| File | Scans | archive.org item | Contents |
|---|---|---|---|
| `PUF34T1.json` | 876 | [ledroitdelanatur01pufe](https://archive.org/details/ledroitdelanatur01pufe) | Épître dédicatoire, Avertissement, Préface du traducteur, Liv. I–IV |
| `PUF34T2.json` | 722 | [ledroitdelanatur02pufe](https://archive.org/details/ledroitdelanatur02pufe) | Liv. V–VIII (scans 11–623), Table des auteurs and Table des matières (624–660, not transcribed), Barbeyrac's two Latin orations (661–722, not transcribed) |

Scan numbers are the PDF pages of these items. They equal the page numbers of the copies in the Zotero library. The items' leaf 0 is a colour card that the PDF leaves out, so archive.org's OCR runs one leaf ahead of the scans; `tools/transcription/ocr_index.py` finds that offset.

## Method

- Claude Sonnet subagents, 10 scans each, read each page image trimmed to the printed area (at most 1300 × 1560 px). Readers could crop note columns and margins at high resolution. Most read the notes from the full page.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed; long s as `ſ`; `&`, `æ`, `œ` as printed; line breaks kept; italics as `<i>…</i>`; small capitals as capitals.
- Uncertain or lost text: `[?]` one character, `[...]` lost words, `[word?]` a guess. Greek the readers could not read at the scan's resolution is `[Greek, n words]` (355 places, almost all in the notes).
- Indexes, tables of contents, the orations, plates and blank pages carry `kind` only.
- After reading, two missing § markers (T2 scans 198 and 238) were added by `tools/transcription/fix_markers.py`.

## Page format

As in `texts/grotius-barbeyrac-1724/README.md`. `by` is `author` for a note Pufendorf signed; Barbeyrac's own notes have `by` "".

## Checks

- Structure: the § and chapter markers run in sequence through both volumes. What remains is a § marked twice where a page ends on its heading (the corpus build counts it once) and a few running heads misprinted in the book (T2 scan 250 "Chap. I.").
- archive.org's OCR of the same scans was compared page by page (8-letter sequences of the main text, accents folded). The median page shares 84% of its sequences with the OCR (T1 85%, T2 80%; `tools/transcription/qc_shingle.py`). The lowest page (T2 54, 51%) is a page where the OCR is garbled; the transcription reads correctly.
- One scan (T1 334) was read against the image by hand. The main text agrees line for line except one dropped word ("ou quelque Gouvernement" read as "ou Gouvernement") and one accent ("demeurérent" for "demeurerent"). Margin and notes agree.

## Known limits

- Greek is mostly not transcribed. Latin in small italic, accents in note type and some digits in references are uncertain; readers flagged them in `notes_scan`.
- Readers worked page by page. Where a note runs from the left note column into the right, some readers joined it into one entry and others gave the second part as `cont`.
- A reader can skip a word in a long line, as in the hand check. The reuse passes match passages fuzzily, so a dropped word does not hide a match.
