# Leibniz, *Essais de théodicée* (Amsterdam, François Changuion, 1734)

Text by section, made for the reuse comparison with Vattel's *Défense du système leibnitien* (1741). Vattel cites the *Théodicée* by § ("Théod. §. 9."), and once the life of Leibniz printed in the 1734 edition ("la Vie de Mr. de Leibnitz §. 137"), which suggests he used this edition.

| File | Sections | Text | Scans linked |
|---|---|---|---|
| `THEO.json` (`nle-sections/1`) | 588: Préface ¶ 1–36 (`Pref.n`), Discours de la conformité §§ 1–87 (`Disc.n`), Essais §§ 1–417 (`T.n`), Abrégé préambule and objections I–VIII (`Abr.0–8`), Réflexions sur Hobbes §§ 1–12 (`Hob.n`), Remarques sur King §§ 1–27 (`King.n`) | [Wikisource](https://fr.wikisource.org/wiki/Essais_de_Th%C3%A9odic%C3%A9e), proofread text of *Œuvres philosophiques de Leibniz*, ed. Paul Janet, 2nd ed., Paris, Alcan, 1900, vol. II (CC BY-SA 4.0) | archive.org [essaisdethodice01leibgoog](https://archive.org/details/essaisdethodice01leibgoog) (vol. I) and [essaisdethodice00leibgoog](https://archive.org/details/essaisdethodice00leibgoog) (vol. II) |

## Method

- `tools/transcription/theodicee_text.py`: the Wikisource text, exported as EPUB by ws-export, split at its section numbers. Janet's notes, note calls, page numbers and index are left out. Italics kept as `<i>…</i>`.
- Numbering fixed against the sequence: Partie I § 1 and § 5 carry no number in the Wikisource text; Discours "63" after 64 is § 65; "445" after 414 is § 415.
- Each section is linked to the leaf of the 1734 edition where it begins: the leaf, at or after the previous section's, whose archive.org OCR holds most of the section's first fifteen long words (accents folded, long s and f as one letter). 539 sections are placed so. 49 are placed between their neighbours and marked `approx`.

## Known limits

- The text is Janet's, with modern spelling and punctuation. Its wording follows the early editions, but it is not a transcription of 1734. Spelling differences (oi/ai, ſ, accents) are folded in the reuse search.
- The life of Leibniz by "M. L. de Neufville" (Louis de Jaucourt) in vol. I of 1734, and the *Causa Dei* in vol. II, are not included.
- About 30 of the 539 matched links are one leaf off where a section begins at the foot of a page.
