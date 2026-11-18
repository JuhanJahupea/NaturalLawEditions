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

Applied (2026-11-18, Vattel 1.15, Burlamaqui 1.11): every audited row carries its verdict in `audit`; the 5 wrong rows have status `rejected` and the viewer no longer shows them; the 46 labels the reader would change are changed (the old label is kept in `audit.labelWas`). Weak rows keep their status. From Vattel 1.16 and Burlamaqui 1.12, match rows rated weak have status possible (`audit.statusWas`): 24 rows of Vattel, 8 of Burlamaqui.

## Re-judge of Vattel's Pufendorf and Burlamaqui tables (2026-11-18)

`rejudge-2026-11-18.json` holds every verdict (`rejudge`).

The audit found most weak match rows of Vattel in the tables for Pufendorf and Burlamaqui. Claude Opus read every other match row of the three tables: Vattel × Pufendorf (Barbeyrac 1734), Vattel × Burlamaqui 1747, Vattel × Burlamaqui, *Principes du droit politique* (1751). Commonplaces and rows the audit had read were left out. The reader had the same task and verdicts as the audit, and was told that Vattel often follows Wolff or Grotius where Pufendorf or Burlamaqui say the same. Where the repository has a transcription of Grotius, Pufendorf or Wolff, the reader checked the passage there.

| Table | Rows | Right | Weak | Wrong | Label does not fit |
|---|---|---|---|---|---|
| Vattel × Pufendorf (Barbeyrac 1734) | 319 | 141 | 175 | 3 | 38 |
| Vattel × Burlamaqui 1747 | 15 | 2 | 12 | 1 | 3 |
| Vattel × Burlamaqui, PDP 1751 | 160 | 5 | 151 | 4 | 37 |

In most weak rows, by the readers' notes, Vattel's wording or order follows Wolff's *Jus gentium* or *Institutiones*, or Grotius in Barbeyrac's translation, and Pufendorf states the same doctrine. Burlamaqui's *Droit politique* copies Grotius, Pufendorf or Barbeyrac's notes in most of the passages these rows pair with Vattel. Its chapter on neutrals (§§ I–XII) is Barbeyrac's note 2 to Pufendorf VIII.6.7. Right rows in the Pufendorf table rest on material found only in Pufendorf or Barbeyrac's notes: examples, references in the same order, Barbeyrac's wording.

The editor changed one verdict: row 6305 (II.280, citation) is right, since Vattel's note names Pufendorf V.XII.7. The reader rated it wrong because the paired source sentence is not the one Vattel's examples follow.

The wrong rows:

- Vattel II.273, pufendorf-barbeyrac-1734, row 6289 (loose paraphrase): Vattel's anecdote follows Pufendorf's main text; Barbeyrac's note gives a different account, none of which Vattel uses.
- Vattel III.93, pufendorf-barbeyrac-1734, row 6469 (loose paraphrase): Vattel's argument is Wolff JG § 669; Barbeyrac's note holds the opposite.
- Vattel III.123, pufendorf-barbeyrac-1734, row 6484 (open disagreement): Vattel rejects a claim of Grotius that Pufendorf also rejects; there is no disagreement with Pufendorf.
- Vattel Prelim.17, burlamaqui-1747, row 1535 (loose paraphrase): only the terms internal and external obligation match; the two authors draw different distinctions with them.
- Vattel III.58, burlamaqui-droit-politique-1751, row 2237 (loose paraphrase): a different point; Vattel's is Wolff JG § 714.
- Vattel III.118, burlamaqui-droit-politique-1751, row 2296 (loose paraphrase): opposite rules on supplying war goods; Vattel's is Wolff JG § 683.
- Vattel IV.47, burlamaqui-droit-politique-1751, row 2606 (close paraphrase): Vattel quotes Grotius III.19.14 by name; Burlamaqui repeats the same quotation.
- Vattel Pref.7, burlamaqui-droit-politique-1751, row 3343 (close paraphrase): Vattel's note says he uses Barbeyrac's translation of Pufendorf II.3.23; Burlamaqui repeats the same quotation of Hobbes.

Applied (Vattel 1.16): weak rows have status possible, wrong rows `rejected` (`audit.statusWas` keeps the old status); 78 labels are changed (`audit.labelWas`). Match rows: Pufendorf table 364 → 186, Burlamaqui 1747 16 → 3, PDP 1751 174 → 19.

## Label check (2026-11-18)

`rejudge-2026-11-18.json` holds every answer (`labelCheck`).

In the audit, about 12% of the rows had a label the reader would change. To find such rows in all tables, a script (`tools/transcription/label_overlap.py`) measured the word overlap of each row's passage and source passage: the share of the shorter passage's words that occur in the same order in the other, with accents and old spellings folded. Latin sources were left out. On the audit sample, verbatim rows have a median overlap of 0.97, close paraphrase 0.58, loose paraphrase 0.23. Rows whose overlap sits far from their label's were flagged:

- verbatim below 0.7;
- close paraphrase below 0.2, or at 0.92 or more with a run of 8 or more words;
- loose paraphrase at 0.6 or more.

On the audit sample, 12 of 27 flagged rows had a label the reader would change. In all tables the script flagged 210 rows (Vattel 108, Burlamaqui 102). Claude Opus read each pair and gave the label that fits. The prompt is `tools/transcription/LABEL_CHECK_PROMPT.md`.

| Edition | Flagged | Changed |
|---|---|---|
| Vattel | 108 | 72 |
| Burlamaqui | 102 | 86 |

Changes: close paraphrase → loose paraphrase 62; loose paraphrase → close paraphrase 43; close paraphrase → verbatim 29; loose paraphrase → verbatim 13; close paraphrase → shared argument 5; loose paraphrase → shared argument 3; verbatim → loose paraphrase 1; verbatim → close paraphrase 1; verbatim → translation 1. Most changes are in the tables for Grotius (Vattel 31, Burlamaqui 5), the *Élémens* 1783 (29), Pufendorf (Burlamaqui 23, Vattel 1), the *Devoirs* (19) and Formey (17).

Applied (Vattel 1.16, Burlamaqui 1.12): a changed row carries `labelCheck` `{was, reason, date}`, and the panel shows it. Status is unchanged.

