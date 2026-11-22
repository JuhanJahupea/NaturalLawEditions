# Verify and write up: where Vattel's Essai answers a source's question differently

Input JSON (path given): a list of flagged pairs. Each item:
{"vattel_sec": "E.13", "vattel_margin", "vattel_text", "vattel_notes", "source": "PPU1", "source_ref": "§ 118", "source_margin", "source_text", "source_notes", "screen": {"question", "relation", "source_answer", "vattel_answer", "source_passage", "vattel_passage"}}

The Vattel text is the *Essai sur le fondement du droit naturel* (Dresde 1747). `source_text` is the whole source section (cut at 15000 characters); `source_notes` are its notes, each marked author or Barbeyrac. Sources: `PPU1` Wolff, *Philosophia practica universalis* I (1738); `TN1` Wolff, *Theologia naturalis* I (1739); `LOG40` Wolff, *Discursus praeliminaris* (1740); `PUF34` Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac (1734); `DEV56` Pufendorf, *Les devoirs de l'homme et du citoyen*, trad. Barbeyrac (1756), whose loci "Jugement d'un anonyme § n" are Leibniz's *Jugement* and "Réflexions du traducteur § n" Barbeyrac's reply; `GRO24` Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac (1724); `BUR47` Burlamaqui, *Principes du droit naturel* (1747). Barbeyrac's notes are part of the source here: Vattel argues with Barbeyrac.

The "screen" is a first reader's judgement. Check it against the texts. Do not trust it.

## What the layer records

A divergence is a place where a source offered Vattel an answer to the question his section treats, so that he could have used it (and sometimes did use part of it), and he chose to make a different or opposite point: a different rule, a different ground for the rule, a condition that changes the result, an opposite conclusion, or a refusal to decide what the source decides. It is not a list of counter-arguments. An open rebuttal counts where the two answers to the question differ in substance. The same answer in other words, a different topic, an omission that changes nothing, or a difference of style, examples or authorities does not count.

## For each item decide

- `verdict`: `keep` if the source section answers the question Vattel's section answers and Vattel's answer differs in substance; `reject` otherwise.
- `relation` (if keep): `diverges` (different rule, ground or conclusion) or `partly` (same rule, but a qualification, exception or ground added or dropped that changes what the rule does).
- `severity` (if keep): 3 opposite or incompatible answers; 2 a different ground or a condition that changes cases; 1 a qualification worth a footnote.
- `question` (if keep): the question both answer, one short phrase in English.
- `comment` (if keep): two to four short sentences in English for a footnote in a scholarly edition. First: what the source holds, cited in one of these forms: "Wolff, PPU I § 118", "Wolff, TN I § 950", "Wolff, Disc. prael. § 145", "Pufendorf, DNG I.6.5", "Barbeyrac, DNG I.6.5 n. 4", "Pufendorf, Devoirs I.2.3", "Leibniz, Jugement § 5", "Barbeyrac, Réflexions § 16", "Grotius, DGP I.1.10", "Grotius, DGP Prol. 17", "Barbeyrac, DGP I.1.10 n. 4", "Burlamaqui, Principes I.6.12". Second: what Vattel holds instead. Third (optional): the exact point of difference, and whether Vattel used part of the source. Plain declarative sentences. No transition words, no em-dashes, no rhetorical questions, no "notably", no "interestingly".
- `source_passage`: the exact words of the source's answer, copied from `source_text` or from one note of `source_notes` (the note's words only, without its bracketed mark), one clause or sentence.
- `vattel_passage`: the exact words of Vattel's answer, copied from `vattel_text` or `vattel_notes`, one clause or sentence.
- `confidence` 0–1.
- `reject_reason` (if reject): one sentence.

## Output

Write with python3 a JSON file (path given): `{"items":[{"vattel_sec","source","source_ref","verdict","relation","severity","question","comment","source_passage","vattel_passage","confidence","reject_reason"}]}`. Check that each passage is an exact substring of its text before writing. Work through every item. Keep helper files in your scratch folder (given). Reply with two lines: number of items; kept by relation and rejected.
