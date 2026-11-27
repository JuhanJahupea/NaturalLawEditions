# Verify and write up: where Vattel's *Défense* (1741) departs from Leibniz or Wolff

Input JSON (path given): `items`, each {`vattel_sec` (D.n = paragraph n of the *Défense*), `vattel_text` (italics _…_), `vattel_notes`, `source` (`THEO` Leibniz, *Théodicée*, in Janet's modern spelling; `PSR34` Wolff, *Psychologia rationalis*, Latin, its note after "[Nota]"), `source_key`, `source_ref`, `source_text` (the whole section), `screen` (a first reader's judgement: question, relation, answers, passages, confidence)}.

Vattel wrote the *Défense* to defend Leibniz and Wolff against Crousaz. Check the screen against the texts. Do not trust it.

## What the layer records

A divergence is a place where the source answers the question Vattel's paragraph treats, and Vattel, while defending the system, gives a different answer: a different rule or ground, a condition or qualification that changes what the doctrine does, a softer or stronger claim (certain for probable, demonstrated for hypothetical), a reading the source does not support, or a refusal to hold what the source holds. Not a divergence: the same doctrine in other words or at another level of detail; Vattel applying it to a case the source does not treat; a paraphrase that is loose but faithful; a difference of style, example or emphasis.

## For each item decide

- `verdict`: `keep` or `reject`.
- If keep:
  - `relation`: `diverges` or `partly`.
  - `severity`: 3 for opposite answers; 2 for a different ground or a changed scope; 1 for a qualification worth a footnote.
  - `question`: the question, in one short English phrase.
  - `comment`: two to four short sentences in English, for a footnote. First, what the source holds, cited as "Leibniz, Théod. § 25", "Leibniz, Théod., Discours § 44", "Leibniz, Théod., Abrégé, obj. 4" or "Wolff, Psych. rat. § 632". Second, what Vattel holds instead. Third, optional: the exact point of difference. Write plain declarative sentences: no transition words, no em-dashes, no rhetorical questions.
  - `source_passage`: exact words copied from `source_text`, one clause or sentence.
  - `vattel_passage`: exact words copied from `vattel_text` or a note, one clause or sentence.
  - `confidence`: 0–1.
- If reject: `reject_reason`, one sentence.

## Output

Write the result with python3 to the path given, as `{"items":[{"vattel_sec","source","source_key","source_ref","verdict","relation","severity","question","comment","source_passage","vattel_passage","confidence","reject_reason"}]}`. Before writing, check every passage as an exact substring. Keep helper files in your scratch folder (given). Reply with one line: items; keep by relation; rejected.
