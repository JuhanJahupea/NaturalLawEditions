# Roadmap

Planned work, in order of priority. Each item names what it would add and how to measure it.

## Vattel 1773

1. A full pass with Grotius (Barbeyrac's translation) and with the *Institutiones*, as done for the *Jus gentium* and Pufendorf on 2026-11-21 (`tools/transcription/full_cand.py`, `FULL_PASS_PROMPT.md`). The Grotius table comes from retrieval only; the *Institutiones* hold about a quarter of the reuse a reader finds.
2. The possible rows of the full pass (1,657). A second reader rated a third of a sample right and most of the rest weak. Read them all and promote the right ones, as was done for the Essai.
3. A recall check after the full pass: the same 24 random sections as on 2026-11-18, to measure what the tables now hold.
4. Sources of the 1773 additions. Most additions take their examples from works the corpus lacks: Grotius, *Annales et historiae de rebus Belgicis* (10 additions), the *Lettres et négociations* of Jean de Witt (8), *Histoire de Timur-Bec* (5), Mariana, *De rege* (4). Transcribing the passages cited would let a pass test them (`audit/additions-1773-2026-11-20.json`).
5. Words hyphenated over a page break keep their hyphen in `text.json` ("quel-que"): 180 in Vattel 1773, 67 in Burlamaqui. Join them where the joined word occurs elsewhere in the edition, as `tools/transcription/essai_data.py` does for the Essai.

## Essai 1747

1. Rows the second readers named and the tables lack: Burlamaqui II.7.11 for § 40; Wolff PPU § 224 for the definition of duty in § 17; PPU § 136 for the Cicero quotation in § 8.
2. A second reading of the 74 rows from the *Theologia naturalis* and the *Discursus praeliminaris*. One reader wrote each.

## Translations of foreign-language passages (all editions)

1. Recall. Candidates came from a character model; a passage of one or two words, or one the model missed, has no gloss. A reader of a sample of units without candidates would measure what is missing.
2. Section numbers in `source` that the edition does not print (some Cicero loci) come from the readers' knowledge. Check them against the texts.
