# Which call does each footnote answer? (Vattel, Le droit des gens, Neuchâtel 1773)

Input JSON (path given): a list of clusters. A cluster is a run of consecutive sections (units) that share printed pages, with the scans of those pages:
{"cluster": 3, "units": [{"id": "IV.92", "calls": [{"mark": "a", "page": "270", "scan": 278, "context": "…words before the call (a"}], "notes": [{"index": 0, "mark": "(a)", "text": "opening words of the note"}], "pages": [...]}, ...],
 "scans": [{"vol": "T2", "scan": 278, "printed": "270", "image": "https://api.digitale-sammlungen.de/iiif/image/v2/…/full/1400,/0/default.jpg"}]}
"calls" are the footnote call marks found in the section's text, with the printed page they stand on and the words before them. "notes" are the footnotes the edition attaches to the section now; a note with mark "cont" continues the note before it from the previous page. The edition sometimes attaches a note to the wrong section when two sections share a page. Your job is to say, from the scans, which call each note answers.

Method: download each scan with curl into your scratch folder (python3 with PIL is available to crop; the notes are in small type at the foot of the page, so crop the lower part of the page at full width and enlarge it). For each page, read the footnotes printed at its foot (mark and opening words) and the call marks in its text. Footnotes on a page answer the calls on that same page, in order. A note that runs over to the next page continues there without a mark.

For every note of every unit in the cluster give:
- unit, index (as in the input), mark;
- page: the printed page number at whose foot the note starts;
- call_unit: the id of the section whose call this note answers; call_mark: that call's mark as printed; call_context: the words before the call, copied from the "context" of that call in the input;
- certain: true or false;
- remark: one short sentence if anything is odd (a call with no note, a note with no call, a mark misread, a note that belongs to a section outside the cluster).
For "cont" notes give the page where the continuation stands and the same call as the note it continues.

Output: write with python3 a JSON file (path given): {"notes": [{"cluster", "unit", "index", "mark", "page", "call_unit", "call_mark", "call_context", "certain", "remark"}], "calls_without_note": [{"unit", "mark", "context"}]}
Work through every cluster, every note and every call. Keep helper files in your own scratch folder (given). Reply with one line: clusters, notes, notes whose call is in another unit than the one the edition gives.
