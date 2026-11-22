# Merge: one note per divergence in Vattel's Essai

Input JSON (path given): the divergence notes of Vattel's *Essai sur le fondement du droit naturel* (1747) that two readers kept. Each note: `_key` ("E.13|DEV56|Réflexions du traducteur § 16"), `unit` (the section of the Essai), `text`, `locus`, `author` (when not the text's author), `relation`, `severity`, `question`, `comment`, `passage` (Vattel), `sourcePassage`, `confidence`.

A divergence is a place where a source offered Vattel an answer to the question his section treats, and he chose to make a different or opposite point. The layer should record each divergence once.

Vattel answers Barbeyrac several times (§§ 11–18 and 29–41). Barbeyrac states the same doctrine in several places: *Réflexions du traducteur* §§ 6, 15 and 16, note 4 to Grotius DGP I.1.10, note 4 to Pufendorf DNG I.6.5, note 1 to *Devoirs* I.2.3. The readers worked on different sections, so the same difference can appear several times.

## What to do

1. Group the notes that record the same difference: the same doctrine of the same source author against the same answer of Vattel's. Two notes on different sub-questions (for example "is there a middle between obligation and no obligation" and "can the nature of things oblige by itself") are different divergences. Notes on different authors (Wolff, Pufendorf, Barbeyrac, Leibniz, Grotius, Burlamaqui) are never the same divergence.
2. In each group of two or more, keep one note: the one at the section where Vattel states his own answer most fully, and whose source passage states the doctrine most exactly. Drop the others.
3. Do not drop a note for any other reason. Do not edit notes.

## Output

Write with python3 a JSON file (path given): `{"drop": [{"key": "<_key of the dropped note>", "kept": "<_key of the note kept in its place>", "reason": "one sentence"}], "groups": <number of groups of two or more>}`. Reply with one line: notes read, groups, notes dropped.
