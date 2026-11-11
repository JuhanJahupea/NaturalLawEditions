# Screen: does Pufendorf answer the same question as Burlamaqui's section, and does Burlamaqui answer it differently?

Input JSON (path given): list of items. Each item = one section of Burlamaqui, Principes du droit naturel (Genève 1747), with candidate sections of Pufendorf, Le droit de la nature et des gens, in Barbeyrac's French translation (Amsterdam 1734):
{"burlamaqui_id": "P1.5.8", "burlamaqui_margin": "...", "burlamaqui_text": "...", "burlamaqui_notes": "...", "candidates": [{"source_id": "Liv. II ch. III § 23", "text": "...", "reuse": ["close paraphrase", ...]}, ...]}
The Pufendorf text is a careful transcription of Pufendorf's own text in Barbeyrac's translation (Barbeyrac's notes are left out). "reuse" lists the reuse labels already found between the two sections, if any; an empty list means the candidate was retrieved by word similarity only. Several candidates per item may be irrelevant.

Burlamaqui taught from Pufendorf's work in Barbeyrac's translation and often takes up his questions, sometimes following Barbeyrac's notes against Pufendorf. The point of this screen is to find places where Pufendorf gives a definite answer to a question and Burlamaqui, treating the same question, gives a significantly different answer: a different rule, a different ground for the rule, an added or removed condition that changes the practical result, an opposite conclusion, or a refusal to decide what Pufendorf decides. Burlamaqui's explicit criticism of Pufendorf counts, but only where the substance of the answers differs.

For each item:
1. State the question Burlamaqui's section answers (one short phrase, in English).
2. For each candidate decide:
   - same_question: true only if Pufendorf's section answers that question or an immediate part of it. Same topic is not the same question.
   - relation (only when same_question): "follows" (same answer, same ground; wording may differ), "diverges" (a different answer, a different ground, or a condition that changes the result), "partly" (same answer, but a qualification, exception or ground is added or dropped that an intellectual historian would note).
   - source_answer, burlamaqui_answer: one sentence each, in English, only when relation is "diverges" or "partly".
   - source_passage: the exact French words of Pufendorf's answer (copied from text), only for "diverges" or "partly".
   - burlamaqui_passage: the exact French words of Burlamaqui's answer (copied from burlamaqui_text or burlamaqui_notes), only for "diverges" or "partly".
   - confidence 0–1.
Do not infer divergence from silence alone: Burlamaqui omitting a point Pufendorf makes is "partly" only if the omission changes the rule. Do not count style, length, examples or authorities cited. Be sceptical: expect "diverges" in well under a fifth of the items.

Output: write with python3 a JSON file (path given): {"items":[{"burlamaqui_id","question","pairs":[{"source_id","same_question","relation","source_answer","burlamaqui_answer","source_passage","burlamaqui_passage","confidence"}]}]}
Copy passages exactly. Work through every item and every candidate. Keep helper files in your own scratch folder (given). Reply with one line: number of items; counts of follows / partly / diverges.
