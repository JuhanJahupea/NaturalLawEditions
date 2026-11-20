# Reuse in the passages Vattel's *Droit des gens* added in 1773

The edition of Vattel's *Le droit des gens* published at Neuchâtel in 1773 adds notes and phrases that Vattel prepared for a new edition before his death in 1767. The reuse tables of the edition hardly cover them. You read these additions and list every passage where Vattel takes something from his main sources.

## Input (JSON, path given)

`items`: one per addition: `unit` (section id, e.g. I.106), `change`, `type` (added note, added to note, added phrase, rewording, correction), `content` (a summary), `added` (the added text: `part` t = the section's text, nK = its note K; `text`), `unit_text` and `notes` (the whole section, for context), `rows_overlapping` (rows the tables already have on the added text).

## Sources (read with python3; never load a whole file into your reply)

- `JG`: Wolff, *Jus gentium* (1749), `<WORK>/srcp/JG.json`; `INST`: Wolff, *Institutiones juris naturae et gentium* (1750), `<WORK>/srcp/INST.json`. `pages` [{`id` e.g. `JG.pdf567`, `text`, `starts` [[offset, §]], `carried`, `margin`}]; `first_page_of` {"669": "JG.pdf567"}.
- `GRO24`: Grotius, trad. Barbeyrac (1724), `<WORK>/corpus/GRO24.json`; `PUF34`: Pufendorf, *Droit de la nature et des gens*, trad. Barbeyrac (1734), `<WORK>/corpus/PUF34.json`. `pages` [{`id` e.g. `GRO24T1.p301`, `text`, `spans` [[start, end, locus]], `margin` [{text, locus}], `notes` [{mark, by, text, locus}]}]; Barbeyrac's notes count.
- `BUR47`: Burlamaqui, *Principes du droit naturel* (1747), `/home/user/NaturalLawEditions/editions/burlamaqui-1747/text.json` (`units` [{`id` e.g. `P1.6.9`, `text`, `notes`}]).
- Start from Vattel's own references in the added text; then the § of Wolff on the same matter (Vattel follows the *Jus gentium* in order); then search each source for distinctive words.

## What counts

Vattel takes wording, or a specific argument, definition, example or order of points, from the source passage; or translates it; or cites it; or takes it up to reject it. A doctrine every writer states is not enough unless the wording is shared.

## Each row (`found`)

- `unit`; `passage`: Vattel's words, copied exactly from the added text (copy, never retype); the reused stretch only.
- `text`: `JG`, `INST`, `GRO24`, `PUF34` or `BUR47`; `page` (BUR47: the unit id); `source_passage`: copied exactly from that page's `text`, one of its `notes` or `margin` entries (BUR47: the unit's text or a note).
- `french` (Wolff only): a plain French rendering of `source_passage`.
- `label`: `translation`, `verbatim`, `close paraphrase`, `loose paraphrase`, `shared argument`, `citation`, `open disagreement`; `confidence` 0.3–1 (0.5 or more: a match you would defend); `reason`: one sentence.
- `covered_by`: the id of a row in `rows_overlapping` that already pairs this stretch with this source passage, or null.

Also give per item `named`: the sources Vattel names in the added text that are not among these five (author and work, one line each), so that they can be added later.

## Output

Write with python3 a JSON file (path given): `{"items": [{"change", "unit", "found": [...], "named": ["..."], "searched": "one line"}]}`. Check that every `passage` occurs in its section and every `source_passage` on its page (exact substrings) before writing. Keep helper files in your scratch folder (given). Reply with one line per item: rows found by source.
