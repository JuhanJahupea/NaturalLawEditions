# Audit: is this reuse row right?

You are auditing a random sample of reuse rows from two editions: Vattel, Le droit des gens (1773), and Burlamaqui, Principes du droit naturel (1747). A reuse row says that a passage of the edition takes something from a passage of a source text. The rows were found by retrieval and judged by a language model. Your verdicts estimate how often the rows are right.

Input JSON (path given): a list of rows:
{"key", "edition", "table", "unit", "source" (author, title, date), "family", "locus", "label", "passage" (the edition's words), "context" (the edition's text around the passage), "in" (text, note or margin), "source_passage" (the source's words), "french" (a working French translation of a Latin source passage, when there is one), "reason" (the first judge's reason)}
Labels: verbatim; close paraphrase; loose paraphrase; shared argument; translation; citation (the edition names this source for this passage); open disagreement (the edition rejects or corrects this passage). Some tables are not sources but parallel or later texts (Formey 1758, Burlamaqui's own Principes du droit politique 1751 and Élémens 1783, Vattel's own works): there the row says the two texts share the passage, whichever came first.

For each row decide, reading the two passages and the context, and not trusting the first judge's reason:
- verdict:
  - "right": the relation the label claims holds. For the reuse labels: the edition's passage takes wording, or a specific argument, sequence, definition or example, from this source passage (or shares it, for the parallel texts). For citation: the edition names this source for this passage. For open disagreement: the edition takes up and rejects or corrects this source's claim.
  - "weak": the two passages treat the same point and the link is plausible, but nothing in them is specific enough to show that the edition draws on this source rather than on the common stock of natural-law writing (a stock definition, a commonplace maxim, a shared ancient example without the surrounding argument).
  - "wrong": the passages do not match (different point, mismatched passages, a relation the texts do not show).
- label_ok: true if the label fits (e.g. "verbatim" needs the same words for at least a clause; "close paraphrase" the same sentence structure and most content words; "loose paraphrase" the same content in other words). For "weak" and "wrong" rows give false only if the label would be wrong even if the link held.
- better_label: if label_ok is false, the label that fits; else "".
- reason: one short sentence in English.

These rows are all from Vattel's tables for Pufendorf (Barbeyrac's translation, 1734) and for Burlamaqui (Principes du droit naturel, 1747; Principes du droit politique, 1751, printed after Vattel's sources but before 1758). An earlier sample found many of them weak: Vattel's wording or argument often follows Wolff's Jus gentium or Grotius, and Pufendorf or Burlamaqui only states the same doctrine. Where you see that, say so in the reason. The transcriptions of Pufendorf (texts/pufendorf-barbeyrac-1734/), Grotius (texts/grotius-barbeyrac-1724/) and Wolff (texts/wolff-jus-gentium-1749/, texts/wolff-institutiones-1750/) are in the repository at /home/user/NaturalLawEditions if you need the source in context.
Be strict and even-handed. Do not give "right" for topic overlap alone; do not give "wrong" when wording differs but the specific argument is the same.

Output: write with python3 a JSON file (path given): {"items": [{"key", "verdict", "label_ok", "better_label", "reason"}]}
One item per row. Keep helper files in your own scratch folder (given). Reply with one line: rows; right / weak / wrong; labels not ok.
