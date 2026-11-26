# Pierre Roques, letters on Leibniz's system (1737–1739), as Vattel quotes them

Roques's letters were not found in a form the project can use. The issues of the *Mercure suisse* and the *Journal helvétique* were not reachable, and Vattel's later collections do not reprint them (`editions/vattel-defense-1741/provenance/sources.md`). Vattel's *Défense du système leibnitien* (1741), Partie II ch. VIII, answers the letters and quotes them at length. Those quotations stand in for the letters.

| Letter | Printed in | Passages | Answered in the *Défense* |
|---|---|---|---|
| 1. First letter to Abraham Ruchat | *Mercure suisse*, December 1737 | 70 | II.VIII section 1, §§ 354–376 |
| 2. Second letter to Ruchat | *Journal helvétique*, January 1738, pp. 104 ff. | 82 | section 2, §§ 377–396 |
| 3. Letter to Louis Bourguet | *Journal helvétique*, November 1738 | 11 | section 3, §§ 398–400 |
| 4. Second letter to Bourguet | *Journal helvétique*, February and March 1739 | 11 | section 3, §§ 401–404 |

`ROQ.json` (`nle-quoted/1`): 174 passages, 3,976 words. 153 are verbatim: Vattel sets Roques's words in italics. 21 are reports, where Vattel gives what Roques says in his own words. Each passage has the journal page Vattel gives, or the page carried over from the passage before it (`resolved`). It also has its place in the *Défense* (`at`: unit, text or note, character offsets in the unit's reading text) and the words Roques himself quotes from Leibniz, Wolff or Bayle (`embedded`).

## Method

- Two Claude Sonnet readers went through the 51 units of chapter VIII (prompt `tools/transcription/ROQUES_QUOTES_PROMPT.md`). They copied each passage character for character from the unit text.
- `tools/transcription/roques_quoted.py` placed every passage in its unit; all 174 are found exactly. It left out five reports that only point to pages ("Toutes les Conséquences, qu'on nous oppose (pag. 89, 90.)") and one passage that lies inside another.
- Check against the gold set of citations: every quotation of Roques that it lists falls in a passage.

## Known limits

- These are Roques's words as Vattel prints them: his selection, his cuts and his italics. Spelling and punctuation are Vattel's printer's.
- The split between letters 3 and 4 rests on the journal pages Vattel gives (pp. 421–442 for November 1738; pp. 143–148 and 228 for 1739).
- Some short echoes of Roques's phrases inside Vattel's replies are listed as passages, with a note. A few roman words that continue an italic run are counted as Roques's, also with a note.
- Pages carried over from an earlier passage are uncertain where the note says so.
