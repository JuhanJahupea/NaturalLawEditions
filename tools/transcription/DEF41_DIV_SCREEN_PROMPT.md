# Screen: where does Vattel's *Défense* depart from Leibniz or Wolff?

Vattel's *Défense du système leibnitien* (1741) defends Leibniz's and Wolff's system against Crousaz. He quotes the *Théodicée* and Wolff's *Psychologia rationalis* in support. The layer being built marks the places where, while defending them, he **diverges** from them: he states the doctrine with a different rule, a different ground, a condition or qualification that changes what it does, a softer or stronger claim (a certainty turned into a probability, a thesis turned into a hypothesis), an interpretation the source does not give, or a refusal to hold what the source holds. Disagreements with Crousaz and Roques are recorded elsewhere: ignore them.

Not a divergence: the same answer in other words; a summary; a different topic; a point the source makes and Vattel omits, unless the omission changes the doctrine; differences of style, length, examples or authorities. Expect divergences in a small share of the pairs: Vattel is a faithful defender.

## Input (JSON, path given)

`items`: one per unit of the *Défense* that reuses Leibniz or Wolff. `vattel_id` (D.n = paragraph n; Pref.k = a page of the Préface), `vattel_text` (italics _…_, page breaks [p. N]), `vattel_notes`, `candidates`: the segments the reuse rows name, each with `key`, `locus`, `text` (cut at 4000 characters), `reuse` (labels and stance of the rows). Segments: `THEO.<id>` Leibniz, *Théodicée* (Janet's modern spelling; T.n = § n, Disc.n = Discours § n, Abr.n = Abrégé objection n, King.n = Remarques sur King § n); `PSR34.<n>` Wolff, *Psychologia rationalis* § n (Latin; its note after "[Nota]").

Every segment, whole, is in `<DIR>/segments.json` (a dict keyed by segment id). Read it with python3 when a candidate is cut, or to add a segment that answers the unit's question better (another § of the Théodicée, another § of Wolff). Never load the whole file into your reply.

## For each item

1. `question`: the question Vattel's unit answers, one short phrase in English.
2. For each candidate, and any segment you add: `same_question` (true only if the segment answers that question or an immediate part of it); if true, `relation`: `follows` (same answer and ground), `diverges` (different answer, ground or conclusion), `partly` (same answer, with a qualification, condition or ground added or dropped that changes what it does). For `diverges` and `partly` also: `source_answer` and `vattel_answer` (one sentence each, English), `source_passage` (exact words copied from the segment text), `vattel_passage` (exact words copied from `vattel_text` or a note), `confidence` 0–1. `added`: true for a segment you found yourself.

## Output

Write with python3 a JSON file (path given): `{"items":[{"vattel_id","question","pairs":[{"key","same_question","relation","source_answer","vattel_answer","source_passage","vattel_passage","confidence","added"}]}]}`. Check every passage as an exact substring before writing. Keep helper files in your scratch folder (given). Reply with one line: items; follows / partly / diverges.
