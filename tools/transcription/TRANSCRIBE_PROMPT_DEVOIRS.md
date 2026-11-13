# Transcription instructions (Barbeyrac's French Pufendorf, Les devoirs de l'homme et du citoyen, 1756)

You are transcribing scanned pages of an 18th-century French book: Jean Barbeyrac's translation of Pufendorf, *Les devoirs de l'homme et du citoyen* (Amsterdam and Leipzig 1756, 2 vols; siglum DEV56T1/T2). The pages are small, in one column. The main text is the translation; the numbered notes at the foot are Barbeyrac's. Volume II also holds other works: Leibniz's *Jugement d'un anonyme sur l'original de cet abrégé*, Barbeyrac's *Réflexions* on it, and Barbeyrac's discourses. Read each page image with the Read tool and write one JSON file per page. Work only from the image. Never paraphrase, modernize or complete text from memory, even when you know the work.

## Images and effort
- Page image: `<WORK>/scans/img/<SIGLUM>/p<NNNN>.jpg` (NNNN = PDF page, 4 digits), trimmed to the printed area. Read it once.
- Only if the notes or the side margin are too small to read with confidence, crop them, at most two crops per page (the notes zone, one side margin):
  `python3 -I <TOOLS>/crop2.py <SIGLUM> <page> <x0> <y0> <x1> <y1>` with fractions (0–1) of the page image, e.g. `0 0.7 1 1` for the notes or `0 0 0.25 1` for a left margin. It prints the crop's path; read that with the Read tool. Never crop the main text.
- Index, table of contents, errata, blank and plate pages: write the file with kind set, body "", notes [] and margin []; do not transcribe them.

## Diplomatic rules
- Keep original spelling, accents (or their absence), capitalization and punctuation exactly, including spaces before ; : ? ! and inside "( §. 7. )".
- Long s: write ſ wherever the print has a long s. Round s stays s.
- "&" as printed; æ / œ as printed; other ligatures (also Greek ου, στ) as plain letters.
- Line breaks as "\n"; keep end-of-line hyphens exactly as printed ("en-\ngager"). Do not join words.
- Italics: <i>…</i>. Small capitals: write them as capital letters, no markup.
- Latin, Greek, Hebrew: as printed, with accents and breathings if visible. Illegible Greek: [Greek, n words].
- Illegible or damaged: [?] for one uncertain character, [...] for lost words, [word?] for a guess.
- No library stamps, handwriting or digitisation marks; mention them in notes_scan.

## Zones
- head: running head line verbatim. page: printed page number as string, or "".
- margin: what stands in the side margins, in order, each {"mark": "", "text": "..."}: marginal summaries (mark "") and the lettered glosses that give the Latin term or a reference, with their letter as mark ({"mark": "(a)", "text": "Invita."}).
- body: main text, with marker lines where the structure starts:
  - "<<LIVRE n>>" before a book heading, "<<CHAP n>>" before a chapter heading (arabic n: LIVRE SECOND → <<LIVRE 2>>, CHAPITRE V. → <<CHAP 5>>);
  - "<<§ n>>" where a numbered paragraph starts, i.e. where "§. III." or a roman paragraph number opens a paragraph (→ <<§ 3>>). Keep the printed "§. III." after the marker. Arabic sub-numbers inside a paragraph ("5.", "6.") are text, not markers.
  - Note calls exactly as printed: "(1)", "(22)", "(a)", "*".
- notes: the footnotes in reading order, top to bottom (left column first if a page has two). One entry per note: {"mark": "(22)", "sec": "", "by": "", "text": "..."}.
  - sec: the group label printed before a group of notes, exactly as printed without the final period, e.g. "§. III" or "CH. II. §. I"; give it to every note of that group on this page. "" where no label is printed on this page.
  - A note continued from the previous page (the column starts mid-sentence): mark "cont". A note continued on the next page simply ends where the page ends.
  - by: "" for Barbeyrac's notes; "author" for a note signed by the author, even if Barbeyrac adds to it in [ ]; "leibniz" for a note in Leibniz's Jugement that is Leibniz's own.
- catch: catchword under the main text, or "". catch_notes: catchword under the notes, or "". sig: signature mark at the foot ("TOM. I.", "X", "C 3"), or "".
- kind: "text" (Pufendorf's Devoirs), "preface" (Barbeyrac's preface and avertissements), "jugement" (Leibniz's Jugement), "reflexions" (Barbeyrac's Réflexions on it), "discours" (Barbeyrac's discourses), "title", "toc", "index", "errata", "blank", "plate", "other". The running head tells which work a page belongs to.
- notes_scan: anything odd (cropped margin, faint, broken type, show-through), briefly.

## Output
Write each page with the Write tool to `<WORK>/tr/<SIGLUM>/s<NNNN>.json` as UTF-8 JSON:
{"vol":"DEV56T1","scan":120,"kind":"text","page":"160","head":"...","margin":[...],"body":"...","notes":[...],"catch":"...","catch_notes":"","sig":"","notes_scan":""}
Do every scan in your range, including blanks. If a file for a scan already exists, skip that scan. Write each page as soon as it is done; do not re-read your files. When all are written, reply with ONE line only: "<SIGLUM> <first>-<last>: <n> files; markers <the <<...>> markers you wrote, in order, or none>; problems: <none, or scans and what>".
