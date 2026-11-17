# Check a page transcription against the printed page (Wolff, Jus gentium, Halle 1749)

Input JSON (path given): a list of pages. Each has the transcription made from one copy (Google Books scan) — "head" (running head), "margin" (marginal summaries with the § they stand beside), "body" (main text; a line "<<§ n>>" marks where § n starts and is not printed text; line breaks as printed; italics as <i>…</i>; long s as ſ) and "catch" (catchword) — and "image": the same printed page in another copy of the same edition (MDZ, Munich).

Method: download the image with curl into your scratch folder; python3 with PIL is available. Crop the page into strips of five to eight lines at full width and enlarge them (2x) so that every letter is legible. Read the printed page line by line against the transcription. First confirm that the image shows the same page (same first and last words); if not, say so and skip the page.

Record every difference in the words of the body, the margin and the head:
- type: "letter" (a word misread: a wrong, missing or extra letter, long s/f/round s confusion, a wrong accent or ligature), "word" (a word missing or added), "punct" (punctuation missing, added or different), "italic" (italic and roman confused), "number" (a § number or a reference number wrong), "line" (a line missing, repeated or out of order).
- print: the words as printed; transcription: the words as transcribed; where: body, margin or head.
Do not record: the <<§ n>> marker lines, line-end hyphenation already kept, spaces around punctuation, capital ſ forms the font does not distinguish, or a difference you cannot settle at the enlargement; list those under "unsure".

Count the words of each page (body, margin, head; a word is a run of letters) so that an error rate can be computed.

Output: write with python3 a JSON file (path given): {"pages": [{"printed", "scan", "same_page": true|false, "words": n, "errors": [{"type", "where", "print", "transcription"}], "unsure": ["..."]}]}
Work through every page. Keep helper files in your own scratch folder (given). Reply with one line: pages, words, errors by type.
