# Collection format

Version `nle/1`. All files are UTF-8 JSON.

## Layout

```
catalogue.json                  the collection: editions, source texts, reuse tables
index.html                      landing page, built from catalogue.json
viewer/index.html, app.js       shared viewer: viewer/?ed=<edition id>#<unit id>; reuse list: viewer/?ed=<edition id>&view=list
viewer/compose.js               builds display HTML from a text and its marks
editions/<edition id>/
  edition.json                  manifest: metadata, version, divisions, layers, viewer settings
  CHANGELOG.md                  what changed in each version
  text.json                     the base text, one record per unit
  layers/<layer id>.json        standoff layers on the text
  provenance/                   inputs kept to check the text against
reuse/<from>__<to>.json         reuse table between two texts
tools/                          conversion and checks
```

## Identifiers

- **Edition id.** Author and date, lower case: `vattel-1773`.
- **Text id.** Author, short title, date: `wolff-jus-gentium-1749`. Every source text named by a reuse table has a `texts` entry in the catalogue. An edited text uses its edition id.
- **Unit id.** `<division>.<number>` (Vattel: `I.51`) or `<division>.<chapter>.<number>` where numbers restart in each chapter (Burlamaqui: `P2.6.9`). Unit ids are fixed. They are never renumbered. A correction that splits or merges units adds new ids and keeps the old ones as aliases in `edition.json`.
- **Global reference.** `<edition id>#<unit id>`, e.g. `vattel-1773#I.51`. The viewer address takes the same pair: `viewer/?ed=vattel-1773#I.51`.

## Versions

- Each manifest carries `version` and `changed`; each edition folder has a `CHANGELOG.md`. The viewer shows the version at the foot of the panel.
- MAJOR goes up when a unit id is retired or takes a new meaning. MINOR goes up for any other change to the text, its layers or its reuse tables.
- Unit ids are the stable part of a citation. A retired id gets an `aliases` entry pointing to the unit that now holds its text; the viewer and the go-to box resolve it. An id that was reused with a new meaning cannot be aliased; the changelog then lists the old and new ids (Vattel's Préface, 2026-10-22).

## Offsets

Positions are 0-based, end-exclusive offsets into the `text` of a unit or of one of its notes. An offset counts UTF-16 code units. A part names the string: `t` is the unit's main text; `n0`, `n1` … are its notes in order.

## catalogue.json

```json
{
  "format": "nle-catalogue/1",
  "title": "...",
  "editions": [{"id", "path", "author", "authorShort", "title", "short", "imprint", "date", "lang", "status"}],
  "texts":    [{"id", "sigla", "author", "title", "imprint", "date", "lang", "layer"}],
  "reuse":    [{"path", "from", "to", "rows", "toLayer", "repeats"}]
}
```

`texts.sigla` are the prefixes of the page ids that name the text in the rows (two projects may use two). `texts.layer` says what text the comparison read (vision transcription, OCR and whose). Where `to` is an edition, `reuse.toLayer` says it, since the comparison read the OCR, not the edition's transcription.

## editions/&lt;id&gt;/edition.json

- Metadata of the base witness and of the transcription.
- `version` (MAJOR.MINOR) and `changed` (date). See Versions below.
- `aliases`: retired unit ids mapped to their successors. The viewer resolves them.
- `divisions`: one entry per division, in order: `key` (the first part of the unit id), `label`, `chapters` (true when units are grouped by chapter), `chapterTitle` for a division without chapters, `unitLabel` (`{chap}`, `{n}` from the unit id), `unitMark`, `cite` (`{prefix}`, `{chap}`, `{n}`, `{unnum}`, `{page}`).
- `layers`: one entry per layer, with the `label` and `tooltip` of its checkbox and `default` (on unless false). A layer with a `file` is a layer file in `layers/`. A layer of `kind: "reuse"` is a view on one reuse table: `table` names it, `family` names the family its checkbox switches.
- `reuse`: `families` (key, label, `chip`, `color`, `dark`, `sourceLabel`) and the wording of the source panel (`baseTag`, `sourceLabel`, `noteLabel`, `partLabels`, `earliest`, `nearer`).
- `viewer`: brand line, start unit, search placeholder, `goto` patterns (a regular expression and an id template), citation prefix and page pattern, `volumes`, `pageLink` (template for a scan link), `pageBreak` (the HTML of a page-break marker).

## text.json

```json
{
  "format": "nle-text/1",
  "edition": "vattel-1773",
  "titles": {"I.I": "Des Nations, ou Etats souverains.", "...": "..."},   // keyed <division>.<chapter>
  "units": [
    {
      "id": "I.51", "div": "I", "chap": "IV", "n": 51,
      "kind": "section",
      "unnumbered": true,
      "margin": "marginal summary",
      "pages": [{"vol": "T1", "scan": 67, "printed": "65"}],
      "text": "plain text of the unit",
      "i":    [[a, b]],
      "para": [k],
      "pb":   [[at, "T1", 68, "66"]],
      "xr":   [[a, b, "I.50"]],
      "notes": [{"mark": "(*)", "text": "...", "i": [[a, b]], "xr": [[a, b, "II.12"]]}]
    }
  ]
}
```

- `kind`: `section` for a numbered unit, `page` for a unit that is a printed page (the Préface), `front` for unnumbered front matter (Burlamaqui's Avertissement), `heading` for a part, book or chapter heading (number 0). The viewer does not show headings.
- `n`: the number the unit carries in the edition. `unnumbered` marks a unit the print gives no number.
- `pages`: the printed pages the unit runs over, with scan numbers.
- `i`: italic ranges. `para`: paragraph starts inside the unit. `pb`: page breaks inside the unit (offset, volume or "", scan, printed page). `xr`: cross-references to other units.
- Text is the reading text: long s resolved, line-end hyphens joined, line breaks removed. Spelling, accents and printed misprints are kept.

## Layers

```json
{"format": "nle-layer/1", "edition": "vattel-1773", "layer": "<layer id>", "kind": "...", "description": "...", "items": [...]}
```

An item names its unit. Where it marks a passage, `at` is a list of `[part, start, end]`.

### `kind: "variants"` (`layers/changes-1773.json`)

One item per change between the base printing and another printing.

```json
{
  "id": "II.45~0", "unit": "II.45", "type": "deleted phrase", "content": "one-line summary", "placed": true,
  "passage": "the passage in the base text", "at": [["t", 120, 214]], "wholeNotes": [0],
  "otherPassage": "the passage in the other printing", "otherPages": "A1.p345 – A1.p346", "otherLink": "url",
  "otherReadings": [["t", 764, " comme les spectres s’évanouissent au lever du soleil "]]
}
```

- `at`: the changed passage in the base text. `wholeNotes`: notes added entire, by index.
- `otherReadings`: readings of the other printing that the base text drops, as `[part, offset, text]`. The viewer shows them struck through at that offset.
- `placed: false` means the change could not be located in the base text. The viewer shows it under the unit.

### `kind: "comments"` (`layers/wolff-divergences.json`)

One item per comment shown under a unit.

```json
{
  "unit": "Prelim.14", "text": "wolff-jus-gentium-1749", "locus": "Jus gentium § 206", "sourceId": "JG.s206",
  "relation": "partly", "severity": 1, "question": "...", "comment": "...",
  "passage": "Vattel's words", "sourcePassage": "Wolff's words", "confidence": 0.55, "links": [["label", "url"]]
}
```

### `kind: "translation"` (`layers/english.json`)

`source` names the translation. `units` maps a unit id to:

```json
{"page": 68, "sents": ["..."], "notes": ["..."], "fr": [[0, 123]], "align": [[[0], [0]]], "flags": [{"k": 0, "fr": "...", "en": "...", "type": "shift", "sev": 2, "note": "..."}]}
```

- `page`: page of the printed translation. `sents`: sentences of the main text. `notes`: footnotes, not aligned.
- `fr`: sentence spans in the unit's `text`. `align`: groups of `[[French sentence indices], [English sentence indices]]`.
- `flags`: translation problems. `k` is the index of the alignment group.

## Reuse tables

`reuse/<from>__<to>.json` holds the reuse found between two texts. Rows are anchored in the units of `from`. `to` is the other text: by default the earlier source that `from` draws on; with `"direction": "derivative"` the later text that repeats `from` (Burlamaqui's *Principes du droit politique*, 1751).

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
- `at` is empty for a row the build could not place on the letters of the text. `where` then says `margin` (the passage is in the marginal summary) or `unplaced`.
- `toUnit` and `toScore`: where `to` is an edition, the unit of that edition that holds the source passage, set by `tools/link_editions.py`. It takes the units printed on the row's page or the next, and keeps the one holding the largest share of the source passage's 5-letter sequences (accents folded, long s and f as one letter), if that share is at least 0.5. The viewer turns the source citation into a link to `viewer/?ed=<to>#<toUnit>` and lists the row under that unit as "reused in".
- `repeats`: where `to` is a later text that repeats an edition (Burlamaqui's PDP 1751 repeats his 1747 text), the unit of that edition the source passage repeats: `{edition, unit, route, score}`. Route `table`: the edition's own table for the later text has a row on the same page whose passage overlaps (≥ 0.5). Route `text`: the passage's wording stands in that unit (≥ 0.7). Set by `tools/link_editions.py`; the catalogue entry of such a table carries `repeats: <edition>`. The viewer shows the link and lists the row under that unit as "reused in … through PDP 1751".
- Optional fields: `nearer` (`DNG` or `Devoirs`: which of the two Pufendorf texts the wording is nearer), `quoting` (an author quoted inside the source passage), `noteRef`, `sourcePart` (the part of the source volume: `barbeyrac_note`, `reflexions`, …), `relation` (in a table whose header lists `relations`).
