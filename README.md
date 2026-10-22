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
| `vattel-1773` | Vattel, *Le droit des gens*, Neuchâtel 1773 | Préface by page, Préliminaires and Livres I–IV by § | 1773 changes, Wolff divergences, English (1797), reuse |

## Running the viewer locally

The viewer reads JSON files, so it needs an HTTP server:

```
python -m http.server
```

Then open `http://localhost:8000/viewer/?ed=vattel-1773`.
