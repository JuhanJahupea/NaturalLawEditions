# Reuse of two more Wolff texts in Vattel's *Essai sur le fondement du droit naturel* (1747)

Vattel's *Essai* (printed in *Le loisir philosophique*, 1747) argues that obligation is the connection of a motive with an action and that its first principle is our own good. Its reuse tables already cover Wolff's *Philosophia practica universalis* I, Pufendorf, Grotius (with Barbeyrac's notes) and Burlamaqui. You read some of its sections with two further Wolff texts and list every passage where Vattel takes something from them.

## Input (JSON, path given)

`hint`: where to start. `units`: sections of the Essai: `unit` (E.13 = § 13), `text`, `notes` (Vattel's footnotes).

## Sources (read with python3; never load a whole file into your reply)

- `TN1`: Wolff, *Theologia naturalis*, pars prior (1739), §§ 948–1006: the end of cap. V, cap. VI *De jure Dei in creaturas* (God's right over creatures, God as lord and legislator, obligation from his will, divine law, rewards and punishments), the start of cap. VII. Vattel cites "Theol. Nat. P. I. §. 950." `<WORK>/srcp/TN1.json`.
- `LOG40`: Wolff, *Discursus praeliminaris de philosophia in genere* (in *Philosophia rationalis sive Logica*, 1740), §§ 1–171: historical, philosophical and mathematical knowledge (cap. I), philosophy defined (cap. II), its parts, among them practical philosophy, ethics, politics and natural law (cap. III), method (cap. IV), style (cap. V), freedom of philosophising (cap. VI). `<WORK>/srcp/LOG40.json`.
- Both: `pages` [{`id` e.g. `TN1.pdf931`, `page` (printed), `text` (long s as s, line-end hyphens joined), `starts` [[offset, §]], `carried` (the § running on from the page before), `margin` (Wolff's marginal summaries)}]; `first_page_of` {"950": "TN1.pdf…"}. Read the § you test in full, with the § before and after.

## What counts

Vattel takes wording, or a specific definition, argument, example or order of points, from the source passage; or translates it; or cites it; or takes it up to reject it. A doctrine every Wolffian states is not enough unless the wording or the order is shared. Vattel's French often translates the Latin: say so. Say also where a passage of these two texts is the same as one of the *Philosophia practica universalis* (Wolff repeats himself); the row stands all the same.

## Each row

- `unit`; `passage`: Vattel's words, copied exactly from the section's `text` or one of its `notes` (copy, never retype). The reused stretch: a clause to a few sentences.
- `text`: `TN1` or `LOG40`; `page`: the page id; `source_passage`: copied exactly from that page's `text` or one of its `margin` entries.
- `french`: a plain French rendering of `source_passage`.
- `label`: `translation`, `verbatim`, `close paraphrase`, `loose paraphrase`, `shared argument`, `citation`, `open disagreement`. `confidence`: 0.3–1 (0.5 or more: a match you would defend).
- `named`: when Vattel names the source for this passage in the same sentence or its note: {"form": "reference", "cue": Vattel's words that name it, copied exactly}; otherwise omit.
- `reason`: one sentence.

## Comparison (batch with §§ 1–8 only)

Also write `compare`: a short plain account (at most 250 words, plain sentences, facts only) of how the *Discursus praeliminaris* stands to Essai §§ 1–8: what Vattel's opening takes from it (definitions, divisions, method), in which order, what it leaves out, and what Vattel has that the Discursus does not. Cite § numbers on both sides.

## Output

Write with python3 a JSON file (path given): `{"rows": [...], "sections": [{"unit", "searched": "one line"}], "compare": "..."}` (`compare` only in the first batch). Check that every `passage` occurs in its section (text or a note) and every `source_passage` on its page, as exact substrings, before writing. Keep helper files in your scratch folder (given). Reply with one line per section: rows by source.
