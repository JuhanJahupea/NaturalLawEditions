# Natural Law Editions

Text-compared editions of early modern natural law texts compiled by AI for scholarly use.

Each edition is a base text cut into units with fixed ids, plus layers on that text: variants between printings, comments, translations. Reuse between texts sits in tables of its own, so one source text can serve several editions.

## Layout

```
catalogue.json          editions, source texts and reuse tables in the collection
index.html              landing page
viewer/                 one viewer for every edition: viewer/?ed=<edition id>#<unit id>; the list of reuse rows: viewer/?ed=<edition id>&view=list[&ch=<chapter>]
editions/<id>/          one folder per edition: manifest, text, layers, changelog, provenance
reuse/                  reuse tables between texts
texts/<id>/             transcriptions of source texts made for the collection
audit/                  audits of the editions' data, with every verdict
docs/FORMAT.md          the file formats
tools/                  conversion and checks; tools/transcription/: the transcription and later-pass pipeline
```

## Editions

| Id | Text | Units | Layers |
|---|---|---|---|
| `vattel-1773` | Vattel, *Le droit des gens*, Neuchâtel 1773 | 1,129: Préface by printed page (24), Préliminaires and Livres I–IV by § (1,100), book headings (5) | 1773 changes (67), divergences (302: Wolff 169, Grotius 89, Pufendorf 44), English 1797 (1,124 units, 278 flags), title pages (2 volumes), translations of 120 Latin and Greek passages, reuse (8,059 rows in 16 tables; Grotius and Pufendorf from transcription passes; 3,260 rows from a full reading with the *Jus gentium* and Pufendorf; 403 rows added after the audits and for the 1773 additions; 92 rows attributed) |
| `burlamaqui-1747` | Burlamaqui, *Principes du droit naturel*, Genève 1747 | 331: Avertissement, Partie I ch. I–XI and Partie II ch. I–XIV by § (303), part and chapter headings (27) | Élémens 1783 (323 rows, with the same/expands relation), PDP 1751 (84 rows, later text), divergences (45: Pufendorf 38, Grotius 6, Devoirs 1), English 1763 (304 units, 133 flags), translations of 27 Latin passages, reuse (1,655 rows in 20 tables, the two layers included; Grotius, Pufendorf and the *Devoirs* from transcription passes; 99 rows attributed) |
| `vattel-essai-1747` | Vattel, *Essai sur le fondement du droit naturel*, in *Le loisir philosophique*, Dresde 1747, pp. 3–70 | 40: §§ 1–41 as printed (the print has no 28 and no 32), title (1) | divergences (43: Barbeyrac 18, Burlamaqui 8, Pufendorf 8, Wolff 5, Grotius 4), English 2008 (39 units, 158 flags), translations of 5 Latin passages, title page, reuse (407 rows in 7 tables: Wolff, *Philosophia practica universalis* I 88, Barbeyrac's *Devoirs* with Leibniz's *Jugement* and his *Réflexions* 83, Burlamaqui 1747 68, Barbeyrac's Pufendorf 54, Wolff, *Theologia naturalis* I 49, Barbeyrac's Grotius 40, Wolff, *Discursus praeliminaris* 25; all from transcription; 67 rows attributed) |

An attributed row is one where the author names the source for the passage (`passes/attributions.json`, judged by a language model), or one labelled citation. The "Attributed" option in the viewer's Layers menu hides them, to show only the reuse the author does not attribute.

In the contents list, each chapter and each listed unit has a bar for the share of its text under the rows shown. In the panel, a click on a source card's header folds it. In the list view, a click on a row shows the item in the panel.

Each edition was converted from its working edition's `data.json` by `tools/convert_<edition>.py`, which use `tools/nle.py`. `tools/link_editions.py` then links the rows whose source is itself an edition (Vattel → Burlamaqui 1747) to that edition's units. `tools/check_edition.js` loads the viewer in Chromium and compares every unit and reuse row it builds with the original `data.json`.

## Accuracy

A random sample of 400 reuse rows was read by Claude Opus (`audit/README.md`). Of the rows at status match, 84% (Vattel) and 94% (Burlamaqui) were right; most of the rest were weak (the source states a doctrine other writers state too); about 1% were wrong. Rows at status possible, shown with "Possible matches", were right in 35–40% of cases. Weak match rows are now possible. Vattel's tables for Pufendorf and Burlamaqui, where most weak rows were, were read again row by row: of 494 match rows, 148 are right, 338 weak (now possible) and 8 wrong (rejected). A label check read 210 rows whose word overlap sits far from their label's and changed 158 labels. A second sample of match rows no audit had read puts right match rows at 89% in both editions, with none wrong. A recall check of 24 random sections of Vattel found that the tables hold about a third of the reuse of Wolff, Grotius and Pufendorf a reader would defend; 341 rows were added from it and from the passages the audits named. Every match row of Vattel's *Essai* was read by a second reader: 170 of 198 are right, 28 weak (now possible), none wrong.

## Source texts

Transcriptions made for the collection. Each folder in `texts/` has a README on method, checks and limits.

| Id | Text | Pages |
|---|---|---|
| `grotius-barbeyrac-1724` | Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac, Amsterdam 1724 | 1,099 scans in 2 vols |
| `pufendorf-barbeyrac-1734` | Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac, Amsterdam 1734 | 1,598 scans in 2 vols |
| `pufendorf-devoirs-barbeyrac-1756` | Pufendorf, *Les devoirs de l'homme et du citoyen*, trad. Barbeyrac, Amsterdam and Leipzig 1756 | 958 scans in 2 vols |
| `wolff-jus-gentium-1749` | Wolff, *Jus gentium methodo scientifica pertractatum*, Halle 1749 | 849 pages; Praefatio and Prolegomena from a second copy (27 units) |
| `wolff-institutiones-1750` | Wolff, *Institutiones juris naturae et gentium*, Halle 1750 | 782 pages |
| `wolff-philosophia-practica-1738` | Wolff, *Philosophia practica universalis*, pars prior, Frankfurt and Leipzig 1738 (MDZ copy of the Halle 1744 issue) | 317 pages, §§ 1–415 |
| `wolff-theologia-naturalis-1739` | Wolff, *Theologia naturalis*, pars prior, Frankfurt and Leipzig 1739 | 54 pages, §§ 948–1006 |
| `wolff-discursus-praeliminaris-1740` | Wolff, *Discursus praeliminaris de philosophia in genere*, in the *Logica*, Frankfurt and Leipzig 1740 | 104 pages, §§ 1–171 |
| `vattel-loisir-1747` | Vattel, *Le loisir philosophique*, Dresde 1747: the *Essai sur le fondement du droit naturel* | 68 pages, checked against a second copy |

## Public address

GitHub Pages serves the repository root from branch `main`.

- Collection: https://juhanjahupea.github.io/NaturalLawEditions/
- Vattel viewer: https://juhanjahupea.github.io/NaturalLawEditions/viewer/?ed=vattel-1773
- A unit: https://juhanjahupea.github.io/NaturalLawEditions/viewer/?ed=vattel-1773#II.45

## Checks

```
tools/check_all.sh <vattel-reuse/edition_data/data.json> <burlamaqui-reuse/edition/data.json>
```

It serves the repository, then:

- `tools/check_edition.js` loads each edition in Chromium and compares every unit (HTML, notes, pages, cross-references, layers) and every reuse row the viewer builds with the working edition's `data.json`.
- `tools/check_links.js` checks every link: rows linked to another edition, the "reused in" lists, cross-references, aliases, catalogue paths, row spans. It opens every link target in the viewer and follows one link each way by clicking.

## Running the viewer locally

The viewer reads JSON files, so it needs an HTTP server:

```
python -m http.server
```

Then open `http://localhost:8000/viewer/?ed=vattel-1773`.
