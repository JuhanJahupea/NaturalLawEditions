# Recall check: what reuse of Wolff, Grotius and Pufendorf do Vattel's tables miss?

Vattel, *Le droit des gens* (1773), has reuse tables: rows that pair a passage of Vattel with a passage of a source. They were built by retrieval and a language-model judge. This check measures how much they miss. You read a few of Vattel's sections whole, with his four main sources, and list every reuse you find, saying whether a row already covers it.

## Input (JSON, path given)

`units`: Vattel sections. Each has `text`, `notes` (list), `margin`; `rows` (every row the section has, in all tables: `id`, `table`, `locus`, `label`, `status` match or possible, `passage`, `source_passage`); `pages_cited_nearby` (pages of the four sources that rows of this section and the four sections on each side cite).

## Sources (read with python3; do not load whole files into your reply)

- `JG`: Wolff, *Jus gentium* (1749), `<WORK>/srcp/JG.json`; `INST`: Wolff, *Institutiones juris naturae et gentium* (1750), `<WORK>/srcp/INST.json`. `pages` [{`id` e.g. `JG.pdf567`, `text`, `starts` [[offset, §]], `carried`, `margin`}]; `first_page_of` {"669": "JG.pdf567"}. Vattel follows *Jus gentium* closely, often in Wolff's order.
- `GRO24`: Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac (1724), `<WORK>/corpus/GRO24.json`; `PUF34`: Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac (1734), `<WORK>/corpus/PUF34.json`. `pages` [{`id` e.g. `GRO24T1.p301`, `text`, `spans` [[start, end, locus]], `margin` [{text, locus}], `notes` [{mark, by, text, locus}]}]. Barbeyrac's notes count as part of these sources.
- Start from `pages_cited_nearby`, Vattel's own citations in his notes, and the § of Wolff that treats the same matter; then search each source for the section's distinctive words and examples (accents and spelling vary). Spend most effort on Wolff's *Jus gentium* and on Grotius.

## What counts as reuse

Vattel takes wording, or a specific argument, definition, example or order of points, from the source passage (the standard of a "right" row in the project's audit). A doctrine every writer states is not reuse unless the wording is shared. A citation of the source by Vattel counts.

## What to report

For each section, list every reuse of the four sources you find (`found`), one item per reused stretch and source passage:
- `unit`; `passage`: Vattel's words, copied exactly from `text`, a note or `margin` (copy, do not retype);
- `text`: `JG`, `INST`, `GRO24` or `PUF34`; `page`; `source_passage`: copied exactly from that page's `text`, or one of its `notes` or `margin` entries;
- `french` (Wolff only): a plain French rendering of `source_passage`;
- `label`: `translation`, `verbatim`, `close paraphrase`, `loose paraphrase`, `citation` or `open disagreement`; `confidence` 0.3–1 (0.5 or more: a match you would defend);
- `reason`: one sentence;
- `covered_by`: the id of a row in `rows` that pairs this Vattel stretch (or most of it) with this source passage or another passage of the same § saying the same; `null` if no row does.

Also give, per section, `rows_wrong`: ids of rows (of these four tables) that you think pair passages with no reuse between them, with a short reason. Do not review the other tables.

## Output

Write with python3 a JSON file (path given): `{"sections": [{"unit", "found": [...], "rows_wrong": [{"id", "why"}], "searched": "one line: what you searched"}]}`. Check that every `passage` occurs in its unit and every `source_passage` on its page (exact substring). Keep helper files in your scratch folder (given). Reply with one line per section: reuse found, covered, not covered.
