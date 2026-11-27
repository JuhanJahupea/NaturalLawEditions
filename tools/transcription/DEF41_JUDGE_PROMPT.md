# Reuse in Vattel's *Défense du système leibnitien* (1741)

Vattel defends Leibniz's and Wolff's system against Jean-Pierre de Crousaz's *Examen de l'Essai de M. Pope sur l'homme* (1737) and *Commentaire* on Du Resnel's translation (1738). Partie I sets out the system and answers the *Examen*; Partie II ch. I–VI answer the *Examen* point by point, ch. VII the *Commentaire*, ch. VIII Pierre Roques's letters. Vattel quotes Crousaz in order to refute him, usually with a page ("(p. 58.)"), and quotes Leibniz's *Théodicée* and Wolff's *Psychologia rationalis* in support. You read a batch of his units with candidate passages of these sources and list every place where Vattel takes something from them.

## Input (JSON, path given)

- `items`: Vattel's units. `unit` (D.n = his paragraph n; Pref.k / Ded.k = a page of the Préface or dedication), `part`, `chap`, `text`, `notes` [{mark, text}]. In `text` and notes, italics are shown as _…_ and the page breaks of the *Défense* as [p. N]. `candidates`: segment ids to read. `cited`: the candidates Vattel himself cites in the unit. `shared`: runs of five or more words the unit has in common with a candidate (found by machine, lower case, accents dropped, s and f merged): check each one; many are stock phrases.
- `segments`: {id: {src, locus, part, text}}.
  - `EXA37.p<page>`: Crousaz, *Examen*, one printed page. `COM38.p<page>`: Crousaz, *Commentaire*, one printed page. Both are Google's OCR: long s often read as f ("fon" for "ſon"), words run together, stray letters. Copy the OCR as it stands.
  - `THEO.<id>`: Leibniz, *Théodicée*, one section (T.n = § n of the Essais; Disc.n = Discours de la conformité § n; Pref.n = Préface paragraph; Abr.n = Abrégé, objection n; Hob.n = Réflexions sur Hobbes § n; King.n = Remarques sur King § n). Modern spelling (Janet's edition): Vattel's 1734 text differs in spelling and accents, not in words.
  - `PSR34.<n>`: Wolff, *Psychologia rationalis* § n, with its note after "[Nota]". Latin. Vattel quotes it in Latin or renders it in French.

Read every candidate of every item in full. Most uncited candidates are false positives.

You may search beyond the candidates in two cases, with python3 on `<DIR>/segments.json` (all segments, same form): when Vattel quotes Leibniz or Wolff and no candidate holds the words; and for Wolff's Latin, by subject, with the index of § summaries `<DIR>/PSR34_index.tsv` (id, Wolff's marginal summary). Do not read the whole file into your reply.

Leave out Vattel's quotations of Roques's letters (Partie II ch. VIII): they are recorded separately. Words of Leibniz or Wolff that Vattel quotes from Roques's letter are recorded here, with `via` "Roques".

## What counts

Vattel quotes or cites the source passage; or takes wording, or a specific definition, argument, example or order of points, from it; or takes it up to reject it. The same topic, a doctrine every writer states, or stock phrases ("il est vrai que", "en un mot") are not enough.

## Each row

- `unit`; `where`: "text" or "note (a)" etc.; `passage`: Vattel's words, copied exactly from the item's text or note, _ marks and [p. N] included. The reused stretch only: a clause to a few sentences. One row per continuous stretch; a long quotation broken by Vattel's comment gives one row per piece.
- `seg`: the segment id; `source_passage`: copied exactly from that segment's `text`, one continuous stretch.
- `label`: `quotation` (Vattel quotes the source and marks it: italics, quotation marks, "dit-il", a page reference), `translation` (Vattel renders Wolff's Latin closely), `verbatim` (the same words, unmarked), `close paraphrase`, `loose paraphrase`, `shared argument`, `citation` (Vattel names or cites this passage without taking its words), `open disagreement` (Vattel takes the passage up, in his own words, to reject it).
- `stance`: `rejects` (Vattel takes it up to refute it), `adopts` (he uses it in support), `neutral`.
- `confidence`: 0.3–1 (0.5 or more: a match you would defend).
- `named`: if Vattel names the source for this passage in the same sentence or its note: {"form": "quotation" or "reference", "cue": his words that name it, copied exactly, e.g. "(p. 58.)" or "Théod. §. 9."}; else omit.
- `quoting`: if both texts quote a third author (Pope, Bayle, Scripture…), that author; else "".
- `via`: "Roques" if the words come to Vattel through Roques's letter; else omit.
- `reason`: one sentence.

## Output

Write with python3 a JSON file (path given): `{"rows": [...], "units": [{"unit", "searched": "one line: candidates read, what you found"}]}`. Before writing, check that every `passage` occurs in its item's text or note, and every `source_passage` in its segment's text, as exact substrings; fix any that do not. Keep helper files in your scratch folder (given). Reply with one line: units, rows by source and label.
