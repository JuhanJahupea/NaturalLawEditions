# Pufendorf, *Les devoirs de l'homme et du citoyen*, trad. Barbeyrac (Amsterdam and Leipzig 1756)

Page transcription of both volumes, made from the scans for the reuse comparison with Burlamaqui.

| File | Scans | archive.org item | Contents |
|---|---|---|---|
| `DEV56T1.json` | 514 | [bub_gb_dDKCHraV9BoC](https://archive.org/details/bub_gb_dDKCHraV9BoC) | Avertissement sur cette nouvelle édition (scans 11–33), Avis postérieur (34–38), Préface du traducteur (39–54), Préface de l'auteur (55–78), Table (79–82, not transcribed), Liv. I (83–508) |
| `DEV56T2.json` | 444 | [bub_gb_unXpgRJJud0C](https://archive.org/details/bub_gb_unXpgRJJud0C) | Liv. II (11–204); Leibniz, *Jugement d'un anonyme sur l'original de cet abrégé*, with Barbeyrac's *Réflexions* (205–298); Barbeyrac, *Discours sur la permission des loix* (299–352) and *Discours sur le bénéfice des loix* (353–418); Table des matières (419–437, not transcribed) |

Scan numbers are the PDF pages of these items. Covers, endpapers, blanks and the frontispiece carry `kind` only.

## Method

- Claude Sonnet subagents, 20 scans each, read each page image trimmed to the printed area (at most 1300 × 1560 px). Readers could crop the notes and the side margins at high resolution. Prompt: `tools/transcription/TRANSCRIBE_PROMPT_DEVOIRS.md`.
- Diplomatic rules: spelling, accents, capitals and punctuation as printed; long s as `ſ`; `&`, `æ`, `œ` as printed; line breaks kept; italics as `<i>…</i>`; small capitals as capitals.
- Uncertain or lost text: `[?]` one character, `[...]` lost words, `[word?]` a guess (13 places in all).
- After reading, the `kind` of two pages (T2 scans 196–197) was set to `text`; the readers had put the catchword there.

## Page format

As in `texts/grotius-barbeyrac-1724/README.md`, with these differences:

- `margin`: marginal summaries (mark "") and the lettered glosses that give Pufendorf's Latin term, with their letter as mark (`{"mark": "(a)", "text": "<i>Invita.</i>"}`).
- `notes`: Barbeyrac's notes, one column at the foot. All have `by` "".
- `kind`: `text` (the *Devoirs*), `preface` (the avertissements and the two prefaces), `jugement` and `reflexions` (the *Jugement* with Barbeyrac's *Réflexions*), `discours` (the two discourses). In the *Jugement* the readers did not tell the two apart consistently: Leibniz's text and Barbeyrac's replies alternate on most pages. The scan ranges above are the reliable division.

## Checks

- Structure: the book, chapter and § markers run in sequence. A § whose heading falls at the foot of a page is marked on both pages. The *Jugement* and the discourses number their §§ afresh.
- One gap: the scan of vol. I lacks printed pp. 78–79 (scan 159 is p. 77, scan 160 is p. 80). Liv. I ch. II § 6 is on those pages and has no marker.
- archive.org's OCR was compared page by page (8-letter sequences of the main text, accents folded; `tools/transcription/qc_shingle.py`). Vol. I: the median page shares 83% of its sequences with the OCR of the same scan; the lowest pages (scan 497 at 35%) are pages where the OCR is garbled. Vol. II: archive.org gives the OCR as one text without page breaks, so each page was compared with the whole volume; the median page shares 93%.
- One scan (T1 120) was read against the image by hand. The main text agrees line for line; the differences are spaces around punctuation ("les-mêmes" for "les - mêmes"). Margin and catchword agree.

## Known limits

- Greek in the notes was read from the full page and is uncertain. Latin glosses in small italic in the margins are uncertain in places; readers flagged them in `notes_scan`.
- A reader can skip a word in a long line. The reuse passes match passages fuzzily, so a dropped word does not hide a match.
