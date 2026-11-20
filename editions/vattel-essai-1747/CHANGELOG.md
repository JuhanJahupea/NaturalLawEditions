# Changelog: vattel-essai-1747

Versions are MAJOR.MINOR. MAJOR goes up when a unit id is retired or takes a new meaning. MINOR goes up for any other change to the text, its layers or its reuse tables. Unit ids are the stable part of a citation. A retired id gets an entry in `aliases` in `edition.json`, and the viewer resolves it.

## 1.0 (2026-11-20)

- First version. Vattel, *Essai sur le fondement du droit naturel, et sur le premier principe de l'obligation où se trouvent tous les hommes, d'en observer les loix*, from *Le loisir philosophique* (Dresde: Walther, 1747), pp. 3–70: a vision transcription of the Google Books scan of the BCU Lausanne copy (`texts/vattel-loisir-1747/`). Units E.0 (title) and E.1–E.41 by the printed paragraph numbers; the print has no 28 and no 32.
- Title page of *Le loisir philosophique*.
- English: T. J. Hochstrasser's translation (Liberty Fund, 2008), aligned by sentence. It follows the 1863 reprint, which numbers 41 paragraphs: its § XXVIII is the second half of 1747 § 27, its § XXXII the second half of § 31. 158 translation flags (Claude Opus): 58 mistranslation, 52 terminology, 32 shift, 9 omission, 4 false friend, 3 addition; 13 change the doctrine or an argument.
- Reuse: Claude Opus read each section with its sources and wrote 333 rows: Wolff, *Philosophia practica universalis* I (88; transcribed for this edition, `texts/wolff-philosophia-practica-1738/`), Barbeyrac's *Devoirs* with Leibniz's *Jugement d'un anonyme* and Barbeyrac's *Réflexions* (83), Burlamaqui 1747 (68, linked to the burlamaqui-1747 edition), Barbeyrac's Pufendorf (54) and Grotius (40). 65 rows carry `attributed`: Vattel names the source.
- A second reader (Claude Opus) read every match row: 170 of 198 right, 28 weak (now possible), none wrong; 7 labels changed (`audit/README.md`).
