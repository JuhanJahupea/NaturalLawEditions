# Full pass: Vattel's *Droit des gens* (1773) with Wolff's *Jus gentium* and Barbeyrac's Pufendorf

Vattel, *Le droit des gens* (1773), has reuse tables: rows that pair a passage of Vattel with a passage of a source. A recall check found that they hold about half of the reuse of Wolff's *Jus gentium* and a fifth of that of Pufendorf. You read a run of Vattel's sections whole, each beside the § of the *Jus gentium* it follows and pages of Pufendorf's *Droit de la nature et des gens* in Barbeyrac's translation (with Barbeyrac's notes), and list every reuse you find, saying whether a row already covers it.

## Input (JSON, path given)

`units`: Vattel sections, in order. Each has `text`, `notes` (list), `margin`; `rows` (the section's rows in the tables of the *Jus gentium* `JG`, the *Institutiones* `INST` and Pufendorf `PUF34`: `id`, `table`, `locus`, `label`, `status` match or possible, `passage`, `source_passage`); `jus_gentium`: the §§ of the *Jus gentium* the section follows or lies between, each {`s`, `page`, `margin` (Wolff's marginal summary), `text`}; `jus_gentium_pages`: pages of rows whose locus is not a § (the Praefatio); `pufendorf_pages`: page ids of Pufendorf near the section (cited by rows around it, cited by Vattel, or close in vocabulary).

## Sources (read with python3; never load a whole file into your reply)

- `JG`: Wolff, *Jus gentium* (1749), `<WORK>/srcp/JG.json`: `pages` [{`id` e.g. `JG.pdf567`, `text`, `starts` [[offset, §]], `carried`, `margin`}]; `first_page_of` {"669": "JG.pdf567"}. Vattel follows the *Jus gentium* closely, mostly in Wolff's order, often translating. The §§ given are a start: read the § before and after when Vattel's section runs on, and follow Wolff's cross-references.
- `PUF34`: Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac (1734), `<WORK>/corpus/PUF34.json`: `pages` [{`id` e.g. `PUF34T2.p301`, `text`, `spans` [[start, end, locus]], `margin` [{text, locus}], `notes` [{mark, by, text, locus}]}]. `by` "author" marks Pufendorf's own notes; the other notes are Barbeyrac's. Look above all for Pufendorf's examples (ancient and modern cases, quotations) and for Barbeyrac's notes, which Vattel uses beside Grotius; search the corpus for a section's distinctive names, cases and words (accents and spelling vary), not only the pages given.

## What counts as reuse

Vattel takes wording, or a specific argument, definition, example or order of points, from the source passage; or translates it; or cites it; or takes it up to reject it. A doctrine every writer states is not reuse unless the wording is shared.

## What to report

For each section, every reuse of `JG` or `PUF34` you find (`found`), one item per reused stretch and source passage:
- `unit`; `passage`: Vattel's words, copied exactly from `text`, a note or `margin` (copy, never retype); the reused stretch only (a clause to a few sentences);
- `text`: `JG` or `PUF34`; `page`; `source_passage`: copied exactly from that page's `text`, one of its `notes` or `margin` entries;
- `french` (JG only): a plain French rendering of `source_passage`;
- `label`: `translation`, `verbatim`, `close paraphrase`, `loose paraphrase`, `shared argument`, `citation` or `open disagreement`; `confidence` 0.3–1 (0.5 or more: a match you would defend);
- `reason`: one sentence;
- `covered_by`: the id of a row in `rows` that pairs this Vattel stretch (or most of it) with this source passage, or with another passage of the same § saying the same; `null` if no row does.

Also give, per section, `rows_wrong`: ids of rows in `rows` that pair passages with no reuse between them, with a short reason.

## Output

Write with python3 a JSON file (path given): `{"sections": [{"unit", "found": [...], "rows_wrong": [{"id", "why"}], "searched": "one line"}]}`, one entry per section, sections with nothing found included. Check that every `passage` occurs in its unit and every `source_passage` on its page (exact substrings) before writing. Keep helper files in your scratch folder (given). Reply with one line: sections, reuse found (covered / not covered) by source, rows judged wrong.
