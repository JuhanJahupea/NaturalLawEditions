# Transcription instructions (Wolff, *Psychologia rationalis*, Frankfurt and Leipzig, Renger, 1734; siglum PSR34)

You are transcribing scanned pages of an 18th-century Latin book: Christian Wolff's *Psychologia rationalis methodo scientifica pertractata* (1734), archive.org copy bub_gb_vMM9AAAAcAAJ (a Google Books scan). Read each page image with the Read tool and write one JSON file per page. Work only from the image. Never paraphrase, modernize or complete text from memory, even when you know the work.

## Images and effort
- Page image: `<WORK>/scans/img/PSR34/p<NNNN>.jpg` (NNNN = scan number, 4 digits), trimmed to the printed area. Read it once.
- If the marginal summaries or a passage are too small or faint to read with confidence, crop them, at most two crops per page:
  `python3 -I <TOOLS>/crop2.py PSR34 <scan> <x0> <y0> <x1> <y1>` with fractions (0–1) of the page image, e.g. `0.75 0 1 0.6` for the right margin. It prints the crop's path; read that with the Read tool.
- Ignore the "Digitized by Google" mark, library stamps, handwriting, show-through from the other side and specks; mention odd ones in notes_scan.

## Diplomatic rules
- Keep original spelling, accents (quàm, ità, à), capitalization and punctuation exactly, including spaces before ; : ? ! and inside "( §. 612. )". Do not keep the irregular space before commas.
- Long s: write ſ wherever the print has a long s ("eſt", "ſyſtema"). Round s stays s.
- "&" as printed; æ / œ as printed; ct, st and other ligatures as plain letters.
- Line breaks as "\n"; keep end-of-line hyphens exactly as printed ("cor-\npus"). Do not join words.
- Italics: <i>…</i>. Wolff sets each proposition (the first sentence or two of a §) in italics, and names in the text ("<i>Leibnitius</i>"). Small capitals and capitals: as capital letters, no markup. A large decorated initial is written as a normal capital joined to its word ("In omni").
- Greek, German (Fraktur) and French: as printed, Fraktur in plain letters. Illegible or damaged: [?] for one uncertain character, [...] for lost words, [word?] for a guess.

## Zones
- head: running head line verbatim ("Sect. III. Cap. IV.", "De Harmonia præſtabilita."), without the page number. page: printed page number as string ("587"), or "".
- margin: the marginal summaries in order, each {"para": "§. 642.", "text": "Quales ſint\noperationes\ngratiæ in\neodem ſy-\nſtemate."} verbatim, with "\n" line breaks and hyphens as printed. "para" is the § the summary stands beside.
- body: the main text, with marker lines (each on its own line):
  - "<<SECTIO n>>" before a section heading (SECTIO II → <<SECTIO 2>>) and "<<CAPUT n>>" before a chapter heading (CAPUT IV → <<CAPUT 4>>); transcribe the heading and title after the marker, as printed.
  - "<<§ n>>" where a numbered paragraph begins: Wolff prints "§. 612." centred above it. Keep the printed heading after the marker ("<<§ 612>>\n§. 612.\n<i>Syſtema harmoniæ</i> …").
  - "<<NOTA>>" before each note: the paragraphs set in smaller type, usually indented, that follow the demonstration of a § (they open with words like "Syſtema hoc invenit", "In hoc differt"). Everything after <<NOTA>> up to the next <<§ n>> marker is the note. A page that opens inside a note continued from the previous page starts with "<<NOTA>>".
  - In-text references such as "(§. 612.)", "(§. 725. Ontol.)", "(not. §. 605.)" stay in the body as printed.
- notes: footnotes at the foot of the page, if any, as {"mark": "(a)", "text": "..."}; usually none.
- catch: the catchword at the foot, or "". sig: the signature ("Ddd 2", "Ee ee 2"), or "".
- kind: "text", "title", "blank", "plate", "index", "other".
- notes_scan: anything odd (faint, cropped edge, gutter shadow, words read from context), briefly.

## Output
Write each page with the Write tool to `<WORK>/tr/PSR34/s<NNNN>.json` as UTF-8 JSON:
{"vol":"PSR34","scan":605,"kind":"text","page":"587","head":"De Harmonia præſtabilita.","margin":[...],"body":"...","notes":[],"catch":"SECTIO","sig":"Ee ee 2","notes_scan":""}
Do every scan in your range. If a file for a scan already exists, skip that scan. Write each page as soon as it is done; do not re-read your files. When all are written, reply with ONE line only: "PSR34 <first>-<last>: <n> files; § markers <first>–<last>; NOTA <n>; problems: <none, or scans and what>".
