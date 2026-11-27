# Reuse rows of the Défense (step 4)

Where Vattel's *Défense du système leibnitien* (1741) takes something from its sources: one file per source text, format `nle-reuse-rows/1`. These are the rows of a reuse table (`nle-reuse/1`, `docs/FORMAT.md`) before the edition build places each passage on the text. Units are the ids of `tools/transcription/def41_data.py` (D.n = paragraph n, Pref.k / Ded.k = a page of the Préface or dedication).

| File | Source | Rows | Match / possible |
|---|---|---|---|
| `leibniz-theodicee-1734.json` | Leibniz, *Théodicée* | 297 | 273 / 24 |
| `crousaz-examen-1737.json` | Crousaz, *Examen* | 200 | 199 / 1 |
| `roques-lettres-1737-1739.json` | Roques, letters, as Vattel quotes them | 174 | 174 / 0 |
| `crousaz-commentaire-1738.json` | Crousaz, *Commentaire* | 87 | 87 / 0 |
| `wolff-psychologia-rationalis-1734.json` | Wolff, *Psychologia rationalis* §§ 480–642 | 40 | 40 / 0 |

798 rows in 236 of the 467 units. 509 are attributed: Vattel names or cites the source for the passage. `stance` gives what Vattel does with the passage. He adopts Leibniz (281 rows) and Wolff (40). He rejects Crousaz (260 of 287). 11 Leibniz rows reach him through Roques's letter (`via`).

## Method

1. Candidates (`tools/transcription/def41_cand.py`). For each unit:
   - the loci Vattel cites (gold set, `../citations.json`);
   - source segments that share a rare run of five words or more with the unit;
   - for the French sources, the two nearest segments per source by vocabulary (TF-IDF cosine ≥ 0.06).

   191 units had no candidate and were not judged. 276 units went in 28 batches of ten.
2. Judges (`tools/transcription/DEF41_JUDGE_PROMPT.md`, Claude Sonnet, one batch each).
   - They read every candidate.
   - They searched the other segments when Vattel quotes Leibniz or Wolff and no candidate held the words.
   - They wrote rows with exact passages on both sides.
   - Result: 644 rows.
3. Check (`tools/transcription/DEF41_CHECK_PROMPT.md`, Claude Opus, `def41_checkbatch.py`).
   - Rows checked: confidence under 0.75, or label shared argument, loose paraphrase or open disagreement. 225 in all.
   - Verdicts: 177 keep, 25 weak (set to possible), 23 drop.
   - Three dropped rows pointed to the wrong § of the *Théodicée* where the checker named the § that holds the words. They are moved there (`RETARGET` in `def41_merge.py`).
4. Roques: each passage of `texts/roques-lettres-1737-1739/ROQ.json` is a row. Verbatim passages are quotations; reported ones are citations.
5. `tools/transcription/def41_merge.py`.
   - Every passage is checked in its unit and every source passage in its segment. All 798 are found.
   - status: match (confidence ≥ 0.5), possible (0.3–0.5).

## Checks

- Gold set: Vattel gives a locus in these sources 400 times. 399 have a row on that locus (or the next page or §). The one without is D.274 ("Ex. pag. 61."), a pointer.

## Known limits

- Many passages Vattel quotes come from works not in the collection, and have no row. Among them:
  - Leibniz: the *Système nouveau* and its *Éclaircissements*, the *Réplique* and the *Réponse* to Bayle, the *Considérations sur les principes de vie*, the *Réponse au P. Lamy*, the fifth letter to Clarke, the *Animadversiones* on Stahl, *De ipsa natura*, the *Monadologia*;
  - Wolff: the *Cosmologia*, and *Psychologia rationalis* § 66 (Sectio I, not transcribed).

  Most of Partie I ch. IV, VI and VIII, where the units have no candidate, draws on them.
- The Crousaz texts are OCR: source passages keep the OCR's misreadings.
- The *Théodicée* text is Janet's modern spelling. Source passages differ from Vattel's 1734 copy in spelling, not in words.
- Judges and checkers worked from candidates. Reuse of a passage that shares no rare run and little vocabulary with the unit can be missed.
