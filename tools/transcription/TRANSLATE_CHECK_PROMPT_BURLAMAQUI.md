# Translation check: Burlamaqui, Principes du droit naturel (Genève 1747) vs Thomas Nugent's English translation (1748; 2nd ed. 1763, as printed in the Liberty Fund edition, 2006)

Input JSON (path given): list of items, one per section:
{"sid": "II.8", "pairs": [{"k": 0, "fr": "...", "en": "..."}, ...]}
Each pair holds one or two French sentences and the English sentence(s) aligned to them by machine. An empty "en" or "fr" means the aligner found no counterpart. The alignment was made by sentence length and can be off by one sentence; judge the meaning across neighbouring pairs before calling something an omission.

The French is the 1747 Geneva text. The English is Nugent's translation, made from the 1747 edition. The French transcription keeps 18th-century spelling (loix, prémier, &).

Task: flag only translation problems that matter to an intellectual historian reading Burlamaqui in English. Do not flag style, word order, punctuation, spelling, or normal free rendering.

Flag:
- mistranslation: the English says something the French does not.
- shift: the English weakens, strengthens, narrows or widens a claim (e.g. "doit" rendered "may"; "toujours" dropped; a qualification lost).
- omission: a clause or phrase with content is missing in English.
- addition: the English adds content not in the French.
- terminology: a key term is rendered inconsistently or by a word that changes the concept. Watch especially: droit / loi / règle; droit naturel / loi naturelle / droit des gens; obligation (interne / externe), devoir; supérieur, souveraineté, empire, autorité, pouvoir; volonté, entendement, raison, instinct, sentiment (moral); bonheur, félicité, perfection; amour de soi / amour-propre; sociabilité; imputation, imputer; moralité, actions humaines; état (naturel / accessoire); liberté; conscience; approbation; principe, fondement.
- false friend: an English word whose 18th-century or modern sense misleads (e.g. "sentiment", "honest", "commerce", "humanity", "constitution", "moral sense").

For every flag give:
- sid, k (pair number)
- fr: the exact French words concerned, copied from "fr" (short, the problem phrase only)
- en: the exact English words concerned, copied from "en" ("" for an omission)
- type: one of mistranslation, shift, omission, addition, terminology, false friend
- severity: 1 (minor but worth knowing), 2 (changes the sense of the sentence), 3 (changes the doctrine or an argument)
- note: one sentence in plain English giving a literal rendering of the French and saying what the English changes.

Most sections have no flag. Expect on average under one flag per section. Do not invent problems.

Output: write with python3 a JSON file (path given): {"flags":[...], "checked":["sid", ...]}. Copy phrases exactly. Work through every item. Keep helper files in your own scratch folder (given). Reply with: number of items, number of flags by type.
