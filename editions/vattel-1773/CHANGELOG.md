# Changelog: vattel-1773

Versions are MAJOR.MINOR. MAJOR goes up when a unit id is retired or takes a new meaning. MINOR goes up for any other change to the text, its layers or its reuse tables. Unit ids are the stable part of a citation. A retired id gets an entry in `aliases` in `edition.json`, and the viewer resolves it.

## 1.11 (2026-11-13)

- Claude Opus read each of the 89 attributed rows again with the whole unit. It confirmed 86 and rejected 3; those lose `attributed`. In two of the three (IV.93, IV.124) the footnote naming Wicquefort belongs to the neighbouring §, which shares the page. In III.155 (Bessus) the sentence calls a note on Quintus Curtius; the Grotius note has no call in the text. It gave a better cue for some rows and changed 2 from quotation to reference. Each attribution now carries the verdict and reason in `review`. Vattel attributes 86 rows: 13 quotations, 73 references.
- Text, layers and the rows of the reuse tables are unchanged.

## 1.10 (2026-11-13)

- New title pages (`titlepage.json`, images in `images/`): a diplomatic transcription of the title page of each volume, line by line, beside its scan (MDZ bsb10725331 and bsb10725332, scan 1). The viewer shows them before the Préface (t. I) and before Livre III (t. II), with a link in the contents. The two volumes differ in five places; `titlepage.json` lists them.
- Viewer: the header has two menus instead of a row of checkboxes. **Authors** chooses the source families; it now filters the divergence notes as well as the reuse rows. **Layers** turns each layer on or off: Reuse (with Possible matches, Attributed and the edition's reuse layers under it), Divergences and the edition's other layers. Reuse can now be off while Divergences is on, so the text can show, for example, only the divergence notes against one author.
- Text, layers and reuse tables are unchanged.

## 1.9 (2026-11-12)

- 89 reuse rows on 58 units now carry `attributed`: Vattel names the source for the passage. 15 give the source's words as a quotation; 74 name it for the content. By source: Grotius 46, Wolff 23 (*Jus gentium* 17, *Institutiones* 5, *Jus naturae* 1), Pufendorf 9, Wicquefort 8, Montesquieu 2, Bynkershoek 1. The items are in `passes/attributions.json`.
- Method: the candidates were the rows (not citation, not commonplace) whose unit names the source's author or work anywhere in its text, notes or margin (306 rows). A language model (Claude Sonnet) read each with the whole unit and decided whether the name belongs to this passage: in its sentence, in the sentence that introduces it, in a note called there, or in the margin beside it. The words that name the source (`cue`) were found in the unit by script. Not checked by hand.
- Viewer: a new "Attributed" checkbox. Attributed rows (these, and the 135 rows labelled citation) have a dotted underline. Unticking the box hides them and leaves the reuse Vattel does not attribute. The panel shows the words that name the source.
- Text, layers and the rows of the reuse tables are unchanged.

## 1.8 (2026-11-11)

- The Pufendorf table now holds 581 rows on 354 units (364 match, 217 possible). It held 612 (322 match, 290 possible). The edition holds 4,396 reuse rows.
- A second model (Claude Opus) read the 9 old match rows that no new row covered, with their pages. 5 rows were added. 132 of the 137 old match rows then had a new row on the same passage; after the review below, 130.
- The same model read 289 of the 290 rows at status possible, each with the Vattel part and the Pufendorf part that hold its passages. It kept 80 (40 now match, 40 stay possible), marked 173 commonplace and dropped 36. By the model's reasons, many of the commonplaces are passages where Vattel's wording follows Wolff's *Jus gentium* or Grotius and Pufendorf only states the same doctrine. Each reviewed row carries the verdict in `review` (`docs/FORMAT.md`). The viewer hides commonplaces unless "Possible matches" is on.
- The 7 old match rows with no new row on the same passage: I.244 (DNG VIII.5.7), II.32 (DNG IV.5, end), II.42 and II.43 (DNG VII.3.9), II.337 (DNG VIII.6.4), III.20 (DNG I.1.13), IV.19 (DNG VIII.7.4). They stay in `provenance/superseded/`. For I.244, II.32, II.337 and IV.19 the new rows sit on the same page but mark other sentences. For III.20 the recheck found only a stock formula (confidence 0.25) and kept no row.
- Text, layers and the other reuse tables are unchanged.

## 1.7 (2026-11-11)

- The divergences layer adds 44 notes against Pufendorf (`passes/divergences-pufendorf-barbeyrac-1734.json`), on 43 units: 27 where Vattel's answer diverges from Pufendorf's, 17 where it differs in part. Severity 3: 12, 2: 24, 1: 8. The layer now holds 302 notes (Wolff 169, Grotius 89, Pufendorf 44).
- Method: for each Vattel § with a Pufendorf match, the Pufendorf §§ it reuses and the nearest other § (394 pairs) went to a screening model. It flagged 46 pairs. A second model read each flagged pair with the whole Pufendorf § and Barbeyrac's notes and kept 44. Each note cites Pufendorf as "Pufendorf, DNG II.3.23" and links to the page of the 1734 edition. The notes take the Pufendorf colour.
- The Pufendorf table adds one row (612 rows, 322 match): Vattel II.170 against DNG VIII.9.5, a page a judge named outside the candidates. The edition holds 4,427 reuse rows.

## 1.6 (2026-11-11)

- The Pufendorf table (`reuse/vattel-1773__pufendorf-barbeyrac-1734.json`) comes from a new pass. Retrieval ran on a vision transcription of Barbeyrac's Pufendorf (Amsterdam 1734, `texts/pufendorf-barbeyrac-1734/`); a language model judged the candidates in two rounds, then rechecked the earlier pass's matches that no new row covered. 611 rows on 373 units (321 match, 290 possible) replace 284 rows on 221 units from the PDF text layer of the same edition. 128 of the 137 old match rows have a new row on the same passage.
- The judges also saw, for each section, the runs of five or more words it shares with a Pufendorf page (`tools/transcription/shared_scan.py`).
- 120 rows quote Barbeyrac's notes (family Bb). Source passages are quoted from the transcription, under the label "source (transcription)".
- The 284 old rows are kept in `provenance/superseded/vattel-1773__pufendorf-barbeyrac-1734.json`. The viewer shows them with `?asbuilt=1`.
- Text, layers and the other reuse tables are unchanged. The edition holds 4,426 reuse rows.

## 1.5 (2026-11-11)

- Three more Grotius divergence notes: III.66 against DGP III.3.12 (diverges), III.142 against DGP III.11.16 and III.180 against DGP III.1.21 (in part). These were the pairs the screeners named outside their candidates; the second model verified them. A fourth (III.31) fell below the confidence threshold. The layer holds 258 notes (Grotius 89).

## 1.4 (2026-10-23)

- The divergences layer adds 86 notes against Grotius (`passes/divergences-grotius-barbeyrac-1724.json`), on 80 units: 45 where Vattel's answer diverges from Grotius's, 41 where it differs in part. Severity 3: 21, 2: 55, 1: 10. The layer now holds 255 notes.
- Method: for each Vattel § with a Grotius match, the Grotius §§ it reuses and the nearest other § (663 pairs) went to a screening model. It flagged 108 pairs. A second model read each flagged pair with the whole Grotius § and Barbeyrac's notes and kept 86. Four pairs the screeners named outside their candidates were verified in 1.5.
- Each note cites Grotius as "Grotius, DGP II.16.25" and links to the page of the 1724 edition. The notes take the Grotius colour.

## 1.3 (2026-10-23)

- The Grotius table (`reuse/vattel-1773__grotius-barbeyrac-1724.json`) comes from a new pass. Retrieval ran on a vision transcription of Barbeyrac's Grotius (Amsterdam 1724, `texts/grotius-barbeyrac-1724/`); a language model judged the candidates in two rounds. 1,136 rows on 504 units (658 match, 478 possible) replace 464 rows on 329 units from the OCR of the same edition. 274 of the 282 old match rows have a new row on the same passage.
- 190 rows quote Barbeyrac's notes (family Bb). Source passages are quoted from the transcription, under the label "source (transcription)".
- The 464 old rows are kept in `provenance/superseded/vattel-1773__grotius-barbeyrac-1724.json`. The viewer shows them with `?asbuilt=1`.
- Text, layers and the other reuse tables are unchanged. The edition holds 4,099 reuse rows.

## 1.2 (2026-10-22)

- 30 of the 382 rows comparing Vattel with Burlamaqui's *Principes du droit politique* (1751) now name the unit of Burlamaqui's 1747 text that the PDP passage repeats (`repeats`). 28 through Burlamaqui's own PDP table (same page, overlapping passage), 2 because the wording stands in the 1747 unit. The Burlamaqui edition lists them as "reused in Vattel … through Burlamaqui 1751".
- The Wolff divergence layer is labelled "Divergences"; each note names its source.

## 1.1 (2026-10-22)

- The 62 rows comparing Vattel with Burlamaqui's *Principes du droit naturel* (1747) now point to the `burlamaqui-1747` edition (`reuse/vattel-1773__burlamaqui-1747.json`). Each row names the Burlamaqui unit that holds the source passage (`toUnit`).
- Aliases: `Preface` → `Pref.1`; the retired Préface paragraph ids `Pref.25`–`Pref.30` → the page that holds that paragraph (table below).
- Text, layers and the other reuse tables are unchanged.

## 1.0 (2026-10-22)

- First version in the collection, converted from the working edition's `edition_data/` (2026-10-22). 1,129 units. Layers: 1773 changes (67), Wolff divergences (169), English 1797 (1,124 units, 278 flags). 3,427 reuse rows in 16 tables.

## Before the collection (working edition, from the method log)

- 2026-10-12: English layer (the 1797 translation, Liberty Fund 2008) and the 67 changes of 1773 placed in the text.
- 2026-10-13: the three paragraphs printed without a § number become units `I.51`, `I.189`, `II.138`. New ids; no existing id changed.
- 2026-10-15: paragraph breaks inside §§ from the scans; Wolff rows from step 3b; the Wolff divergence layer.
- 2026-10-21: paragraph breaks restricted to the 381 verified on the scans. The Préface added as 30 paragraph units, `Pref.1`–`Pref.30`.
- 2026-10-22: the Préface units become the 24 printed pages, `Pref.1`–`Pref.24`. `Pref.1`–`Pref.24` changed meaning (paragraph n became page n); `Pref.25`–`Pref.30` were retired. Breaks after an italic word had been placed late; fixed.

## Préface: paragraph ids of 2026-10-21 and the pages that hold them

A link made on 21–22 October 2026 to `#Pref.n` with n ≤ 24 now opens printed page n, not paragraph n. Use this table to find the paragraph.

| Old id | Page unit | Old id | Page unit | Old id | Page unit |
|---|---|---|---|---|---|
| Pref.1 | Pref.1 | Pref.11 | Pref.9 | Pref.21 | Pref.18 |
| Pref.2 | Pref.1 | Pref.12 | Pref.10 | Pref.22 | Pref.19 |
| Pref.3 | Pref.2 | Pref.13 | Pref.11 | Pref.23 | Pref.19 |
| Pref.4 | Pref.4 | Pref.14 | Pref.12 | Pref.24 | Pref.20 |
| Pref.5 | Pref.4 | Pref.15 | Pref.13 | Pref.25 | Pref.21 |
| Pref.6 | Pref.5 | Pref.16 | Pref.14 | Pref.26 | Pref.22 |
| Pref.7 | Pref.6 | Pref.17 | Pref.14 | Pref.27 | Pref.23 |
| Pref.8 | Pref.7 | Pref.18 | Pref.14 | Pref.28 | Pref.23 |
| Pref.9 | Pref.7 | Pref.19 | Pref.17 | Pref.29 | Pref.24 |
| Pref.10 | Pref.8 | Pref.20 | Pref.18 | Pref.30 | Pref.24 |
