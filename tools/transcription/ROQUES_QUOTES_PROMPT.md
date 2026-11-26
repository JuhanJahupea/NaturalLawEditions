# Roques's letters as Vattel quotes them (Défense du système leibnitien, 1741, Partie II ch. VIII)

Pierre Roques's letters on Leibniz's system are not available to the project. Vattel's chapter VIII answers them and quotes them at length; those quotations stand in for the letters. Your task: list every passage of Roques that Vattel gives, with its exact words.

The letters:
- Section 1 answers the first letter to Ruchat, *Mercure suisse*, December 1737.
- Section 2 answers the second letter to Ruchat, *Journal helvétique*, January 1738, pp. 104 ff.
- Section 3 answers the two letters to Bourguet, *Journal helvétique*, November 1738, February and March 1739.
Vattel gives page numbers of the journal in parentheses ("(p. 432.)") or in notes. A number in parentheses that is not a page, such as "(215)", is Vattel's cross-reference to his own paragraph.

Input JSON (path given): {"titles", "titleNotes", "units": [{"id", "section", "text", "notes": [{"mark", "text"}]}]}. In `text`, italics are shown as _…_ and page breaks of the Défense as [p. N]. Vattel sets Roques's words in italics, usually introduced by "Mr. ROQUES dit", "continue-t-il", "ajoute-t-il" and the like. Inside them, words Roques quotes from Leibniz or Wolff stand in „…" marks or in roman, often with "dit-il". Other italics are Vattel's emphasis or titles: they are not Roques's.

For every passage of Roques give:
- unit; where: "text" or "note (a)";
- text: the passage exactly as it stands in the unit, copied character for character, the _ marks and [p. N] included, from its first word to its last. Copy only Roques's words; leave out Vattel's "dit-il", "continue Mr. ROQUES" unless they stand inside the italics. One passage = one continuous run; where Vattel breaks into it, start a new passage;
- kind: "verbatim" (set off by italics or quotation marks as Roques's words), or "report" (Vattel reports what Roques says in his own words: "Mr. ROQUES prétend que…"; give the report clause as text);
- letter: 1 (first to Ruchat), 2 (second to Ruchat), 3 (to Bourguet, November 1738), 4 (to Bourguet, February or March 1739), or 0 if you cannot tell within section 3;
- page: the journal page Vattel gives for it, or the page carried over from the passage before it in the same letter ("resolved": true), or "";
- embedded: the words Roques himself quotes inside the passage (Leibniz, Wolff, the Bible…), as [{"author", "locus", "text"}], copied exactly; [] if none;
- note: one short phrase if anything is uncertain.

Write the result with python3 to the output path given, as {"passages": [...]} in the order of the book. Then reply with ONE line: units read, passages (verbatim / report), passages per letter.
