# Check of doubtful reuse rows in Vattel's *Défense du système leibnitien* (1741)

A first judge read Vattel's units with candidate passages of his sources (Crousaz's *Examen* 1737 and *Commentaire* 1738, both Google OCR; Leibniz's *Théodicée*, Janet's modern-spelling text; Wolff's *Psychologia rationalis*, Latin) and wrote reuse rows. You check the rows it was least sure of. Vattel defends Leibniz and Wolff against Crousaz: he quotes Crousaz to refute him and quotes Leibniz and Wolff in support.

Input JSON (path given): `items` [{`key`, `unit`, `where`, `passage` (Vattel's words), `seg`, `locus`, `source_passage`, `label`, `confidence`, `reason` (the judge's), `unit_text` (the whole unit, italics as _…_, notes after "NOTES:"), `segment_text` (the whole source segment)}].

For each row decide:
- `keep`: Vattel takes this passage of the source (quotes, cites, translates, paraphrases it, or takes it up to reject it). Give the right `label` (quotation, translation, verbatim, close paraphrase, loose paraphrase, shared argument, citation, open disagreement) and a `confidence` (0.5–1).
- `weak`: there is a link, but it could come from elsewhere: the same doctrine stated in other words, a topic both treat, a stock argument. Give `label` and `confidence` (0.3–0.45).
- `drop`: no reuse: shared vocabulary, a stock phrase, a different point, or the wrong segment.

Be sceptical of `shared argument` and `loose paraphrase` rows: keep them only if the argument is specific (its steps, its example, its order) and not just Leibnizian doctrine any defender would state. A row whose source is the wrong segment while another § of the same work holds the words is `drop`, with that § named in the reason.

Output: write with python3 a JSON file (path given): `{"verdicts": [{"key", "verdict", "label", "confidence", "reason"}]}`, one per item. `reason`: one sentence. Reply with one line: items, keep / weak / drop.
