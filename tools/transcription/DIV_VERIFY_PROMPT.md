# Verify and write up: where Vattel answers Grotius's question differently

Input JSON (path given): list of items. Each item = one flagged pair:
{"vattel_sec": "II.8", "vattel_margin": "...", "vattel_text": "...", "vattel_notes": "...", "grotius_ref": "Liv. II ch. XVI § 25", "grotius_text": "...", "barbeyrac_notes": "...", "screen": {"question": "...", "relation": "diverges" | "partly", "grotius_answer": "...", "vattel_answer": "...", "grotius_passage": "...", "vattel_passage": "..."}}
grotius_text is Grotius's whole section in Barbeyrac's French translation (Amsterdam 1724), from a careful transcription. barbeyrac_notes are Barbeyrac's notes to that section, for context only: the layer compares Vattel with Grotius, not with Barbeyrac. The "screen" is a first-pass judgement by another reader. Check it against the texts. Do not trust it.

The layer being built marks the places where Grotius gives a definite answer to a question and Vattel, treating the same question, gives a significantly different answer: a different rule, a different ground for the rule, a condition that changes the practical result, an opposite conclusion, or a refusal to decide what Grotius decides.

For each item decide:
- verdict: "keep" if Grotius's section answers the question Vattel's section answers and Vattel's answer differs in substance; "reject" if the two do not answer the same question, or the difference is only wording, length, examples, authorities or emphasis.
- relation (if keep): "diverges" (different rule, ground or conclusion) or "partly" (same rule, but a qualification, exception or ground is added or dropped that changes what the rule does).
- severity (if keep): 3 = opposite or incompatible answers; 2 = a different ground or a condition that changes cases; 1 = a qualification worth a footnote.
- comment (if keep): two to four short sentences in English for a footnote in a scholarly edition. First sentence: what Grotius holds, citing him in the form "Grotius, DGP II.16.25" (book, chapter and section in arabic numerals). Second: what Vattel holds instead. Third (optional): the exact point of difference; say so if Vattel follows Barbeyrac's note against Grotius. Plain declarative sentences. No transition words, no em-dashes, no rhetorical questions, no "notably", no "interestingly". Name the doctrine, not the reader's feelings.
- grotius_passage: the exact French words of Grotius's answer, copied from grotius_text (one clause or sentence).
- vattel_passage: the exact French words of Vattel's answer, copied from vattel_text or vattel_notes (one clause or sentence).
- confidence 0–1.

Output: write with python3 a JSON file (path given): {"items":[{"vattel_sec","grotius_ref","verdict","relation","severity","comment","grotius_passage","vattel_passage","confidence","reject_reason"}]}
Copy passages exactly. Work through every item. Keep helper files in your own scratch folder (given). Reply with two lines: number of items; kept by relation and rejected.
