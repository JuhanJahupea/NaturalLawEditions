# Natural Law Editions

Text-compared editions of early modern natural law texts compiled by AI for scholarly use.

Each edition is a base text cut into units with fixed ids, plus layers on that text: variants between printings, comments, translations. Reuse between texts sits in tables of its own, so one source text can serve several editions.

## Layout

```
catalogue.json          editions, source texts and reuse tables in the collection
index.html              landing page
viewer/                 one viewer for every edition: viewer/?ed=<edition id>#<unit id>
editions/<id>/          one folder per edition: manifest, text, layers, provenance
reuse/                  reuse tables between texts
docs/FORMAT.md          the file formats
tools/                  conversion and checks
```

## Editions

| Id | Text | Units | Layers |
|---|---|---|---|
| `vattel-1773` | Vattel, *Le droit des gens*, Neuchâtel 1773 | 1,129: Préface by printed page (24), Préliminaires and Livres I–IV by § (1,100), book headings (5) | 1773 changes (67), Wolff divergences (169), English 1797 (1,124 units, 278 flags), reuse (3,427 rows in 16 tables) |
| `burlamaqui-1747` | Burlamaqui, *Principes du droit naturel*, Genève 1747 | 331: Avertissement, Partie I ch. I–XI and Partie II ch. I–XIV by § (303), part and chapter headings (27) | Élémens 1783 (323 rows, with the same/expands relation), PDP 1751 (84 rows, later text), reuse (1,611 rows in 20 tables, the two layers included) |

Each edition was converted from its working edition's `data.json` by `tools/convert_<edition>.py`, which use `tools/nle.py`. `tools/check_edition.js` loads the viewer in Chromium and compares every unit and reuse row it builds with the original `data.json`.

## Public address

GitHub Pages serves the repository root from branch `claude/vattel-edition-setup-7jkvhg`.

- Collection: https://juhanjahupea.github.io/NaturalLawEditions/
- Vattel viewer: https://juhanjahupea.github.io/NaturalLawEditions/viewer/?ed=vattel-1773
- A unit: https://juhanjahupea.github.io/NaturalLawEditions/viewer/?ed=vattel-1773#II.45

## Running the viewer locally

The viewer reads JSON files, so it needs an HTTP server:

```
python -m http.server
```

Then open `http://localhost:8000/viewer/?ed=vattel-1773`.
