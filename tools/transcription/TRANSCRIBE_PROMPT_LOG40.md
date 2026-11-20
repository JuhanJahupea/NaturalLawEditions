# Transcription instructions (Wolff, Philosophia rationalis sive Logica, Frankfurt and Leipzig, Renger, 1740 (MDZ bsb10008633): the Discursus praeliminaris de philosophia in genere; siglum LOG40)

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
Write the file with the Write tool as UTF-8 JSON to <WORK>/tr/LOG40/s<NNNN>.json (NNNN = the 4-digit canvas number in the image name):
{"vol":"LOG40","scan":142,"kind":"text","page":"118","head":"...","margin":[...],"body":"...","notes":[...],"catch":"...","notes_scan":""}
One file per scan. Do every scan in your range. If a file for a scan already exists, skip that scan. When all are written, reply with ONE line only: "LOG40 <first>-<last>: <n> files; § markers <first>–<last>; problems: <none, or scans and what>".

## Efficiency
- Page image: <WORK>/scans/img/LOG40/p<NNNN>.jpg (NNNN = MDZ canvas number, 1300 px wide). Read it once.
- Only for a zone you cannot read with confidence (usually the margins), fetch a full-resolution crop, at most two per page: `python3 -I <TOOLS>/mdz_crop.py LOG40 <canvas> <x0> <y0> <x1> <y1>` with fractions (0-1) of the page, e.g. `0 0.4 0.3 0.8` for the left margin. It prints the crop's path; read that with the Read tool.
- Write each page's JSON as soon as it is done; do not re-read your own files.
- Commas: do not keep the irregular space before commas; do keep spaces before ; : ? ! and inside "( §. 7. )" as printed.

## Wolff-specific
- Latin. Keep ſ, æ/œ, accents (à, è, ù, quàm etc.), abbreviations and ligatures as printed (& for et). 
- Wolff's paragraphs are numbered "§. 1." centred above the paragraph (not in the margin). Put <<§ N>> where each new § begins. Marginal notes are short Latin summaries: record them in margin with "para" = the § they stand beside.
- Wolff's in-text references like "(§. 12. part. 1. Jur. nat.)" stay in the body as printed.
- Running heads like "Prolegomena." / "PRÆFATIO." go in head.

- MDZ colour scans: ignore page edges, show-through from the other side and specks.
- Running heads like "Discursus praeliminaris" or "Cap. I." go in head as printed.
