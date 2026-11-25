# Crousaz, *Commentaire sur la traduction en vers de Mr. l'abbé Du Resnel, de l'Essai de M. Pope sur l'homme* (Genève, Pellissari & Comp., 1738)

The book Vattel answers in Partie II ch. VII of the *Défense du système leibnitien* (1741). He cites it by page ("Com. pag. 41, 42."), 59 times.

| File | Pages | Copy | Contents |
|---|---|---|---|
| `COM38.json` (`nle-ocr/1`) | 376 | Google Books PDF supplied by the editor (382 scans); stamp of the Biblioteca Nazionale Vittorio Emanuele, Rome; probably Google Books daRZAAAAcAAJ | Avis au lecteur; Lettre à M. de Crousaz (pp. 1–28); Commentaire sur les Épîtres I–IV (pp. 29–351); a second Lettre à M. de Crousaz (pp. 352–353); Réponse de M. de Crousaz (pp. 354–374) |

Printed page = scan − 8.

## Method and limits

- `tools/transcription/crousaz_ocr.py`: Google's OCR text layer of the PDF, page by page. The running head is kept apart as `head`; `part` is taken from the running heads. Nothing is corrected by hand.
- The OCR keeps long s as `ſ` on most pages and reads it as f on others. The reuse search folds s and f.
- Check against the *Défense*: of the 42 quotations Vattel gives with a page of the *Commentaire*, 38 share wording with that page, 2 with the next page, 2 with neither.
