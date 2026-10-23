# Judge: reuse of a source in an edition, from a new transcription of the source

Input JSON (path given):
{"edition": "...", "source": "...", "pages": {"<page_id>": {"printed": "160", "parts": [{"k": 0, "part": "text", "locus": "Liv. I ch. III § 21", "text": "..."}, {"k": 3, "part": "note", "by": "Barbeyrac", "locus": "Liv. I ch. III § 21, n. 4", "text": "..."}, ...]}},
 "items": [{"unit": "I.5", "margin": "...", "text": "...", "notes": [{"mark": "(a)", "text": "..."}], "candidates": ["GRO24T1.p214", ...]}]}

- The edition is the later text. Each item is one of its sections (or printed pages, for a preface): its marginal summary, its text and its footnotes.
- The source pages are a careful transcription of the printed book (long s printed as s, line-end hyphens joined). Parts: "text" is the author's main text, cut where a numbered paragraph starts; "note" is a footnote, by "Barbeyrac" (the translator's notes) or by the author (the author's own notes, translated); "margin" is a marginal summary or the author's lettered reference.
- Candidate pages were retrieved automatically by word overlap. Most are false positives.

Task: for each item decide which candidate pages the edition's author actually reuses or engages. Be sceptical: shared natural-law vocabulary, the same topic, or the same classical example (Livy, Cicero, the Digest, Scripture) is NOT reuse unless argument, sequence or wording is shared. When both texts quote the same ancient text, that is "commonplace" unless the surrounding argument also follows the source. Read only the candidates listed for the item.

Labels (one per match):
- verbatim: the same French words for at least a clause;
- close paraphrase;
- loose paraphrase;
- commonplace;
- citation: the edition names this author or work for this passage;
- open disagreement: the edition rejects or corrects this passage.

For every match give:
- unit; page_id; k: the part of that page that holds the source passage;
- passage: exact words copied from the item's text, margin or notes (the reused part only, one continuous stretch);
- source_passage: exact words copied from part k (the reused part only, one continuous stretch);
- label; confidence 0–1; reason (one sentence, in English);
- quoting: the ancient or other author both texts quote, if the shared matter is a quotation; else "".
One match per reused stretch. Several stretches of one item may match the same page.

Output: write with python3 a JSON file (path given): {"matches": [{"unit", "page_id", "k", "passage", "source_passage", "label", "confidence", "reason", "quoting"}], "no_match": ["<unit>", ...]}
Copy passages exactly, character for character, including spaces before punctuation; no paraphrase, no ellipsis. Work through every item. Keep helper files in your own scratch folder (given). Reply with one line: number of items, number of matches by label.
