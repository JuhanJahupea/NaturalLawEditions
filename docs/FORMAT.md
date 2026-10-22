# Collection format

Version `nle/1`. All files are UTF-8 JSON.

## Layout

```
catalogue.json                  the collection: editions, source texts, reuse tables
index.html                      landing page, built from catalogue.json
viewer/index.html               shared viewer: viewer/?ed=<edition id>#<unit id>
viewer/compose.js               builds display HTML from a text and its layers
editions/<edition id>/
  edition.json                  manifest: metadata, divisions, layers, viewer settings
  text.json                     the base text, one record per unit
  layers/<layer id>.json        standoff layers on the text
  provenance/                   inputs kept to check the text against
reuse/<from>__<to>.json         reuse table between two texts
tools/                          conversion and checks
```

## Identifiers

- **Edition id.** Author and date, lower case: `vattel-1773`.
- **Text id.** Author, short title, date: `wolff-jus-gentium-1749`. Every source text named by a reuse table has a `texts` entry in the catalogue. An edited text uses its edition id.
- **Unit id.** `<division>.<number>`. Unit ids are fixed. They are never renumbered. A correction that splits or merges units adds new ids and keeps the old ones as aliases in `edition.json`.
- **Global reference.** `<edition id>#<unit id>`, e.g. `vattel-1773#I.51`. The viewer address takes the same pair: `viewer/?ed=vattel-1773#I.51`.

## Offsets

Positions are 0-based, end-exclusive offsets into the `text` of a unit or of one of its notes. An offset counts UTF-16 code units. A part names the string: `t` is the unit's main text; `n0`, `n1` … are its notes in order.

## catalogue.json

```json
{
  "format": "nle-catalogue/1",
  "title": "...",
  "editions": [{"id", "path", "author", "title", "short", "imprint", "date", "lang", "status"}],
  "texts":    [{"id", "siglum", "author", "title", "imprint", "date", "lang", "layer"}],
  "reuse":    [{"path", "from", "to", "rows"}]
}
```

`texts.layer` says what text the comparison read (vision transcription, OCR and whose).

## editions/&lt;id&gt;/edition.json

Metadata of the base witness, the list of divisions, the layer files with their labels, and the settings the shared viewer reads: brand line, start unit, unit labels, citation patterns, link templates for scans, source families for the reuse filter.

## text.json

```json
{
  "format": "nle-text/1",
  "edition": "vattel-1773",
  "titles": {"I.I": "Des Nations, ou Etats souverains.", "...": "..."},
  "units": [
    {
      "id": "I.51", "div": "I", "chap": "IV", "n": 51,
      "kind": "section",
      "unnumbered": true,
      "margin": "marginal summary",
      "pages": [{"vol": "T1", "scan": 89, "printed": "65"}],
      "text": "plain text of the unit",
      "i":    [[a, b]],
      "para": [k],
      "pb":   [[at, "T1", 90, "66"]],
      "xr":   [[a, b, "I.50"]],
      "notes": [{"mark": "(*)", "text": "...", "i": [[a, b]], "xr": [[a, b, "II.12"]]}]
    }
  ]
}
```

- `kind`: `section` for a numbered unit, `page` for a unit that is a printed page (the Préface), `heading` for the book heading printed before § 1 (`<div>.0`).
- `n`: the number the unit carries in the edition. `unnumbered` marks a unit the print gives no number.
- `pages`: the printed pages the unit runs over, with scan numbers.
- `i`: italic ranges. `para`: paragraph starts inside the unit. `pb`: page breaks inside the unit (offset, volume, scan, printed page). `xr`: cross-references to other units.
- Text is the reading text: long s resolved, line-end hyphens joined, line breaks removed. Spelling, accents and printed misprints are kept.

## Layers

```json
{"format": "nle-layer/1", "edition": "vattel-1773", "layer": "<layer id>", "kind": "...", "items": [...]}
```

A layer item addresses the text by unit id and, where it marks a passage, by `at`: a list of `[part, start, end]`.

- `kind: "variants"` (`changes-1773`). One item per change between two printings: type, summary, the passages in each printing, the page of the older printing, `at` for the changed passage in the base text, `wholeNotes` for notes added entire, and `older` for readings of the older printing that the base text drops (`[part, offset, text]`, shown struck through).
- `kind: "comments"` (`wolff-divergences`). One item per comment attached under a unit: the source text and locus compared, the question, the relation, severity, the comment, the passages quoted from both texts, confidence, links.
- `kind: "translation"` (`english`). `units` maps a unit id to its translation: page, sentences, French sentence spans in the unit text (`fr`), the sentence alignment (`align`, groups of French and English sentence indices), and translation flags keyed by alignment group (`flags`).

## Reuse tables

`reuse/<from>__<to>.json` holds the reuse found between two texts. `from` is the later, reusing text. `to` is the source.

```json
{
  "format": "nle-reuse/1",
  "from": "vattel-1773", "to": "wolff-jus-gentium-1749",
  "rows": [
    {
      "id": 0, "unit": "Prelim.1", "at": [["t", 120, 214]],
      "family": "W", "work": "Wolff, Jus gentium (1749)", "locus": "§ 9", "page": "JG.pdf34", "inNote": false,
      "label": "close paraphrase", "confidence": 0.55, "status": "match", "step": "3b",
      "passage": "Vattel's words", "source": "the source's words", "french": "working French of a Latin source",
      "reason": "the judge's reason", "links": [["PDF p. 34", "url"]],
      "earliest": {"witness", "locus", "passage", "latin", "nearest", "reason"}
    }
  ]
}
```

- Row ids are unique for a `from` text across all its tables.
- `family` groups rows by author for the viewer filter. A table between two physical texts can hold more than one family (Grotius and Barbeyrac's notes in the same 1724 volume).
- `status`: `match` (confidence ≥ 0.5) or `possible` (0.3–0.5). `step` names the pipeline step in the method log.
- `earliest`: where an earlier text (Grotius 1625, Pufendorf 1672) already holds the passage.
