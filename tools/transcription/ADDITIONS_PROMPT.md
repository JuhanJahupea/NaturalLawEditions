# Add the reuse rows an audit named but the tables lack (Vattel 1773)

Vattel, *Le droit des gens* (1773), has reuse tables: rows that pair a passage of Vattel with a passage of a source. An audit read rows of the tables for Pufendorf and Burlamaqui and rated many of them weak: Pufendorf or Burlamaqui says the same thing, but Vattel's wording or argument follows another source, which the audit reason names (Wolff's *Jus gentium*, Wolff's *Institutiones*, or Grotius in Barbeyrac's translation). Your task: find that passage of Wolff or Grotius and, where Vattel draws on it and the tables lack the row, write the row.

## Input (JSON, path given)

`units`: Vattel sections. Each has `text`, `notes` (list), `margin`; `weak_rows` (the weak rows: `passage`, `source_passage`, `audit_reason`; `named_not_in_tables`: the loci the reason names that have no row in this unit, e.g. `JG 669`, `INST 804`, `GRO24 2.16.32` = Liv. II ch. XVI § 32); `rows_in_tables` (the rows this unit already has in the Wolff and Grotius tables).

## Sources (read with python3; do not load whole files into your reply)

- `<WORK>/srcp/JG.json` (Wolff, *Jus gentium*, 1749) and `<WORK>/srcp/INST.json` (Wolff, *Institutiones*, 1750): `pages` [{`id` e.g. `JG.pdf567`, `text`, `starts` [[offset, §]] (where each § begins in `text`), `carried` (the § running at the top of the page), `margin`}]; `first_page_of` {"669": "JG.pdf567"}. A § can run onto the next pages.
- `<WORK>/corpus/GRO24.json` (Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac, 1724): `pages` [{`id` e.g. `GRO24T1.p301`, `text`, `spans` [[start, end, locus]] over `text`, `margin` [{text, locus}], `notes` [{mark, by, text, locus}]}]. Loci look like `Liv. II ch. XVI § 32`; Barbeyrac's notes have `by` empty or `Barbeyrac` and a locus ending `, n. 3`.
- The reason may name a neighbouring § or the wrong book; look around it. You may search the whole text for words of Vattel's passage.

## What to write

For each weak row, read the named passage in context. Write a row only if Vattel takes wording, or a specific argument, definition, example or order of points, from that passage (the standard of the audit's "right"). Stock doctrine stated by every writer is not enough. Do not write a row that `rows_in_tables` already has: the same Vattel stretch with the same source passage, or a source passage of the same § that covers the same point.

Each row:
- `unit`; `passage`: Vattel's words, copied exactly from the unit's `text`, one of its `notes`, or `margin` (copy, do not retype: spacing and spelling as in the input). The reused stretch only: a clause to a few sentences.
- `text`: `JG`, `INST` or `GRO24`; `page`: the page id; `source_passage`: copied exactly from that page's `text`, or from one of its `notes` or `margin` entries (Grotius). The stretch Vattel uses.
- `french` (Wolff only): a plain French rendering of `source_passage`.
- `label`: `translation` (Vattel translates the Latin closely), `verbatim`, `close paraphrase` (same structure, most content words), `loose paraphrase` (same content, other words and structure), `citation` (Vattel names or cites this passage), `open disagreement` (Vattel takes up the passage and rejects it).
- `confidence`: 0.3–1 (0.5 or more: a match you would defend; below 0.5: possible).
- `reason`: one sentence on what Vattel takes.
- `for_row`: the weak row's id.

If you write no row for a weak row, list it in `none` with a short reason (the reason does not hold; the table already has it; the passage could not be found).

## Output

Write with python3 a JSON file (path given): `{"rows": [...], "none": [{"for_row", "why"}]}`. Check before writing that every `passage` occurs in its unit and every `source_passage` on its page (exact substring). Keep helper files in your scratch folder (given). Reply with one line: weak rows read; rows written (match / possible); none.
