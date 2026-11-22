# Screen: where could Vattel have used a source, and chose to make a different or opposite point?

Vattel's *Essai sur le fondement du droit naturel, et sur le premier principe de l'obligation* (written about 1742–1746, printed in *Le loisir philosophique*, Dresde 1747) argues that obligation is the connection of a motive with an action, and that the first principle of obligation is our own good. He follows Wolff and argues against Barbeyrac. The layer being built marks his **divergences** from his sources.

## What a divergence is

A divergence is a place where a source offered Vattel an answer to the question his section treats, so that he could have used it (and sometimes did use part of it), and he chose to make a different or opposite point: a different rule, a different ground for the rule, a condition that changes the result, an opposite conclusion, or a refusal to decide what the source decides.

A divergence is not the same as a counter-argument. Vattel answers Barbeyrac openly in §§ 18 and 30–41. A rebuttal counts only where the two answers to the question differ in substance, and then once, for the question, not once per sentence of the polemic. A divergence also exists where Vattel names no opponent: where he takes Wolff's definition and changes its ground, or where Burlamaqui answers the same question in the same year and Vattel answers it otherwise.

Not a divergence: the same answer in other words; a different topic; a point the source makes and Vattel omits, unless the omission changes the rule; differences of style, length, examples or authorities cited.

## Input (JSON, path given)

A list of items, one per section of the Essai: `vattel_id` (E.13 = § 13), `vattel_margin`, `vattel_text`, `vattel_notes`, `candidates`. Each candidate is a source section: `key` ("<source>|<locus>"), `source`, `locus`, `margin` (Wolff's marginal summary), `text` (cut at 2500 characters), `notes` (cut at 1500; each note marked author or Barbeyrac), `reuse` (labels of the reuse rows already found between the two; empty if none), `why` (own rows, rows of a neighbouring §, or vocabulary). Several candidates may be irrelevant.

Sources:
- `PPU1`: Wolff, *Philosophia practica universalis* I (1738). Latin.
- `TN1`: Wolff, *Theologia naturalis* I (1739), §§ 948–1006. Latin.
- `LOG40`: Wolff, *Discursus praeliminaris de philosophia in genere* (1740). Latin.
- `PUF34`: Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac (1734), with Barbeyrac's notes.
- `DEV56`: Pufendorf, *Les devoirs de l'homme et du citoyen*, trad. Barbeyrac (1756). Loci "Jugement d'un anonyme § n" are Leibniz's *Jugement*; "Réflexions du traducteur § n" are Barbeyrac's reply.
- `GRO24`: Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac (1724), with Barbeyrac's notes.
- `BUR47`: Burlamaqui, *Principes du droit naturel* (Genève 1747).

Every source section, whole, is in `<WORK>/ediv/sections.json` (a dict keyed "<source>|<locus>", each with `text`, `notes`, `margin`, `pages`). Read it with python3 when a candidate is cut, or to look for a section that answers the question better than the candidates do (e.g. the § of Wolff on the same definition, the chapter of Burlamaqui on the same question). Never load the whole file into your reply.

## For each item

1. `question`: the question Vattel's section answers, one short phrase in English. A section that answers two questions: name both, separated by " / ".
2. For each candidate, and for any section you add: decide
   - `same_question`: true only if the source section answers that question or an immediate part of it. Same topic is not the same question.
   - `relation` (only when same_question): `follows` (same answer, same ground; wording may differ), `diverges` (a different answer, ground or conclusion), `partly` (same answer, but a qualification, exception or ground added or dropped that changes what the rule does).
   - `source_answer`, `vattel_answer`: one sentence each, in English, only for `diverges` and `partly`.
   - `source_passage`: the exact words of the source's answer, copied from its `text` or `notes` (for a note, copy from the note's text, not its bracketed mark), only for `diverges` and `partly`.
   - `vattel_passage`: the exact words of Vattel's answer, copied from `vattel_text` or `vattel_notes`, only for `diverges` and `partly`.
   - `confidence` 0–1.
   - `added`: true for a section you found yourself (give its `key`).

Report only the pairs with same_question true for added sections. Be sceptical: in a text that follows Wolff, expect `diverges` in a small share of the pairs. Where Vattel quotes Barbeyrac or Leibniz to reject him, the quoted passage is the source's answer; record the divergence once, at the section where Vattel states his own answer.

## Output

Write with python3 a JSON file (path given): `{"items":[{"vattel_id","question","pairs":[{"key","same_question","relation","source_answer","vattel_answer","source_passage","vattel_passage","confidence","added"}]}]}`. Check that every passage is an exact substring of its text before writing. Work through every item and every candidate. Keep helper files in your scratch folder (given). Reply with one line: number of items; counts of follows / partly / diverges.
