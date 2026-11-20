# Transcription instructions (Vattel, *Essai sur le fondement du droit naturel*, in *Le loisir philosophique*, Genève 1747)

You are transcribing scanned pages of an 18th-century French book: Emer de Vattel's *Essai sur le fondement du droit naturel, et sur le premier principe de l'obligation où se trouvent tous les hommes, d'en observer les loix*, printed in *Le loisir philosophique, ou pièces diverses de philosophie, de morale et d'amusement* (Genève 1747; siglum LOI47). Small octavo pages; numbered paragraphs (1., 2., …); footnotes at the foot. Read each page image with the Read tool and write one JSON file per page. Work only from the image. Never paraphrase, modernize or complete text from memory, even when you know the work.

## Images and effort
- Page image: `<WORK>/scans/img/LOI47/p<NNNN>.jpg` (NNNN = PDF page, 4 digits), trimmed to the printed area. Read it once.
- If the footnotes are too small to read with confidence, crop them, at most two crops per page:
  `python3 -I <TOOLS>/crop2.py LOI47 <page> <x0> <y0> <x1> <y1>` with fractions (0–1) of the page image, e.g. `0 0.6 1 1`. It prints the crop's path; read that with the Read tool. Never crop the main text.
- Ignore the "Digitized by Google" mark, library stamps, handwriting and specks; mention odd ones in notes_scan.

## Diplomatic rules
- Keep original spelling, accents (or their absence), capitalization and punctuation exactly, including spaces before ; : ? ! and inside "( a )".
- Long s: write ſ wherever the print has a long s. Round s stays s.
- "&" as printed; æ / œ as printed; ct, st and other ligatures as plain letters.
- Quotation marks: Vattel quotes long passages with „ or ,, at the start of each line. Keep them exactly as printed, at the start of each line where the print has them ("„ ").
- Line breaks as "\n"; keep end-of-line hyphens exactly as printed ("ob-\nligation"). Do not join words.
- Italics: <i>…</i>. Small capitals and capitals: as capital letters, no markup (GROTIUS, BARBEYRAC). A large initial letter is written as a normal capital joined to its word ("LEs Loix").
- Latin: as printed. Illegible or damaged: [?] for one uncertain character, [...] for lost words, [word?] for a guess.

## Zones
- head: running head line verbatim ("ESSAI SUR LE", "DROIT NATUREL, &c."). page: printed page number as string, or "".
- body: main text, with a marker line "<<§ n>>" where a numbered paragraph starts, i.e. where an arabic number "13." opens a paragraph (→ <<§ 13>>). Keep the printed "13." after the marker. On the first page put the title before the first marker, as printed (with its line breaks). Note calls exactly as printed: "(1)", "(a)", "*".
- notes: the footnotes in reading order. One entry per note: {"mark": "(1)", "text": "..."}. Numbered notes (1), (2) are Vattel's remarks; lettered notes (a), (b) are references. A note continued from the previous page (it starts mid-sentence): mark "cont".
- catch: catchword under the main text (often after the signature line), or "". catch_notes: catchword under the notes, or "". sig: signature mark at the foot ("A ii", "B"), or "".
- kind: "text", "title", "blank", "other".
- notes_scan: anything odd (faint, broken type, show-through), briefly.

## Output
Write each page with the Write tool to `<WORK>/tr/LOI47/s<NNNN>.json` as UTF-8 JSON:
{"vol":"LOI47","scan":30,"kind":"text","page":"14","head":"...","body":"...","notes":[...],"catch":"...","catch_notes":"","sig":"","notes_scan":""}
Do every scan in your range. If a file for a scan already exists, skip that scan. Write each page as soon as it is done; do not re-read your files. When all are written, reply with ONE line only: "LOI47 <first>-<last>: <n> files; markers <the <<...>> markers you wrote, in order>; problems: <none, or scans and what>".
