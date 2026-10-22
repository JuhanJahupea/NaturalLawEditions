# Changelog: vattel-1773

Versions are MAJOR.MINOR. MAJOR goes up when a unit id is retired or takes a new meaning. MINOR goes up for any other change to the text, its layers or its reuse tables. Unit ids are the stable part of a citation. A retired id gets an entry in `aliases` in `edition.json`, and the viewer resolves it.

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
