# Judge: reuse of Vattel's *Law of Nations* in American documents, 1762–1776

Input JSON (paths given): {"items": [{"id", "doc", "volume", "char_start", "before", "passage", "candidates": [{"unit", "english_1797"}]}]}

- `passage` is a stretch of an American text, from OCR of an archive.org scan (long s mostly restored as s; some OCR errors remain). `before` is the text just before it, for context (document heading, date, author). `volume` names the book or pamphlet. Several volumes are collected writings (Samuel Adams, John Adams), the journals of the Continental Congress, or the Massachusetts state papers: one volume holds many documents by several hands, and modern editors' notes.
- `candidates` are sections of Vattel's *Le droit des gens* (1758), given in the London English translation of 1797, which revises the first English translation of 1760. Americans read the 1760 English or the French. A quotation from the 1760 text may differ from the 1797 wording in single words.
- Candidates were found by word overlap. Most are false positives.

Task: for each item and each candidate, decide whether the American passage reuses that section of Vattel.

Be sceptical. Shared political vocabulary ("law of nations", "fundamental laws", "constitution", "allegiance", "independent states") is not reuse. The same topic is not reuse. Reuse needs shared wording, or a shared argument in the same order, or an explicit reference to Vattel at this point. Locke, Grotius, Pufendorf, Burlamaqui, Montesquieu and Blackstone say many of the same things: if the passage follows one of them rather than Vattel, it is not a match to Vattel (say so in the reason of a no_match if obvious).

Labels (one per match):
- quotation: Vattel's words given as a quotation (quotation marks, or named as Vattel's);
- verbatim: Vattel's words used without marks for at least a clause;
- close paraphrase;
- loose paraphrase;
- reference: Vattel named or cited for this point, without his words;
- commonplace: shared matter too common to show use of Vattel.

For each match give:
- id; unit;
- passage: exact words copied from `passage` (the reusing stretch only, one continuous stretch; copy the OCR as it stands, errors included);
- vattel: exact words copied from `english_1797` (the reused stretch only, one continuous stretch);
- label; confidence 0–1;
- named: true if the American text names Vattel (in the text or a note) for this stretch;
- document: the American document as far as `volume`, `before` and `passage` show it: author, title or kind, date (e.g. "Samuel Adams, letter to Arthur Lee, 4 Nov. 1771"; "Massachusetts House of Representatives, answer to the Governor's speech, 26 Jan. 1773"). If the passage is an editor's note or a document after 1776, say so;
- quoted_by: if the American text quotes another writer who quotes Vattel (e.g. a Governor's speech quoted in the House's answer), name that writer; else "";
- reason: one sentence in English.

Copy passages exactly, character for character; no paraphrase, no ellipsis. Work through every item and every candidate.

Output: write with python3 a JSON file (path given): {"matches": [{"id", "unit", "passage", "vattel", "label", "confidence", "named", "document", "quoted_by", "reason"}], "no_match": [{"id", "unit", "reason"}]}. Keep helper files in your own scratch folder (given). Reply with one line: number of items, number of matches by label.
