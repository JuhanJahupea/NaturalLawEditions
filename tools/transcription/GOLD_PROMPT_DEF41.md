# Gold set: every explicit citation in Vattel's *Défense du système leibnitien* (1741)

Input JSON (path given): {"titles": {key: {"title", "notes"}}, "units": [{"id", "part", "chap", "section", "pages", "text", "notes": [{"mark", "text"}]}]}. Units are the dedication and Préface pages (Ded.k, Pref.k), Vattel's numbered paragraphs (D.n), and a fold-out table (Tab.1). Italics are shown as _…_; page breaks as [p. N]. Context: Vattel defends Leibniz's and Wolff's system against Jean-Pierre de Crousaz, *Examen de l'Essai de M. Pope sur l'homme* (Lausanne 1737) and *Commentaire sur la traduction en vers de M. l'abbé Du Resnel de l'Essai de M. Pope* (Genève 1738); Partie II ch. VI examines the first, ch. VII the second; ch. VIII answers Pierre Roques's letters (Mercure suisse 1737, Journal helvétique 1738-39).

Task: list every explicit citation of another text, in the text and in the notes:
- a reference: an author or work named with a locus or as the source of a point ("Théod. §. 9.", "Dictionaire, Article Rorarius", "(p. 58.)" for a page of Crousaz, "Psychol. Ration. §. 536.", "Rom. VIII. 28.");
- a quotation: words given as another author's (in quotation marks „ or italics introduced as his), with or without a locus.
Resolve "Ibid.", "ubi supra", "l. c." and bare page numbers to the work they point to, from the text and the notes before them. A bare "(p. 58.)" after a mention of Crousaz is a page of the work under discussion in that chapter (the Examen in Part I, the Préface and Part II ch. I-VI unless the text says otherwise; the Commentaire in ch. VII); after a mention of Roques it is the letter under discussion. Vattel's own cross-references to his paragraphs, "(215)", "(13 & suiv.)", are not citations: skip them. Do not list a mere mention of a person without a text ("les Cartésiens", "Mr. Newton").

For each citation give:
- unit; where: "text" or "note (a)" etc.; raw: the words of the citation as they stand, copied exactly (the locus words, or for a quotation without locus its first few words);
- author: normalized name (Leibniz, Wolff, Crousaz, Bayle, Clarke, Pope, Roques, Bible, ...); work: normalized short title (e.g. "Théodicée", "Théodicée, Discours de la conformité", "Recueil de diverses pièces (Des Maizeaux)", "Leibniz-Clarke, 5e écrit", "Examen de l'Essai sur l'homme", "Commentaire", "Psychologia rationalis", "Theologia naturalis", "Dictionnaire historique et critique", "Réponse aux questions d'un provincial", "Journal helvétique, Jan. 1738"...); locus: normalized ("§ 9", "p. 58", "art. Rorarius, rem. H", "Rom. 8:28");
- container: where the cited text is printed, if Vattel says ("Recueil T. I p. 83", "Acta Eruditorum 1695"); else "";
- kind: "reference" or "quotation"; resolved: true if you resolved an Ibid./ubi supra/bare page from context; note: one short phrase if anything is uncertain.

Output: write with python3 a JSON file (path given): {"citations": [...]}. Work through every unit and every note; keep the order of the book. Reply with one line: number of units read, number of citations, the ten most cited works with counts.
