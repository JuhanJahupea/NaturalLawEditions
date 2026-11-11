# Second judge: weak reuse rows

Input JSON (path given): {"edition": "...", "source": "...", "items": [...]}. Each item is one reuse row that a first judge found but rated weakly (confidence 0.3–0.45):
{"key": "6001", "unit": "II.8", "part": "text" | "note (a)" | "margin", "edition_text": "...", "passage": "...", "source_locus": "Liv. II ch. III § 23, n. 3", "source_part": "note by Barbeyrac" | "text" | ..., "source_text": "...", "source_passage": "...", "label": "loose paraphrase", "confidence": 0.4, "reason": "..."}
- edition_text is the part of the edition's section that holds the passage (main text, a footnote or the marginal summary). passage is the stretch the first judge marked in it.
- source_text is the part of the source page that holds source_passage, from a careful transcription of the printed book (long s printed as s, line-end hyphens joined). Source notes are by Barbeyrac (the translator) or by the author.
- label, confidence and reason are the first judge's. Do not trust them. Read both texts afresh.

The edition is the later text. Decide for each row whether its author took this passage from this source or engages it:
- verdict "keep": the edition reuses the source passage. Shared wording, or the same argument in the same order, or the same unusual example or distinction used to the same end, or an explicit reference to this author for this point, or an explicit rejection of this passage.
- verdict "commonplace": the shared matter is a stock idea, phrase, maxim, definition or classical example of the natural-law tradition. It cannot tie the edition to this source.
- verdict "drop": no reuse. Same topic or shared vocabulary only, or the two passages say different things.

For "keep" give a label:
- verbatim: the same French words for at least a clause;
- close paraphrase;
- loose paraphrase;
- citation: the edition names this author or work for this passage;
- open disagreement: the edition rejects or corrects this passage.

Give your own confidence 0–1 that the edition's author used this source here (for "commonplace": that the shared matter is there at all). Be sceptical. Pufendorf and Barbeyrac were read by everyone: a shared idea is reuse only where wording, sequence or a distinctive turn ties the passage to this page. Keep the first judge's passages; you cannot change them.

Output: write with python3 a JSON file (path given): {"items": [{"key", "verdict", "label", "confidence", "reason"}]}
reason: one sentence in English naming what ties the two passages, or why nothing does. Work through every item. Keep helper files in your own scratch folder (given). Reply with one line: number of items; keep / commonplace / drop.
