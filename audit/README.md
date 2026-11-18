# Audits

## Precision of the reuse rows (2026-11-17)

`precision-2026-11-17.json` holds every verdict.

A random sample of reuse rows was drawn from both editions: 160 rows at status match and 40 at status possible per edition, commonplaces left out. Claude Opus read each row: the edition's passage with its context, the source passage, and the working French of a Latin source. Where the repository has a transcription of the source, the reader checked the passage there in context. Verdicts:

- right: the relation the label claims holds (the edition takes wording, or a specific argument, definition or example, from the source; for citation rows, the edition names the source; for open disagreement, the edition takes up and rejects the source's claim);
- weak: the two passages treat the same point, but nothing specific shows that the edition draws on this source rather than on the common stock;
- wrong: the passages do not match.

| Rows | Sample | Right (95% interval) | Weak | Wrong (95% interval) | Label does not fit |
|---|---|---|---|---|---|
| Vattel, match | 160 | 135 (84%, 78–89) | 24 | 1 (1%, 0–3) | 21 |
| Burlamaqui, match | 160 | 150 (94%, 89–97) | 8 | 2 (1%, 0–4) | 14 |
| Vattel, possible | 40 | 14 (35%, 22–50) | 25 | 1 (2%, 0–13) | 6 |
| Burlamaqui, possible | 40 | 16 (40%, 26–55) | 23 | 1 (2%, 0–13) | 5 |

The viewer shows match rows by default and possible rows with "Possible matches". About one match row in a hundred is wrong. Most of the remainder that is not right is weak: the edition says what the source says, but so do other writers. Possible rows are mostly weak.

Match rows by source:

| Edition | Source | Sample | Right | Weak | Wrong |
|---|---|---|---|---|---|
| Vattel | Wolff | 70 | 66 | 3 | 1 |
| Vattel | Grotius and Barbeyrac | 36 | 35 | 1 | 0 |
| Vattel | Pufendorf and Barbeyrac (DNG, Devoirs) | 26 | 19 | 7 | 0 |
| Vattel | Burlamaqui (1747, PDP 1751, Élémens 1783) | 14 | 4 | 10 | 0 |
| Vattel | Formey | 7 | 5 | 2 | 0 |
| Vattel | Bynkershoek | 3 | 3 | 0 | 0 |
| Vattel | Vattel's own works | 3 | 2 | 1 | 0 |
| Vattel | Montesquieu | 1 | 1 | 0 | 0 |
| Burlamaqui | Pufendorf and Barbeyrac (DNG, Devoirs) | 99 | 93 | 5 | 1 |
| Burlamaqui | Burlamaqui (1747, PDP 1751, Élémens 1783) | 37 | 35 | 2 | 0 |
| Burlamaqui | Grotius and Barbeyrac | 17 | 16 | 0 | 1 |
| Burlamaqui | ancient and other sources | 7 | 6 | 1 | 0 |

In Vattel, the weak rows concentrate in the Pufendorf and Burlamaqui tables. Several of them, by the readers' notes, follow Wolff or Grotius, and Pufendorf or Burlamaqui only states the same doctrine.

Labels: the reader would change the label of 46 of the 400 rows. Most often: close paraphrase → loose paraphrase 21; loose paraphrase → shared argument 6; loose paraphrase → close paraphrase 5; close paraphrase → verbatim 5; close paraphrase → translation 4; citation → close paraphrase 1; loose paraphrase → verbatim 1; loose paraphrase → citation 1.

The wrong rows:

- Vattel Pref.9, wolff-jus-gentium-1749, row 3355 (close paraphrase): Vattel's sentence on individual natural law being modified when applied to states paraphrases Wolff's earlier 'illis convenienter immutanda sunt'; this source sentence is about modifying the natural law of nations into the voluntary law, a different point.
- Vattel I.240, burlamaqui-droit-politique-1751, row 1683 (loose paraphrase): Vattel's passage is about taxes supplementing an insufficient domain; the source passage distinguishes goods for the king's upkeep from goods for state expenses.
- Burlamaqui P1.10.15, pufendorf-devoirs-barbeyrac-1756, row 4140 (loose paraphrase): Barbeyrac's Devoirs note says that human laws draw their force from divine natural law, a different point; Burlamaqui's sentence comes from Barbeyrac's note 6 on DJNG I.6.18.
- Burlamaqui P1.6.12, grotius-barbeyrac-1724, row 2011 (citation): Burlamaqui's note cites Leibniz's Jugement and Barbeyrac's remarks joined to the Devoirs, not Barbeyrac's Grotius; this source is not named, only the same reflections are mentioned in both.
- Burlamaqui P2.12.5, pouilly-theorie-1749, row 1135 (loose paraphrase): Pouilly's 'joye secrette toujours prete à se developer' (ch. XVI) describes the contentment of people in moderate labour, not the joy that follows a good action; only the phrase is shared.

Applied (2026-11-18, Vattel 1.15, Burlamaqui 1.11): every audited row carries its verdict in `audit`; the 5 wrong rows have status `rejected` and the viewer no longer shows them; the 46 labels the reader would change are changed (the old label is kept in `audit.labelWas`). Weak rows keep their status.
