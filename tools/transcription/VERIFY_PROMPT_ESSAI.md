# Second reading: is this reuse row right?

You are checking every match row of the reuse tables of Vattel's *Essai sur le fondement du droit naturel* (1747). A reuse row says that a passage of the Essai takes something from a passage of a source text. A first reader (a language model) wrote the rows while reading the Essai with Wolff's *Philosophia practica universalis* I (1738), Barbeyrac's translations of Pufendorf (*Droit de la nature et des gens*, *Devoirs*, with Leibniz's *Jugement d'un anonyme* and Barbeyrac's *Réflexions*) and of Grotius, and Burlamaqui's *Principes du droit naturel* (1747, printed the same year as the Essai: there a row says the two texts share the passage, whichever came first). Your verdicts decide which rows stay matches. Where you need more context, the sources are in <WORK>/srcp/PPU1.json (Wolff, pages with text) and <WORK>/corpus/DEV56.json, PUF34.json, GRO24.json (pages with text and notes); Burlamaqui in /home/user/NaturalLawEditions/editions/burlamaqui-1747/text.json.

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

Be strict and even-handed. Do not give "right" for topic overlap alone; do not give "wrong" when wording differs but the specific argument is the same.

Output: write with python3 a JSON file (path given): {"items": [{"key", "verdict", "label_ok", "better_label", "reason"}]}
One item per row. Keep helper files in your own scratch folder (given). Reply with one line: rows; right / weak / wrong; labels not ok.
