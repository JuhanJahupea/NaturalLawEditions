# Check a page transcription against the printed page (Vattel, Essai sur le fondement du droit naturel, in Le loisir philosophique, 1747)

Input JSON (path given): a list of pages. Each has the transcription made from one copy (Google Books scan of the BCU Lausanne copy) — "head" (running head), "body" (main text; a line "<<§ n>>" marks where § n starts and is not printed text; line breaks as printed; italics as <i>…</i>; long s as ſ; Vattel's quotation marks „ at line starts kept), "notes" (footnotes with their marks) and "catch" (catchword) — and "image": a local file, the same printed page in another copy (Zentralbibliothek Zürich, e-rara), which may be another issue of the same edition.

Method: the image is a local file; python3 with PIL is available. Crop the page into strips of five to eight lines at full width and enlarge them (2x) so that every letter is legible. Read the printed page line by line against the transcription. First confirm that the image shows the same page (same first and last words); if not, say so and skip the page.

Record every difference in the words of the body, the notes and the head:
- type: "letter" (a word misread: a wrong, missing or extra letter, long s/f/round s confusion, a wrong accent or ligature), "word" (a word missing or added), "punct" (punctuation missing, added or different), "italic" (italic and roman confused), "number" (a § number or a reference number wrong), "line" (a line missing, repeated or out of order).
- print: the words as printed; transcription: the words as transcribed; where: body, notes or head. Where the two copies are differently set (another issue), say so in "unsure" and record only clear misreadings.
Do not record: the <<§ n>> marker lines, line-end hyphenation already kept, spaces around punctuation, capital ſ forms the font does not distinguish, or a difference you cannot settle at the enlargement; list those under "unsure".

Count the words of each page (body, notes, head; a word is a run of letters) so that an error rate can be computed.

Output: write with python3 a JSON file (path given): {"pages": [{"printed", "scan", "same_page": true|false, "words": n, "errors": [{"type", "where", "print", "transcription"}], "unsure": ["..."]}]}
Work through every page. Keep helper files in your own scratch folder (given). Reply with one line: pages, words, errors by type.
