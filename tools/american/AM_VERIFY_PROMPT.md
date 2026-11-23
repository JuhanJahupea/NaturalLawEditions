# Second reading: Vattel in American documents, and what of Vattel's own each reuse carries

Input JSON (path given): {"items": [{"key", "match", "doc", "context", "vattel_english", "vattel_french", "vattel_french_notes", "source_rows", "divergences"}]}

- `match` is a first judge's finding that an American passage reuses a section ("unit") of Vattel's *Le droit des gens*: the American words (`passage`), the Vattel words in the 1797 English (`vattel`), a label and the judge's guess at the document.
- `context` is the OCR text around the passage (2,500 characters before, 1,500 after), from a printed volume (`doc`): a pamphlet, a volume of collected writings (Samuel or John Adams), the Massachusetts state papers, or the journals of Congress. Look for the document's heading, date and the running heads with page numbers.
- `vattel_french` is the same section in the French of 1773; `source_rows` are the edition's findings of Vattel's own sources for passages of this French section (Wolff's *Jus gentium*, *Institutiones*, *Jus naturae* VIII; Grotius and Pufendorf in Barbeyrac's French; Burlamaqui; Vattel's earlier works; and others), each with the French words of Vattel it concerns (`vattel_french`) and the source's words. `divergences` are places where Vattel had a source before him and reached the opposite point.

For each item:
1. verdict: keep, relabel, or reject. Labels: quotation (marked or named as Vattel's), verbatim (Vattel's words without marks, a clause or more), close paraphrase, loose paraphrase, reference (Vattel named for the point, without his words). Reject if the shared matter is too common to show use of Vattel, or if the passage follows another author.
2. document: author, title or kind, date, as precise as the context allows. Give the page of the printed volume if a running head shows it. Say whether the stretch is the author's own text, a quotation of someone else (e.g. the House quoting the Governor), or an editor's note.
3. french: the French words of `vattel_french` that the reused English renders (exact copy, one continuous stretch).
4. source: for those French words, which `source_rows` cover them (the row's `vattel_french` overlaps them), as a list of {"text", "locus", "label"}; the closest Wolff row first. If no row covers them, say "none". Then the relation in one word: "wolff" (a Wolff row with label translation, verbatim or close paraphrase covers them), "wolff-loose" (only a loose paraphrase or shared argument of Wolff), "other" (rows of other sources only), "own" (no row), "against-wolff" (a divergence note from Wolff concerns these words).
5. note: one or two sentences in English: what the American writer does with the passage, and anything the first judge got wrong.

Output: write with python3 a JSON file (path given): {"items": [{"key", "id", "unit", "verdict", "label", "confidence", "document", "page", "own_or_quoted", "french", "source", "relation", "note"}]}. Copy French words exactly. Reply with one line: counts of keep, relabel, reject; counts by relation.
