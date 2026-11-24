# Transcription instructions (Vattel, *Défense du système leibnitien*, Leide 1741)

You are transcribing scanned pages of an 18th-century French book: Emer de Vattel's *Défense du système leibnitien contre les objections et les imputations de Mr. de Crousaz* (Leide, Jean Luzac, 1741; siglum DEF41). Small octavo pages: a dedication to the King of Prussia, a Préface, then two Parties in chapters, with paragraphs numbered 1, 2, 3 … through the whole book, and footnotes at the foot. Read each page image with the Read tool and write one JSON file per page. Work only from the image. Never paraphrase, modernize or complete text from memory, even when you know the work.

## Images and effort
- Page image: `<WORK>/scans/img/DEF41/p<NNNN>.jpg` (NNNN = scan number, 4 digits), trimmed to the printed area. Read it once.
- If the footnotes are too small to read with confidence, crop them, at most two crops per page:
  `python3 -I <TOOLS>/crop2.py DEF41 <scan> <x0> <y0> <x1> <y1>` with fractions (0–1) of the page image, e.g. `0 0.6 1 1`. It prints the crop's path; read that with the Read tool. Never crop the main text.
- Ignore the "Digitized by Google" mark, library stamps, bookplates, handwriting and specks; mention odd ones in notes_scan.

## Diplomatic rules
- Keep original spelling, accents (or their absence), capitalization and punctuation exactly, including spaces before ; : ? ! and inside "( a )".
- Long s: write ſ wherever the print has a long s. Round s stays s.
- "&" as printed; æ / œ as printed; ct, st and other ligatures as plain letters.
- Quotation marks: keep „ or ,, or « » exactly as printed, at the start of each line where the print has them ("„ ").
- Line breaks as "\n"; keep end-of-line hyphens exactly as printed ("ob-\nligation"). Do not join words.
- Italics: <i>…</i>. The Préface and the dedication are set mostly in italics with some words in roman: mark exactly what is italic, whatever the proportion. Small capitals and capitals: as capital letters, no markup (LEIBNITZ, CROUSAZ, WOLFF). A large initial letter is written as a normal capital joined to its word ("COMME", "LE titre").
- Greek and Latin: as printed. Illegible or damaged: [?] for one uncertain character, [...] for lost words, [word?] for a guess.
- Numbers in parentheses inside the text, such as "(215)" or "(13 & suiv.)", are the author's cross-references to his numbered paragraphs: keep them as text. They are not note calls.

## Zones
- head: running head line verbatim ("DÉFENSE DU SYSTÈME", "LEIBNITIEN. PARTIE I. CHAP. II.", "PRÉFACE.", "DEDICATOIRE."), without the page number. page: printed page number as string, or "" (the dedication and the Préface have none).
- body: main text, with marker lines (each on its own line) where the structure starts:
  - "<<PARTIE n>>" before the heading of a Partie (PREMIERE PARTIE → <<PARTIE 1>>);
  - "<<CHAP n>>" before a chapter heading (CHAPITRE SECOND → <<CHAP 2>>); transcribe the heading and the chapter's title after it, as printed;
  - "<<SECTION n>>" before a section heading inside a chapter (SECTION PREMIERE → <<SECTION 1>>);
  - "<<§ n>>" where a numbered paragraph starts, i.e. where an arabic number with a point ("13.", "220.") opens a paragraph (→ <<§ 13>>). Keep the printed number after the marker ("<<§ 13>>\n13. EXPLIQUONS …"). The number may stand at the start of the first line, beside a large initial, or in the margin; check the sequence against the paragraphs before and after on your pages. Numbers that are objection or point numbers inside a paragraph ("Prémière Objection", "1°", "I.") are text, not markers.
  - "<<DEDICACE>>" before the first line of the dedication, "<<PREFACE>>" before the heading of the Préface.
  Note calls exactly as printed: "(a)", "(b)", "(*)", "*".
- notes: the footnotes in reading order. One entry per note: {"mark": "(a)", "text": "..."}. A note continued from the previous page (it starts mid-sentence, without a mark): mark "cont".
- catch: catchword under the main text (often on the line with the signature), or "". catch_notes: catchword under the notes, or "". sig: signature mark at the foot ("A 2", "B", "* 3"), or "".
- kind: "text", "title" (the title page: transcribe it, line by line), "blank", "plate" (an engraving with no text), "other".
- notes_scan: anything odd (faint, broken type, show-through, a word you could not read), briefly.

## Output
Write each page with the Write tool to `<WORK>/tr/DEF41/s<NNNN>.json` as UTF-8 JSON:
{"vol":"DEF41","scan":30,"kind":"text","page":"14","head":"...","body":"...","notes":[...],"catch":"...","catch_notes":"","sig":"","notes_scan":""}
Do every scan in your list. If a file for a scan already exists, skip that scan. Write each page as soon as it is done; do not re-read your files. When all are written, reply with ONE line only: "DEF41 <first>-<last>: <n> files; markers <the <<...>> markers you wrote, in order>; problems: <none, or scans and what>".
