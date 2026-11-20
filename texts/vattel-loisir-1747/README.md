# Vattel, *Le loisir philosophique, ou pièces diverses de philosophie, de morale et d'amusement* (Dresde 1747)

Page transcription of the *Essai sur le fondement du droit naturel, et sur le premier principe de l'obligation où se trouvent tous les hommes, d'en observer les loix*, the first piece of the collection. The edition `editions/vattel-essai-1747/` is built from it (`tools/transcription/essai_data.py`).

| File | Scans | Copy | Contents |
|---|---|---|---|
| `LOI47.json` | 68 pages (PDF pp. 19–86) | BCU Lausanne copy, Google Books [130TAAAAQAAJ](https://books.google.com/books?id=130TAAAAQAAJ), 332 PDF pages | Essai, printed pp. 3–70 |

The title page reads "DRESDE 1747. chez GEORGE CONRAD WALTHER, LIBRAIRE DU ROI." The Liberty Fund edition of *The Law of Nations* (2008) gives Geneva.

## Method

- Claude Sonnet subagents, 17 pages each, read each page image (1300 px wide). Prompt: `tools/transcription/TRANSCRIBE_PROMPT_LOISIR.md`.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed; long s as `ſ`; Vattel's quotation marks „ at the start of each quoted line kept; line breaks and line-end hyphens kept; italics as `<i>…</i>`.
- `body` has a marker line `<<§ n>>` where a numbered paragraph starts. `notes`: Vattel's footnotes, numbered remarks (1) and lettered references (a).

## Checks and limits

- The paragraph numbers run 1–41 as printed. The print has no 28 and no 32; the transcription keeps the numbers as printed.
- Catchwords: on 20 pages a reader wrote the catchword as the last body line as well. `essai_data.py` drops a last body line that repeats the catchword.
- Pages 24, 27, 28, 33 and 34 are heavily inked; some words were read from partial letters. Scan 62 has an ink blot over three italic Latin words; the Zürich copy gives them.
- Checked against a second copy (2026-11-20): the Zentralbibliothek Zürich copy (25.933) on e-rara ([IIIF manifest](https://www.e-rara.ch/i3f/v20/17961846/manifest)). Its title page reads "à Geneve … Et Se Vend à Dresde : chez George Conrad Walther, 1747"; the setting of the Essai is the same. Claude Sonnet readers compared every page, line by line, at 2x enlargement (prompt: `tools/transcription/PAGE_CHECK_PROMPT_LOISIR.md`). 10,569 words; 20 misreadings, all corrected: 11 letters (e.g. "obéïr" for "obéir", "vûe" for "vue", three letters under the ink blot on scan 62), 9 punctuation marks (e.g. a missing hyphen in "autre-|chose", "„„Pourquoi" for "„Pourquoi"). Rate: 1.9 per 1,000 words. `LOI47.json` lists the corrections under `checked`.
