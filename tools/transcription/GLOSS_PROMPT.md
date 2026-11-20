# Translations of foreign-language passages in three French editions

The collection holds three French texts: Vattel, *Le droit des gens* (1773 edition), Burlamaqui, *Principes du droit naturel* (1747), and Vattel, *Essai sur le fondement du droit naturel* (1747). They quote Latin (Cicero, Tacitus, Grotius, the Digest, papal letters, Wolff), some Greek, and a little English and other languages. The reader of the editions reads French but not necessarily Latin. You give each foreign-language passage an English translation.

## Input (JSON, path given)

`units`: each has `edition`, `unit`, `text` (the unit's main text), `notes` [{mark, text}] (its footnotes), and `candidates`: stretches a character model took for Latin (`la`), English (`en`) or Greek (`grc`), with `part` (`t` = the main text, `nK` = note K), `text` and `context`. The model over-reaches and falls short: candidates may be French, a bibliographic reference, or only part of a passage. Read each unit's text and notes yourself.

## What to gloss

- Every quotation or phrase in a language other than French, of two words or more, that a reader without that language would not follow: quoted sentences, maxims, legal formulas, lines of verse, a Latin clause inside a French sentence.
- One gloss per passage: the whole foreign stretch, from its first foreign word to its last (a quotation running over several sentences is one passage; a passage interrupted by French, such as "dit-il", is two).
- Not: bibliographic references and titles of works ("Lib. IV. c. 98.", "Phil. Pract. univ. p. 1. §. 118.", "De Jure Belli ac Pacis"), names, single words, Latin terms the French text itself explains, and French text.

## Each gloss

- `edition`, `unit`, `part` (`t` or `nK`); `text`: the foreign passage, copied exactly from that part (copy, never retype: spelling, spacing and punctuation as in the input, including any errors); it must occur in the part.
- `lang`: `la`, `grc`, `en`, `it`, `es`, `de`, or another ISO 639 code.
- `translation`: a plain, accurate English translation of the passage, as it stands. Where the printed text is corrupt and the sense must be guessed, say so in `note`.
- `source`: where the edition names or makes plain the author and work quoted, that author and work in a few words (e.g. "Cicero, De officiis III.29"); otherwise omit. Do not guess.
- `note`: optional, one sentence: a misprint, a doubtful reading, or a translation choice the reader needs.

## Output

Write with python3 a JSON file (path given): `{"glosses": [...], "skipped": [{"unit", "text", "why"}]}`: `skipped` lists the candidates you did not gloss (French, a reference, a single word), one line each. Check that every `text` occurs in its part before writing. Keep helper files in your scratch folder (given). Reply with one line: glosses by language, candidates skipped.
