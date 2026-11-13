# Does the author attribute the reused passage to its source?

Input JSON (path given): list of units. Each unit is one section of an eighteenth-century treatise (Vattel, Le droit des gens, 1773, or Burlamaqui, Principes du droit naturel, 1747), with its margin, main text and footnotes, and the reuse rows found in it:
{"unit": "II.45", "margin": "...", "text": "...", "notes": [{"part": "n0", "mark": "(a)", "text": "..."}],
 "rows": [{"key": 17, "source": "Grotius, Le droit de la guerre et de la paix, trad. Barbeyrac (1724)", "by": "Grotius" | "Barbeyrac's note", "label": "close paraphrase", "part": "t" | "n0" | "m", "passage": "...", "source_passage": "..."}]}
"passage" is the stretch of the unit that reuses the source; "part" says where it stands (t main text, m margin, n0, n1 … the notes in order). "by" says whose words the source passage are: the source's author, or the translator's note (Barbeyrac's notes to Grotius or Pufendorf).

Task: for each row decide whether the unit's author attributes this passage to its source. Attributed means the author names, for this passage, the source's author or the source's work (for a translator's note: the translator, or the work and place where the note stands). The name must belong to this passage:
- in the sentence that holds the passage, or in the sentence or clause that introduces it ("Voici comment Grotius raisonne", "M. Wolf dit");
- or in a footnote whose call stands inside the passage or at the end of its sentence, or in the footnote that holds the passage;
- or in a marginal reference beside the passage.
Not attributed:
- the name stands elsewhere in the unit, for another point;
- the author names another writer (an ancient author both texts quote, a jurist, Scripture) and not the source;
- the author cites the source only for a fact or a different claim, not for this passage's content;
- a general acknowledgement ("les Auteurs", "on dit", "quelques-uns") with no name.
A passage the author rejects ("Grotius prétend …, mais …") is attributed if the source is named for it.

For each row give:
- key;
- attributed: true or false;
- form (only if attributed): "quotation" if the passage is given as the source's own words (quotation marks, italics with the name, "ce sont ses termes", "dit-il", a translation offered as his words); "reference" if the source is named for the content but the words are the author's own;
- cue (only if attributed): the exact words of the unit that name the source, copied character for character from text, margin or notes (a name, a title, or a reference such as "Grotius, Liv. II chap. II. § 6.");
- cue_part: where the cue stands (t, m, n0, n1 …);
- confidence 0–1; reason: one short sentence in English.

Output: write with python3 a JSON file (path given): {"items": [{"key", "attributed", "form", "cue", "cue_part", "confidence", "reason"}]}
One item per row, every row. Copy cues exactly. Keep helper files in your own scratch folder (given). Reply with one line: number of rows; attributed (quotation / reference); not attributed.
