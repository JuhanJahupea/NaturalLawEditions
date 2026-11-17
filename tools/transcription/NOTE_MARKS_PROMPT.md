# Footnote calls and notes as printed (Vattel, Le droit des gens, Neuchâtel 1773)

Input JSON (path given): a list of items. Each item is one section (unit) with a task, the footnote calls the edition found in its text (mark, printed page, words before the call), its notes (index, mark, opening words), and the scans of its pages (MDZ images, 1600 px wide).

Method: download each scan with curl into your scratch folder; python3 with PIL is available. Notes are in small type at the foot of the page: crop the lower part at full width and enlarge it (2x). Crop around a call to read its mark. Read marks exactly as printed: (a), (b), (*), (**), [a] …

Tasks:
- "marks": the edition's call mark and note mark disagree (e.g. call (a), note (*)). Say what the print has, for every call and every note of the section: the printed mark of each call (in text order) and of each note (in order).
- Other tasks are written out in the item: answer them from the scans. Where a note or call is missing from the edition, transcribe it diplomatically (long s as ſ, & as printed, italics as <i>…</i>, line breaks as spaces) and give the words before the call, copied from the item's text where the call stands, so that it can be placed.

Output: write with python3 a JSON file (path given): {"items": [{"unit", "printed_calls": [{"mark", "context"}], "printed_notes": [{"index", "mark", "start"}], "answer": "one or two sentences", "missing": [{"kind": "note" | "call", "mark", "page", "text", "context"}], "certain": true|false}]}
"context" for a call: the last 40 characters before it, copied exactly from the item's call contexts or text. Work through every item. Keep helper files in your own scratch folder (given). Reply with one line per item.
