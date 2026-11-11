# Changelog: burlamaqui-1747

Versions are MAJOR.MINOR. MAJOR goes up when a unit id is retired or takes a new meaning. MINOR goes up for any other change to the text, its layers or its reuse tables. Unit ids are the stable part of a citation. A retired id gets an entry in `aliases` in `edition.json`, and the viewer resolves it.

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
