# Check: does the author attribute the reused passage to its source?

Input JSON (path given): list of units of an eighteenth-century treatise (Vattel, Le droit des gens, 1773, or Burlamaqui, Principes du droit naturel, 1747), each with its margin, main text, footnotes (part n0, n1 …) and some reuse rows:
{"unit", "edition", "margin", "text", "notes": [{"part", "mark", "text"}], "rows": [{"id", "source", "by", "locus", "label", "passage_part", "passage", "source_passage", "claimed_form", "claimed_cue", "cue_part", "first_reason"}]}
"passage" is the stretch of the unit that reuses the source; "passage_part" says where it stands (t main text, m margin, n0 … notes). "by" is whose words the source passage are (the source's author, or Barbeyrac's note in his translation of Grotius or Pufendorf). A first reader claimed that the author attributes the passage to the source and named the words that do it ("claimed_cue", in "cue_part"). Check that claim against the unit. Do not trust it.

Attributed means the author names, for this passage, the source's author or work (for Barbeyrac's note: Barbeyrac, or the work and place where the note stands). The name must belong to this passage: in the sentence that holds it, in the sentence or clause that introduces it, in a footnote whose call stands inside the passage or at the end of its sentence (or the footnote that holds the passage), or in a marginal reference beside it. Not attributed: the name stands elsewhere in the unit for another point; the cue names another writer (an ancient author both texts quote, a jurist, Scripture) rather than the source; the source is cited for a different claim; a general "les Auteurs", "on dit", "quelques-uns" with no name nearby. A passage the author rejects ("Grotius prétend …, mais …") is attributed if the source is named for it.

For each row give:
- id;
- verdict: "correct" (the cue, or other words of the unit, name the source for this passage), "wrong" (the passage is not attributed to this source), "unsure" (the call depends on something you cannot settle from the unit: a footnote call you cannot place, a name that could cover the passage or the sentence before it, an indirect designation such as "ce grand homme" or "l'Auteur" far from the name);
- form (if correct): "quotation" (the passage is given as the source's own words) or "reference" (the source is named for the content);
- cue (if correct and the claimed cue is not the best one): the exact words of the unit that name the source, copied character for character; else "";
- reason: one short sentence in English.
Use "unsure" sparingly: only where a careful reader with the page in front of them would still hesitate.

Output: write with python3 a JSON file (path given): {"items": [{"id", "verdict", "form", "cue", "reason"}]}
One item per row. Keep helper files in your own scratch folder (given). Reply with one line: number of rows; correct / wrong / unsure.
