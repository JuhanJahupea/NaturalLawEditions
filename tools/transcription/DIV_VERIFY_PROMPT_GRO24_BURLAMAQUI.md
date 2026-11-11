# Verify and write up: where Burlamaqui answers Grotius's question differently

Input JSON (path given): list of items. Each item = one flagged pair:
{"burlamaqui_sec": "P1.5.8", "burlamaqui_margin": "...", "burlamaqui_text": "...", "burlamaqui_notes": "...", "source_ref": "Liv. II ch. XVI § 25", "source_text": "...", "barbeyrac_notes": "...", "screen": {"question": "...", "relation": "diverges" | "partly", "source_answer": "...", "burlamaqui_answer": "...", "source_passage": "...", "burlamaqui_passage": "..."}}
source_text is Grotius's whole section in Barbeyrac's French translation (Amsterdam 1724), from a careful transcription. barbeyrac_notes are Barbeyrac's notes to that section, for context only: the layer compares Burlamaqui with Grotius, not with Barbeyrac. The Burlamaqui text is Principes du droit naturel (Genève 1747). The "screen" is a first-pass judgement by another reader. Check it against the texts. Do not trust it.

The layer being built marks the places where Grotius gives a definite answer to a question and Burlamaqui, treating the same question, gives a significantly different answer: a different rule, a different ground for the rule, a condition that changes the practical result, an opposite conclusion, or a refusal to decide what Grotius decides.

For each item decide:
- verdict: "keep" if Grotius's section answers the question Burlamaqui's section answers and Burlamaqui's answer differs in substance; "reject" if the two do not answer the same question, or the difference is only wording, length, examples, authorities or emphasis.
- relation (if keep): "diverges" (different rule, ground or conclusion) or "partly" (same rule, but a qualification, exception or ground is added or dropped that changes what the rule does).
- severity (if keep): 3 = opposite or incompatible answers; 2 = a different ground or a condition that changes cases; 1 = a qualification worth a footnote.
- comment (if keep): two to four short sentences in English for a footnote in a scholarly edition. First sentence: what Grotius holds, citing him in the form "Grotius, DGP II.16.25" (book in roman numerals, chapter and section in arabic). Second: what Burlamaqui holds instead. Third (optional): the exact point of difference; say so if Burlamaqui follows Barbeyrac's note against Grotius. Plain declarative sentences. No transition words, no em-dashes, no rhetorical questions, no "notably", no "interestingly". Name the doctrine, not the reader's feelings.
- source_passage: the exact French words of Grotius's answer, copied from source_text (one clause or sentence).
- burlamaqui_passage: the exact French words of Burlamaqui's answer, copied from burlamaqui_text or burlamaqui_notes (one clause or sentence).
- confidence 0–1.

Output: write with python3 a JSON file (path given): {"items":[{"burlamaqui_sec","source_ref","verdict","relation","severity","comment","source_passage","burlamaqui_passage","confidence","reject_reason"}]}
Copy passages exactly. Work through every item. Keep helper files in your own scratch folder (given). Reply with two lines: number of items; kept by relation and rejected.
