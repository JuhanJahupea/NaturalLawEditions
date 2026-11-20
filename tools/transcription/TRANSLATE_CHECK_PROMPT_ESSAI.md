# Translation check: Vattel, Essai sur le fondement du droit naturel (1747) vs T. J. Hochstrasser's English translation (Liberty Fund, 2008)

Input JSON (path given): list of items, one per section:
{"sid": "II.8", "pairs": [{"k": 0, "fr": "...", "en": "..."}, ...]}
Each pair holds one or two French sentences and the English sentence(s) aligned to them by machine. An empty "en" or "fr" means the aligner found no counterpart. The alignment was made by sentence length and can be off by one sentence; judge the meaning across neighbouring pairs before calling something an omission.

The French is the 1747 print (Le loisir philosophique, Dresde 1747). The English is Hochstrasser's translation (2008), made from the text reprinted in Pradier-Fodéré's edition of Le droit des gens (Paris 1863); where the English has words the 1747 French lacks, it may follow the 1863 text: flag it as an addition and say so in the note. The French transcription keeps 18th-century spelling (loix, prémier, &).

Task: flag only translation problems that matter to an intellectual historian reading Vattel in English. Do not flag style, word order, punctuation, spelling, or normal free rendering.

Flag:
- mistranslation: the English says something the French does not.
- shift: the English weakens, strengthens, narrows or widens a claim (e.g. "doit" rendered "may"; "toujours" dropped; a qualification lost).
- omission: a clause or phrase with content is missing in English.
- addition: the English adds content not in the French.
- terminology: a key term is rendered inconsistently or by a word that changes the concept. Watch especially: droit / loi / règle; droit naturel / loi naturelle / morale; obligation (active / passive), devoir, être tenu, nécessité morale; motif, raison, fondement, principe; utilité / utile, honnêteté / honnête, intérêt, avantage; bien, bien-être, bonheur, félicité, perfection; amour de soi / amour-propre; volonté, supérieur, dépendance, soumission; convenance / disconvenance; essence, nature; vertu, beauté de la vertu.
- false friend: an English word whose 18th-century or modern sense misleads (e.g. "sentiment", "honest", "commerce", "humanity", "constitution", "moral sense").

For every flag give:
- sid, k (pair number)
- fr: the exact French words concerned, copied from "fr" (short, the problem phrase only)
- en: the exact English words concerned, copied from "en" ("" for an omission)
- type: one of mistranslation, shift, omission, addition, terminology, false friend
- severity: 1 (minor but worth knowing), 2 (changes the sense of the sentence), 3 (changes the doctrine or an argument)
- note: one sentence in plain English giving a literal rendering of the French and saying what the English changes.

This translation is known to contain errors: check every pair with care and flag every real problem. Do not invent problems, and do not flag free but faithful rendering.

Output: write with python3 a JSON file (path given): {"flags":[...], "checked":["sid", ...]}. Copy phrases exactly. Work through every item. Keep helper files in your own scratch folder (given). Reply with: number of items, number of flags by type.
