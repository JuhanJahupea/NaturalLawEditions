# Check the label of a reuse row

Input JSON (path given): a list of reuse rows from two editions (Vattel 1773, Burlamaqui 1747). Each row says that the edition's "passage" takes something from the source's "source_passage", with a "label". "word_overlap" is the share of the shorter passage's words that occur in the same order in the other (accents and old spellings folded); it was used to pick these rows because it sits far from what the label usually shows.

Labels:
- verbatim: the same words for at least a clause (small differences of spelling, punctuation or a word or two allowed);
- close paraphrase: the same sentence structure and most of the content words, reworded in places;
- loose paraphrase: the same content in other words and another structure;
- shared argument: the same argument or reasoning, expressed independently;
- translation: the passage translates the source (another language).

For each row give the label that fits the two passages as they stand: keep the current one if it fits. Judge the wording, not the overlap figure alone: a long passage can share a verbatim clause inside a looser paraphrase (choose by the reused stretch as a whole), and a short passage can have high overlap from stock words.

Output: write with python3 a JSON file (path given): {"items": [{"key", "label", "changed": true|false, "reason": "one short sentence"}]}
One item per row. Keep helper files in your own scratch folder (given). Reply with one line: rows; changed, by old → new label.
