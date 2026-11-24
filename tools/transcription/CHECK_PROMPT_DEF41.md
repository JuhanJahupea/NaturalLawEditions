# Second reading of the DEF41 transcription (Vattel, *Défense du système leibnitien*, 1741)

A first reader transcribed each page of the book into `<WORK>/tr/DEF41/s<NNNN>.json` by the rules in `<TOOLS>/TRANSCRIBE_PROMPT_DEF41.md` (read them first). You check given pages against their images and correct the files.

For each scan in your list:
1. Read the image `<WORK>/scans/img/DEF41/p<NNNN>.jpg` with the Read tool. For small or dark footnotes, or a dark passage of the main text, crop: `python3 -I <TOOLS>/crop2.py DEF41 <scan> <x0> <y0> <x1> <y1>` (fractions of the page image); read the crop. Up to four crops per page.
2. Read the transcription file. Compare it with the image line by line: head, page, every line of body (words, letters, long s ſ against round s, accents, punctuation and its spacing, line-end hyphens, italics <i>…</i>, the markers <<…>>), every note, catch, sig.
3. Correct what differs from the print. Keep the rules: the print as it stands, misprints included; do not modernize, do not complete from the sense. Where the print is truly unreadable, keep or write [?] / [...] / [word?]. Keep the file's fields and JSON form; notes as {"mark","text"} objects. Write the corrected file over the old one with python3 (json.dump, ensure_ascii=False).
4. Log every change: {"scan", "zone" (head/page/body/notes/catch/sig), "line" (1-based line of body or note index), "old", "new", "kind"}. kind: "word" (a wrong or missing word or letters in a word), "longs" (ſ/s or f/ſ), "accent", "punct", "italic" (an italic boundary), "hyphen" (line-end hyphen or line break), "marker", "other". Also record per scan the number of words on the page ("words", an estimate is enough).

Write the log with python3 to `<WORK>/tr/DEF41_check/<batch>.json` as {"batch", "pages": [{"scan", "words", "changes": [...]}]}. Your batch name and scans are given. Reply with ONE line: "<batch>: <n> pages, <n> changes (word <n>, longs <n>, accent <n>, punct <n>, italic <n>, other <n>)".
