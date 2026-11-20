# Reuse in Vattel's *Essai sur le fondement du droit naturel* (1747)

Vattel's *Essai sur le fondement du droit naturel, et sur le premier principe de l'obligation* (written about 1742–1746, printed in *Le loisir philosophique*, Dresde 1747) argues that obligation is the connection of a motive with an action, and that the first principle of obligation is our own good (perfection, happiness). He follows Wolff and argues against Barbeyrac. You read a few of its sections with its sources and list every passage where Vattel takes something from them.

## Input (JSON, path given)

`units`: sections of the Essai. Each has `unit` (E.13 = § 13), `text`, `notes` (Vattel's footnotes: numbered remarks and lettered references) and `candidates`: for each French source, the 8 pages nearest the section by shared vocabulary (a start, not a limit).

## Sources (read with python3; never load a whole file into your reply)

- `PPU1`: Wolff, *Philosophia practica universalis*, pars prior (1738), §§ 1–415 (Prolegomena; cap. I on human actions; cap. II on obligation and natural law, from § 115; cap. III on God as author of natural law, rewards and punishments, from § 271; cap. IV on virtue, vice and happiness). `<WORK>/srcp/PPU1.json`: `pages` [{`id` e.g. `PPU1.pdf142`, `page` (printed), `text`, `starts` [[offset, §]], `carried`, `margin`}]; `first_page_of` {"118": "PPU1.pdf..."}. An index of Wolff's marginal summaries, one per line (§, page id, printed page, summary): `<WORK>/srcp/PPU1_margins.tsv`. Vattel cites PPU pars I §§ 118, 119, 132 (note) and 137. Wolff is his main source: expect definitions and arguments translated from the Latin.
- `DEV56`: Pufendorf, *Les devoirs de l'homme et du citoyen*, trad. Barbeyrac (1756 printing; Vattel used the 4th edition, Amsterdam 1718, pp. 441–476). Tome II holds Leibniz's *Jugement d'un anonyme* (loci "Jugement d'un anonyme § n") and Barbeyrac's *Réflexions du traducteur* (loci "Réflexions du traducteur § n"). Vattel quotes both at length in §§ 30–41. `<WORK>/corpus/DEV56.json`.
- `PUF34`: Pufendorf, *Le droit de la nature et des gens*, trad. Barbeyrac (1734), with Barbeyrac's notes. Vattel cites I.1.21 and I.6.5 note 4. `<WORK>/corpus/PUF34.json`.
- `GRO24`: Grotius, *Le droit de la guerre et de la paix*, trad. Barbeyrac (1724), with Barbeyrac's notes. Vattel cites I.1.10 and Barbeyrac's note 4 to it. `<WORK>/corpus/GRO24.json`.
  - DEV56, PUF34, GRO24 pages: [{`id` e.g. `DEV56T2.p232`, `text`, `spans` [[start, end, locus]], `margin` [{text, locus}], `notes` [{mark, by, text, locus}]}]; `by` "author" marks the author's own notes, other notes are Barbeyrac's.
- `BUR47`: Burlamaqui, *Principes du droit naturel* (Genève 1747), printed the same year; Vattel does not name it. Check whether the two share wording or a specific argument; either may follow the other or a common source. `/home/user/NaturalLawEditions/editions/burlamaqui-1747/text.json`: `units` [{`id` e.g. `P1.6.9`, `text`, `notes` [{mark, text}]}].

## What counts

Vattel takes wording, or a specific definition, argument, example or order of points, from the source passage; or quotes it; or cites it; or takes it up to reject it. A doctrine every writer states is not enough unless the wording is shared. For Wolff, Vattel's French often translates the Latin: say so.

## Each row

- `unit`; `passage`: Vattel's words, copied exactly from the section's `text` or one of its `notes` (copy, never retype: spacing and spelling as in the input). The reused stretch: a clause to a few sentences. A long quotation of Barbeyrac or Leibniz: one row per quoted block.
- `text`: `PPU1`, `DEV56`, `PUF34`, `GRO24` or `BUR47`; `page`: the page id (for BUR47 the unit id); `source_passage`: copied exactly from that page's `text`, one of its `notes` or `margin` entries (BUR47: the unit's `text` or a note).
- `french` (PPU1 only): a plain French rendering of `source_passage`.
- `label`: `quotation` (Vattel quotes the source, marked as a quotation), `translation` (Vattel translates the Latin closely), `verbatim`, `close paraphrase` (same structure, most content words), `loose paraphrase` (same content, other words and structure), `shared argument` (same reasoning, independently worded), `citation` (Vattel names or cites this passage), `open disagreement` (Vattel takes the passage up and rejects it).
- `confidence`: 0.3–1 (0.5 or more: a match you would defend).
- `named`: when Vattel names the source for this passage in the same sentence or its note: {"form": "quotation" or "reference", "cue": Vattel's words that name it, copied exactly, e.g. "dit M. Barbeyrac" or "Wolf. Phil. Pract. univ. p. 1. §. 118."}; otherwise omit.
- `reason`: one sentence.

## Output

Write with python3 a JSON file (path given): `{"rows": [...], "sections": [{"unit", "searched": "one line"}]}`. Check that every `passage` occurs in its section (text or a note) and every `source_passage` on its page, as exact substrings, before writing. Keep helper files in your scratch folder (given). Reply with one line per section: rows by source.
