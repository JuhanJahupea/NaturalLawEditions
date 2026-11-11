# Transcription instructions (Wolff, Jus gentium methodo scientifica pertractatum, Halle 1749, and Institutiones juris naturae et gentium, Halle 1750; Google Books scans)

You are transcribing scanned pages of an 18th-century Latin book. Read each page image with the Read tool and write one JSON file per page. Work only from the image. Never paraphrase, modernize or complete text from memory.

## Diplomatic rules
- Keep original spelling, accents (or their absence), capitalization and punctuation exactly, including spaces before ; : ? ! and inside "( §. 7. )".
- Long s: write ſ wherever the print has a long s (e.g. "ſoldats", "eſt", "auſſi"). Round s stays s.
- Ligatures: write "&" as printed; write æ / œ as printed; ct/st ligatures as plain letters.
- Keep line breaks as "\n" and keep end-of-line hyphens exactly as printed (e.g. "en-\ngager"). Do not join words.
- Italics: wrap in <i>…</i>. Small caps: write as printed letters (no markup).
- Illegible or damaged: [?] for one uncertain character, [...] for lost words. If a reading is a guess, put it as [word?].
- Do not transcribe library stamps or handwriting; note them in "notes_scan".

## Zones (keep them separate)
- head: running head line, verbatim (e.g. "12 LE DROIT DES GENS.").
- page: printed page number as string ("12"), or "" if none.
- margin: list of marginal summaries in order, each {"para": "§. 14.", "text": "Ce qu'il\nfaut obſer-\nver dans\nleur enga-\ngement."} — verbatim with "\n" line breaks and hyphens as printed, same rules as body.
- body: main text. Where a new numbered paragraph begins (its § number is in the margin), insert a marker line "<<§ 14>>" at the start of that paragraph. Footnote call signs in the body as printed, e.g. "(a)" or "(*)".
- notes: list of footnotes in order, each {"mark": "(a)", "text": "..."} verbatim, including the citation exactly as printed (author, work, book, chapter, §, page). A note continued from the previous page: mark "cont".
- catch: catchword at page foot, or "".
- kind: one of "text", "title", "preface", "toc", "index", "errata", "blank", "plate", "other".
- notes_scan: anything odd (cropped, stamp, two pages on one scan, upside down).

## Output
Write the file with the Write tool to the path given, as UTF-8 JSON:
{"vol":"JG","scan":512,"kind":"text","page":"486","head":"...","margin":[...],"body":"...","notes":[...],"catch":"...","notes_scan":""}
"scan" is the PDF page number given in the image file name (img/JGs/s-512.jpg → scan 512; img/INSTs/s-100.jpg → scan 100). Output path: /home/claude/vr/transcr/JG/s512.json or /home/claude/vr/transcr/INST/s100.json.
One file per scan. Do every scan in your range, including blanks. Then reply with one line per scan: scan number, kind, page, first § marker seen (if any), and any problems. Nothing else.

## Efficiency
- Read each 1300px page image once (img/JGs/s-NNN.jpg or img/INSTs/s-NNN.jpg). Crop the full-resolution source (img/JG/p-NNN.jpg, img/INST/p-NNN.jpg, about 2000 px wide) only for zones you cannot read with confidence (usually margins), one crop per zone at most, saved in your own scratch folder.
- Write each page's JSON as soon as it is done; do not re-read your own files.
- Commas: do not keep the irregular space before commas; do keep spaces before ; : ? ! and inside "( §. 7. )" as printed.

## Wolff-specific
- Latin. Keep ſ, æ/œ, accents (à, è, ù, quàm etc.), abbreviations and ligatures as printed (& for et). 
- Wolff's paragraphs are numbered "§. 1." centred above the paragraph (not in the margin). Put <<§ N>> where each new § begins. Marginal notes are short Latin summaries: record them in margin with "para" = the § they stand beside.
- Wolff's in-text references like "(§. 12. part. 1. Jur. nat.)" stay in the body as printed.
- Running heads like "Prolegomena." / "PRÆFATIO." go in head.

- Google Books scans: ignore black page edges, the Google watermark and any ruler. If a scan shows two pages, transcribe both in order and say so in notes_scan.
- Institutiones (1750): same layout as the Jus gentium; §§ numbered "§. N." centred; marginal summaries in the margin; running heads like "Pars I. Cap. II. De Lege naturali." go in head.
- The text is Latin; expect many abbreviations (c. for cap., §. with a dot, &c.). Keep them.
