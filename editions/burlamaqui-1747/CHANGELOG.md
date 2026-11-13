# Changelog: burlamaqui-1747

Versions are MAJOR.MINOR. MAJOR goes up when a unit id is retired or takes a new meaning. MINOR goes up for any other change to the text, its layers or its reuse tables. Unit ids are the stable part of a citation. A retired id gets an entry in `aliases` in `edition.json`, and the viewer resolves it.

## 1.8 (2026-11-13)

- Claude Opus read each of the 97 attributed rows again with the whole unit. It confirmed 90, rejected 4 and left 3 unsure; those lose `attributed`. The rejected rows name Pufendorf or Grotius for a passage taken from Barbeyrac's note, without naming Barbeyrac or the note. The 3 unsure rows were decided by hand and kept: P1.11.11 (2 rows; note (a) at the end of the paragraph cites the places "avec les notes de Monsr. Barbeyrac") and P2.4.20 (the paragraph opens "suivant la judicieuse remarque de Mr. BARBEYRAC"). Several cues now point at the words that name Barbeyrac. Each attribution carries the verdict and reason in `review`. Burlamaqui attributes 93 rows: 29 quotations, 64 references.
- Text, layers and the rows of the reuse tables are unchanged.

## 1.7 (2026-11-13)

- The English layer now flags translation problems: 133 flags on 106 units (shift 32, mistranslation 26, terminology 25, false friend 25, omission 13, addition 12; severity 1: 95, 2: 37, 3: 1). The panel shows them beside the aligned sentences, as in the Vattel edition. The one severity-3 flag: P1.1.1, where Nugent renders "la seule Raison" as "nature alone".
- Method: Claude Sonnet read every aligned pair of French and English sentences, 28 sections per batch, with a list of Burlamaqui's key terms (droit / loi, obligation, sentiment, amour de soi, imputation …). All quoted phrases were checked against the pair by script; one flag whose English was not in its pair was dropped. Machine judgements, not checked by hand.
- Viewer: the header has two menus instead of a row of checkboxes. **Authors** chooses the source families; it now filters the divergence notes as well as the reuse rows. **Layers** turns each layer on or off: Reuse (with Possible matches, Attributed and the edition's reuse layers under it), Divergences and the edition's other layers. Reuse can now be off while Divergences is on, so the text can show, for example, only the divergence notes against one author.
- Text, the other layers and the reuse tables are unchanged.

## 1.6 (2026-11-12)

- The Devoirs table (`reuse/burlamaqui-1747__pufendorf-devoirs-barbeyrac-1756.json`) comes from a new pass. Retrieval ran on a vision transcription of Barbeyrac's *Devoirs* (Amsterdam and Leipzig 1756, `texts/pufendorf-devoirs-barbeyrac-1756/`). 391 rows on 136 units (341 match, 50 possible) replace 350 rows on 140 units (248 match, 102 possible) from archive.org's OCR of the same edition. 222 rows quote Barbeyrac's notes (family Bb), 165 Pufendorf, 4 Leibniz's *Jugement*. The edition holds 1,655 reuse rows.
- Method: a language model (Claude Sonnet) judged the candidates in two rounds, then rechecked the earlier pass's matches that no new row covered. Claude Opus read the 9 units whose old match rows were still uncovered. The same model read 85 of the 86 rows at status possible: it kept 51 (30 now match, 21 stay possible), marked 23 commonplace and dropped 11.
- 245 of the 248 old match rows have a new row on the same passage. The 3 without: P2.11.7 (Barbeyrac's note 1 to Devoirs I.1.24), P2.11.15 (a citation of Barbeyrac's notes to I.1.27; the new rows mark the note's text), P2.14.16 (Pufendorf's preface § 6, "dans une pleine évidence"). They stay in `provenance/superseded/`.
- The divergences layer adds 1 note against the *Devoirs* (`passes/divergences-pufendorf-devoirs-barbeyrac-1756.json`): P2.4.9 against Devoirs I.3.13, on the principle of the duties to oneself (diverges, severity 2). The layer now holds 45 notes (Pufendorf DNG 38, Grotius 6, Devoirs 1).
- Method: for each Burlamaqui § with a Devoirs match, the Devoirs §§ it reuses and the nearest other § (233 pairs on 110 §§) went to a screening model (Claude Sonnet), with the notes the layer already holds against DNG for that §. The screen left out differences those notes record. It flagged 3 pairs at confidence 0.5 or more. Two were against Barbeyrac's *Réflexions* and were left out: the layer compares Burlamaqui with Pufendorf. Claude Opus kept the third.
- New layer `layers/english.json`: Thomas Nugent's translation, *The Principles of Natural Law* (2nd ed., London: J. Nourse 1763; Liberty Fund ed. by Petter Korkman, 2006), for 304 units. The editor's notes are left out; Burlamaqui's own notes are kept. The English is aligned with the French by sentence, chapter by chapter, by machine (Gale–Church lengths, with Nugent's § numbers as anchors where he prints them). 1,963 of 2,153 groups are one sentence to one; 10 French sentences have no English and 2 English sentences no French. The "English" button of a section, or a selection in the text, opens the aligned English.
- 97 reuse rows on 37 units now carry `attributed`: Burlamaqui names the source for the passage. 29 give the source's words as a quotation; 68 name it for the content. By source: Pufendorf DNG 37, Devoirs 26, Grotius 23, Cicero 8, Seneca 1, Pouilly 1, Spectateur 1. The items are in `passes/attributions.json`. Method as in the Vattel edition's changelog, 1.9 (245 candidate rows).
- Viewer: a new "Attributed" checkbox. Attributed rows (these, and the 105 rows labelled citation) have a dotted underline. Unticking the box hides them and leaves the reuse Burlamaqui does not attribute.
- Text and the other reuse tables are unchanged.

## 1.5 (2026-11-11)

- The divergences layer adds 6 notes against Grotius (`passes/divergences-grotius-barbeyrac-1724.json`), on 6 units: 5 where Burlamaqui's answer diverges from Grotius's, 1 where it differs in part. Severity 3: 4, 2: 2. The layer now holds 44 notes (Pufendorf 38, Grotius 6).
- Method: for each Burlamaqui § with a Grotius match, the Grotius §§ it reuses and the nearest other § (61 pairs on 29 §§) went to a screening model (Claude Sonnet). It flagged 7 pairs at confidence 0.5 or more. A second model (Claude Opus) read each with the whole Grotius § and Barbeyrac's notes and kept 6. Each note cites Grotius as "Grotius, DGP I.1.14" and links to the page of the 1724 edition. The notes take the Grotius colour.
- P1.10.5 and P1.10.6 now carry a note against Grotius (DGP I.1.9) beside the one against Pufendorf (DNG I.6.15). Both authors deny that permission is an effect of law.

## 1.4 (2026-11-11)

- New divergences layer (`layers/divergences.json`, from `passes/divergences-pufendorf-barbeyrac-1734.json`): 38 notes on 33 units where Burlamaqui answers a question of Pufendorf's differently. 30 diverge, 8 differ in part. Severity 3: 15, 2: 19, 1: 4. Each note cites Pufendorf as "Pufendorf, DNG I.6.15" and links to the page of the 1734 edition. The notes take the Pufendorf colour. The "Divergences" checkbox hides the layer.
- Method: for each Burlamaqui § with a Pufendorf match, the Pufendorf §§ it reuses and the nearest other § (350 pairs on 145 §§) went to a screening model (Claude Sonnet). It flagged 42 pairs and named one more outside its candidates (P1.9.9 against DNG I.6.12). A second model (Claude Opus) read the 43 pairs with the whole Pufendorf § and Barbeyrac's notes and kept 38. The comments say where Burlamaqui follows Barbeyrac's note against Pufendorf.
- The Pufendorf table now holds 587 rows on 182 units (531 match, 56 possible). It held 580 (447 match, 133 possible). The edition holds 1,614 reuse rows.
- Claude Opus read the old match rows that no new row covered (25 rows on 22 units; two units are chapter headings and were not read). 27 rows were added. 348 of the 359 old match rows then had a new row on the same passage; after the review below, 342.
- The same model read 129 of the 133 rows at status possible, each with the Burlamaqui part and the Pufendorf part that hold its passages. It kept 74 (59 now match, 15 stay possible), marked 35 commonplace and dropped 20. By the model's reasons, several drops are passages Burlamaqui took from Pufendorf's *Devoirs* and Barbeyrac's notes to it, which the Devoirs table already holds. Each reviewed row carries the verdict in `review`.
- The 17 old match rows with no new row on the same passage: P1.2.9 (DNG I.4.2), P1.3.2 (DNG I.5.3), P1.6.6 (DNG I.2.4), P1.6.9 (DNG I.6.5), P1.9.6 (DNG I.6.12), P2.4.12 (DNG II.3.15, Barbeyrac's Latin of Seneca), P2.6.8 (DNG II.3.23, citation), P2.7.0 (DNG I.2.6, chapter heading), P2.7.15 (DNG II.3.19), P2.9.8 (Barbeyrac's preface § 3), P2.9.9 (DNG I.3.5), P2.10.0 (DNG I.9, chapter heading), P2.10.9 (DNG I.9.3), P2.11.10 (DNG I.5.14, two rows), P2.11.13 (DNG I.5.14), P2.11.14 (DNG III.1.4). They stay in `provenance/superseded/`.
- Text and the other reuse tables are unchanged.

## 1.3 (2026-11-11)

- The Pufendorf table adds the rows for P1.2.12 against DNG I.4.9 on p. 226 of vol. 1, a page a judge named outside the candidates (580 rows, 447 match). The edition holds 1,607 reuse rows.

## 1.2 (2026-11-11)

- The Pufendorf table (`reuse/burlamaqui-1747__pufendorf-barbeyrac-1734.json`) comes from a new pass. Retrieval ran on a vision transcription of Barbeyrac's Pufendorf (Amsterdam 1734, `texts/pufendorf-barbeyrac-1734/`); a language model judged the candidates in two rounds, then rechecked the earlier pass's matches that no new row covered. 579 rows on 183 units (446 match, 133 possible) replace 639 rows on 235 units from the PDF text layer of the same edition. 334 of the 359 old match rows have a new row on the same passage.
- The judges also saw, for each section, the runs of five or more words it shares with a Pufendorf page (`tools/transcription/shared_scan.py`).
- 220 rows quote Barbeyrac's notes (family Bb). Source passages are quoted from the transcription, under the label "source (transcription)".
- The 639 old rows are kept in `provenance/superseded/burlamaqui-1747__pufendorf-barbeyrac-1734.json`. The viewer shows them with `?asbuilt=1`.
- Text, layers and the other reuse tables are unchanged. The edition holds 1,606 reuse rows.

## 1.1 (2026-10-23)

- The Grotius table (`reuse/burlamaqui-1747__grotius-barbeyrac-1724.json`) comes from a new pass. Retrieval ran on a vision transcription of Barbeyrac's Grotius (Amsterdam 1724, `texts/grotius-barbeyrac-1724/`); a language model judged the candidates in two rounds. 142 rows on 59 units (95 match, 47 possible) replace 87 rows on 50 units from the OCR of the same edition. 46 of the 50 old match rows have a new row on the same passage.
- 77 rows quote Barbeyrac's notes (family Bb). Source passages are quoted from the transcription, under the label "source (transcription)".
- The 87 old rows are kept in `provenance/superseded/burlamaqui-1747__grotius-barbeyrac-1724.json`. The viewer shows them with `?asbuilt=1`.
- Text, layers and the other reuse tables are unchanged. The edition holds 1,666 reuse rows.

## 1.0 (2026-10-22)

- First version in the collection, converted from `burlamaqui-reuse/edition/data.json` (working edition of 2026-10-07). 331 units with the working edition's ids (`P2.6.9`).
- 1,611 reuse rows in 20 tables. Two are layers: Élémens 1783 (323 rows, with the same/expands relation from step 10) and PDP 1751 (84 rows, the later text). The 1757 Latin translation is left out.
- 62 rows of the Vattel edition link to 29 units of this edition ("reused in Vattel").

## Before the collection (working edition, from the method log)

- 2026-10-06: transcription of the 1747 print (354 scans); gold set of citations; Barbeyrac's Pufendorf, the *Devoirs* and Barbeyrac's Grotius compared.
- 2026-10-07: Locke, Malebranche, Pouilly, Cumberland and others; earliest witness in the Latin; PDP 1751; ancient authors; the *Élémens* of 1783; the 1757 Latin identified as a translation of the 1747 text. Working edition built from steps 3, 4, 6, 8, 9 and 10.
