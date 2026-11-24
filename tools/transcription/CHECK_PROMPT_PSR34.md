# Second reading of the PSR34 transcription (Wolff, *Psychologia rationalis*, 1734)

A first reader transcribed each page into `<WORK>/tr/PSR34/s<NNNN>.json` by the rules in `<TOOLS>/TRANSCRIBE_PROMPT_PSR34.md` (read them first). You check given pages against their images and correct the files.

For each scan in your list:
1. Read the image `<WORK>/scans/img/PSR34/p<NNNN>.jpg` with the Read tool. The scans show through from the other side and are often blurred: crop where you need it, `python3 -I <TOOLS>/crop2.py PSR34 <scan> <x0> <y0> <x1> <y1>` (fractions of the page image), and read the crop. Up to four crops per page.
2. Read the transcription file. Compare it with the image line by line: head, page, every line of body (words, letters, long s ſ against round s, æ/œ, accents, punctuation, line-end hyphens, italics <i>…</i>, the markers <<§ n>>, <<NOTA>>, <<SECTIO n>>, <<CAPUT n>>), every marginal summary, catch, sig. The <<NOTA>> marker belongs where the smaller type begins.
3. Correct what differs from the print. Keep the rules: the print as it stands, misprints included; do not modernize, do not complete from the sense or from your memory of the text. Where the print is truly unreadable, keep or write [?] / [...] / [word?]. The catchword stands only in "catch", never as the last line of body. Keep the file's fields and JSON form. Write the corrected file over the old one with python3 (json.dump, ensure_ascii=False).
4. Log every change: {"scan", "zone" (head/page/body/margin/catch/sig), "line" (1-based line of body, or index of the margin entry), "old", "new", "kind"}. kind: "word" (a wrong or missing word or letters in a word), "longs" (ſ/s), "accent", "punct", "italic" (an italic boundary), "hyphen" (line-end hyphen or line break), "marker", "other". Also record per scan the number of words on the page ("words", an estimate is enough).

Write the log with python3 to `<WORK>/tr/PSR34_check/<batch>.json` as {"batch", "pages": [{"scan", "words", "changes": [...]}]}. Your batch name and scans are given. Reply with ONE line: "<batch>: <n> pages, <n> changes (word <n>, longs <n>, accent <n>, punct <n>, italic <n>, marker <n>, other <n>)".
