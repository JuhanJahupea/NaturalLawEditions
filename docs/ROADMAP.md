# Roadmap

Planned work, in order of priority. Each item names what it would add and how to measure it.

## Vattel 1773

1. A full Wolff *Jus gentium* pass. Vattel follows *Jus gentium* in Wolff's order. Read each Vattel section side by side with the § of Wolff it follows, and add the reuse the tables miss. The recall check of 2026-11-18 (`audit/README.md`) found that the tables hold about half of the defensible reuse of *Jus gentium* and about a quarter of that of the *Institutiones*.
2. A Pufendorf pass on Barbeyrac's notes and Pufendorf's examples. Recall is lowest there: about a fifth of the defensible reuse of Pufendorf is in the tables. The misses are mostly Pufendorf's examples and Barbeyrac's notes used beside Grotius.
3. A precision check of the 341 rows added on 2026-11-18 (`editions/vattel-1773/passes/additions.json`). Each was judged by one reader. A random sample read by a second reader would measure them, as `audit/precision-2026-11-18.json` did for the older rows.
4. Sources of the 1773 additions. Most additions take their examples from works the corpus lacks: Grotius, *Annales et historiae de rebus Belgicis* (10 additions), the *Lettres et négociations* of Jean de Witt (8), *Histoire de Timur-Bec* (5), Mariana, *De rege* (4). Transcribing the passages cited would let a pass test them (`audit/additions-1773-2026-11-20.json`).
5. Words hyphenated over a page break keep their hyphen in `text.json` ("quel-que"): 180 in Vattel 1773, 67 in Burlamaqui. Join them where the joined word occurs elsewhere in the edition, as `tools/transcription/essai_data.py` does for the Essai.

## Essai 1747

1. Rows the second readers named and the tables lack: Burlamaqui II.7.11 for § 40; Wolff PPU § 224 for the definition of duty in § 17; PPU § 136 for the Cicero quotation in § 8.
2. A second reading of the 74 rows from the *Theologia naturalis* and the *Discursus praeliminaris*. One reader wrote each.

## Translations of foreign-language passages (all editions)

1. Recall. Candidates came from a character model; a passage of one or two words, or one the model missed, has no gloss. A reader of a sample of units without candidates would measure what is missing.
2. Section numbers in `source` that the edition does not print (some Cicero loci) come from the readers' knowledge. Check them against the texts.
