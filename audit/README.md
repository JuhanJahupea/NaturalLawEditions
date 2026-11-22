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

## Second precision sample (2026-11-18)

`precision-2026-11-18.json` holds every verdict.

After the re-judge, Claude Opus read a random sample of the match rows no audit had read (commonplaces left out): 100 of Vattel and 50 of Burlamaqui, with the task of the first audit (`tools/transcription/PRECISION_PROMPT.md`). Every match row an audit has read is right by now: weak rows became possible and wrong rows were rejected. The share of right match rows is therefore (audited + unaudited × share right in the sample) / all.

| Edition | Sample | Right | Weak | Wrong | Label does not fit | Match rows | Right, all match rows (95% interval) |
|---|---|---|---|---|---|---|---|
| Vattel | 100 | 87 | 13 | 0 | 9 | 2,289 (283 audited) | 89% (82–93) |
| Burlamaqui | 50 | 44 | 6 | 0 | 5 | 1,310 (150 audited) | 89% (79–95) |

Weak rows by table: Vattel, Wolff *Jus gentium* 8 of 46, Formey 3 of 9, Vattel's *Questions* and *Amusemens* 2 of 4; Grotius 0 of 29. Burlamaqui, Pufendorf 5 of 22, Locke 1 of 1. No sampled row is wrong (95% interval 0–4% for Vattel, 0–7% for Burlamaqui).

Applied (Vattel 1.17, Burlamaqui 1.13): the 19 weak rows have status possible, 14 labels are changed, every sampled row carries its verdict in `audit`.

## Wolff loci (2026-11-18)

`wolff-loci-2026-11-18.json` lists every correction.

The readers of the second sample found Wolff rows whose locus is a § that the source passage only cites: Wolff's references such as "(§. 380. 547.)" stand inside his text, and the first pass read the locus from them. A script (`tools/transcription/wolff_loci.py`) placed each Wolff row's source passage in the transcription (`texts/`) and read the § it stands in. Where the passage was found on the row's page and the § differs from the locus by more than one, the locus is corrected: 191 rows (*Jus gentium* 165, *Institutiones* 26), 17% of Wolff rows. In every one the old § number is cited on that page. Each carries `locusCheck` `{was, date}`. Differences of one § were left alone: there a § marker may be missing from the transcription. 186 source passages were not found in the transcription (OCR-era wording, or text running over two pages); their loci are unchecked.

## Rows added for the weak rows (2026-11-18)

`additions-2026-11-18.json` holds what the readers wrote.

The readers of the re-judge and of the first audit named, for many weak rows, the passage of Wolff or Grotius that Vattel follows. A script (`tools/transcription/add_cand.py`) read the named loci from the reasons: of 348 weak rows naming Wolff or Grotius, 201 already had a row at the named § in the same section. For the other 147 (in 120 sections), Claude Opus found the named passage in the transcriptions and wrote a row where Vattel takes wording, or a specific argument, definition, example or order of points, from it (`tools/transcription/ADDITIONS_PROMPT.md`). The readers wrote 193 rows and no row for 40 weak rows (the reason did not hold, or the table already had the row under another locus). After placing each passage in Vattel and each source passage on its page, and leaving out duplicates, 191 rows were added: 144 match, 47 possible (*Jus gentium* 118, Grotius 50, *Institutiones* 23). They are in `editions/vattel-1773/passes/additions.json`, step A.

## Recall (2026-11-18)

`recall-2026-11-18.json` holds every section's reading.

Precision says how many rows are right; recall says how much reuse the tables miss. Claude Opus read 24 random sections of Vattel (Préliminaires and Livres I–IV, by §) with Wolff's *Jus gentium* and *Institutiones*, Grotius and Pufendorf (both in Barbeyrac's translation, his notes included), and listed every reuse of these four sources it found, with the row that covers it, if any (`tools/transcription/RECALL_PROMPT.md`). The reader started from the pages that rows of nearby sections cite, Vattel's own citations and the § of Wolff on the same matter, then searched each source.

| Reuse found | Found | Covered by a row | Covered by a match row |
|---|---|---|---|
| All | 208 | 57 (27%) | 44 (21%) |
| Confidence 0.5 or more | 121 | 44 (36%) | 41 (34%) |
| of which *Jus gentium* | 49 | 23 (47%) | 23 (47%) |
| of which Grotius | 34 | 13 (38%) | 11 (32%) |
| of which Pufendorf | 25 | 5 (20%) | 5 (20%) |
| of which *Institutiones* | 13 | 3 (23%) | 2 (15%) |

Of the reuse the reader would defend (confidence 0.5 or more), the tables hold about a third (95% interval about 28–45%, wider in fact since the sample is 24 sections). The tables miss most: whole sections that follow one § of Wolff (II.92, II.101 on §§ 284–300), Pufendorf's examples and Barbeyrac's notes used beside Grotius (II.136, III.187), and Wolff's *Institutiones*, which Vattel uses beside *Jus gentium*. In 5 of the 23 sections with reuse, no row covers any of it (I.64, II.92, II.322, IV.36, IV.84); in I.80 the reader found no reuse of the four sources. The readers' own finds are not checked by a second reader; their precision is not measured.

The reuse the readers found and no row covered is added: 150 rows, 76 match and 74 possible (step C). The readers judged two rows wrong (4022, Grotius; 1479, Wolff § 700); they have status `rejected`.

## Vattel, Essai sur le fondement du droit naturel: second reading (2026-11-20)

`essai-second-reading-2026-11-20.json` holds every verdict.

The rows of the *Essai* were written by readers (Claude Opus) who read each section with its sources. A second reader (Claude Opus, `tools/transcription/VERIFY_PROMPT_ESSAI.md`, the task of the precision audit) read every match row: 198 rows.

| Table | Match rows | Right | Weak | Wrong |
|---|---|---|---|---|
| Wolff, *Philosophia practica universalis* I | 53 | 46 | 7 | 0 |
| Barbeyrac's *Devoirs* (Leibniz's *Jugement*, Barbeyrac's *Réflexions*) | 62 | 58 | 4 | 0 |
| Burlamaqui 1747 | 32 | 24 | 8 | 0 |
| Barbeyrac's Pufendorf | 30 | 24 | 6 | 0 |
| Barbeyrac's Grotius | 21 | 18 | 3 | 0 |
| All | 198 | 170 (86%) | 28 | 0 |

Weak rows rest on stock vocabulary or doctrine (the Roman-law definition of obligation, "parvenir à la connoissance"), or on a passage that has a closer source elsewhere (Wolff's *Theologia naturalis* I § 950, which Vattel cites and the corpus lacks). Applied (Essai 1.0): weak rows have status possible, 7 labels are changed, every read row carries `audit`. 

### Possible rows (2026-11-20)

`essai-possible-reading-2026-11-20.json` holds every verdict. The same reader task read the 135 rows the first readers rated possible.

| Table | Possible rows | Right | Weak | Wrong |
|---|---|---|---|---|
| Wolff, *Philosophia practica universalis* I | 35 | 18 | 17 | 0 |
| Burlamaqui 1747 | 36 | 12 | 21 | 3 |
| Barbeyrac's Pufendorf | 24 | 9 | 15 | 0 |
| Barbeyrac's *Devoirs* | 21 | 7 | 13 | 1 |
| Barbeyrac's Grotius | 19 | 8 | 10 | 1 |
| All | 135 | 54 (40%) | 76 | 5 |

Applied (Essai 1.1): right rows have status match, wrong rows `rejected`, weak rows stay possible; 9 labels are changed. The readers point to passages with no row: Burlamaqui II.7.11 for § 40 ("pétition de principe"); Wolff PPU § 224 for the definition of duty in § 17; PPU § 136 for the Cicero quotation in § 8.


## Vattel 1773: the passages added in 1773 (2026-11-20)

`additions-1773-2026-11-20.json` holds each addition with its rows, the sources Vattel names there and what the reader searched.

The layer `changes-1773` has 64 additions with text: added notes, added phrases and rewordings. Claude Opus read each with Wolff's *Jus gentium* and *Institutiones*, Barbeyrac's Grotius and Pufendorf, and Burlamaqui 1747 (`tools/transcription/ADDITIONS_1773_PROMPT.md`). 34 additions have no row. 62 rows are new (step V in `editions/vattel-1773/passes/additions.json`); 3 more were already in the tables.

| Table | Match | Possible |
|---|---|---|
| Grotius (Barbeyrac) | 4 | 22 |
| Pufendorf (Barbeyrac) | 0 | 13 |
| Wolff, *Jus gentium* | 1 | 8 |
| Wolff, *Institutiones* | 1 | 7 |
| Burlamaqui 1747 | 4 | 2 |

The Burlamaqui rows are in the note to Prelim. § 6 (P1.1.1, P1.5.4–5, P1.6.9, P2.2.3, P2.5.7). Most additions are historical examples from works the corpus lacks. Named most often: Grotius, *Annales et historiae de rebus Belgicis* (10 additions); the *Lettres et négociations* of Jean de Witt, with Boreel's and Van Beuningen's letters (8); Pétis de La Croix, *Histoire de Timur-Bec* (5); Mariana, *De rege et regis institutione* (4); Xenophon (4); Velly, *Histoire de France* (3); de Thou (2); the marquis de Saint-Philippe, *Mémoires* (2). One added note cites the *Journal de Bouillon* of 1771, after Vattel's death; the editors of 1773 added it.

## Essai §§ 1–8 and Wolff's *Discursus praeliminaris* (2026-11-20)

The *Discursus praeliminaris de philosophia in genere* (`texts/wolff-discursus-praeliminaris-1740/`) heads Wolff's *Logica*. It defines philosophy (§ 29), divides it (§§ 55–70), orders its parts (§§ 87–104) and sets out method (§§ 115–139) and style (§§ 140–150).

- Essai § 3 renders § 68: natural right is "une science qui nous apprend ce qui est naturellement bon, ou mauvais" (*scientia actionum bonarum atque malarum*), and the "théorie" of practical philosophy. "Consideré simplement comme homme" echoes § 63 (*quatenus est homo*).
- Essai § 4 gives to ethics Wolff's definition of practical philosophy in § 62: "diriger nos facultés pour pratiquer ce qui est bon, & pour éviter ce qui est mauvais" (*dirigendi facultatem appetitivam in eligendo bono & fugiendo malo*).
- Wolff lets natural law be taught inside ethics (§ 68). Vattel keeps natural right apart from ethics and puts it first. §§ 92 and 104 order the disciplines that way.
- Essai § 1, on keeping distinct what ordinary speech confuses, follows the style rules of §§ 144–145.
- Vattel takes nothing from §§ 1–54 (the three kinds of knowledge, philosophy in general), the theoretical parts, politics, economics or universal practical philosophy (§ 70). His definition of law (§ 2) comes from the *Philosophia practica universalis* §§ 131 and 135. The questions of foundation and obligation (§ 5) and the replies to the utilitarian and voluntarist accounts (§§ 7–8) have no counterpart in the *Discursus*.

The rows are in `editions/vattel-essai-1747/passes/wolff-discursus-praeliminaris-1740.json`: 25 rows, 6 match. The match rows: § 3 (two, § 68), § 4 (one, § 62), § 21 (two, §§ 1 and 4: knowledge by attending to oneself; we desire nothing we have not judged good) and § 22 (one, § 68).

## Vattel 1773: second reading of the added rows (2026-11-21)

`additions-second-reading-2026-11-21.json` holds every verdict. A second reader (Claude Opus, `tools/transcription/PRECISION_PROMPT.md`) read all 403 rows of `editions/vattel-1773/passes/additions.json` (steps A, C and V).

| Status before | Rows | Right | Weak | Wrong |
|---|---|---|---|---|
| match | 230 | 215 (93%, 90–96) | 15 | 0 |
| possible | 173 | 71 | 96 | 6 |

By table: *Jus gentium* 152 right of 174, *Institutiones* 37 of 49, Grotius 69 of 116, Pufendorf 24 of 58, Burlamaqui 4 of 6. Applied (Vattel 1.19): right rows have status match, weak rows possible, wrong rows `rejected`; 37 labels changed.

## Vattel 1773: full pass with the *Jus gentium* and Pufendorf (2026-11-21)

Claude Opus read every section of the Préface, the Préliminaires and Livres I–IV in 72 batches of about 22,000 characters (`tools/transcription/full_cand.py`, `FULL_PASS_PROMPT.md`). Each section came with the §§ of the *Jus gentium* it follows (those its rows cite, or the §§ between its neighbours'), pages of Barbeyrac's Pufendorf (cited by rows nearby, cited by Vattel, or nearest by vocabulary), and its rows in the *Jus gentium*, *Institutiones* and Pufendorf tables. The readers listed every reuse and whether a row covers it.

The reuse no row covered became 3,260 rows (step F): *Jus gentium* 1,773 (1,119 match), Pufendorf 1,485 (482 match; 420 in Barbeyrac's notes). 978 of 1,124 sections have one or more. The *Jus gentium* table grew from 1,370 rows to 3,153, the Pufendorf table from 626 to 2,125.

`fullpass-second-reading-2026-11-21.json` holds the second reading (`tools/transcription/fullpass_check.py`, `fullpass_apply.py`):

| Rows read | Rows | Right | Weak | Wrong |
|---|---|---|---|---|
| New match rows, random | 80 | 71 (89%, 80–94) | 9 | 0 |
| New possible rows, random | 40 | 13 | 25 | 2 |
| Rows the readers judged wrong | 49 | 4 | 34 | 11 |

The new match rows are as precise as the older ones (89% in the precision sample of 2026-11-18). Weak sampled rows have status possible, right ones match; flagged rows the second reader found wrong are `rejected`.

The readers also named Wolff rows whose locus is a § the passage only cites. `tools/transcription/wolff_loci2.py` placed every Wolff row with the old text layer's spelling folded (et/&, ae, j/i, v/u): 43 stand in another §. The 25 two or more §§ away now name the § where the passage stands (`locusCheck`); 18 that straddle two neighbouring §§ keep their locus.

## Vattel, Essai: divergences (2026-11-22)

A divergence is a place where a source offered Vattel an answer to the question his section treats, so that he could have used it (and sometimes used part of it), and he made a different or opposite point. It is not a list of counter-arguments: an open rebuttal counts where the two answers differ in substance, once for the question.

- Screen (`tools/transcription/essai_div.py`, `ESSAI_DIV_SCREEN_PROMPT.md`): Claude Opus read each of the 39 sections, in 20 batches, with up to 14 candidate source sections: those its reuse rows and its neighbours' use, and the two nearest by vocabulary in each French source. Readers could search every source section themselves and added sections they found. 614 pairs: 222 follows, 32 partly, 57 diverges, 303 not the same question.
- Verify (`essai_div_verify.py`, `ESSAI_DIV_VERIFY_PROMPT.md`): a second reader read the 67 flagged pairs (confidence 0.5 or more) with the whole source section and its notes. Kept 60, rejected 7.
- Merge (`ESSAI_DIV_MERGE_PROMPT.md`): a third reader grouped the notes that record the same doctrine of one author against the same answer of Vattel's, and kept one per group: 12 groups, 17 notes dropped. The largest group is Barbeyrac's thesis that a superior's will makes obligation; it is kept at § 11, where Vattel gives his definition, against *Réflexions* § 15.
- Result (`essai_div_write.py`): 43 notes in `editions/vattel-essai-1747/passes/divergences-<text id>.json`, all passages placed exactly. Barbeyrac 18, Burlamaqui 8, Pufendorf 8, Wolff 5 (PPU I §§ 115, 255, 262, 266 twice), Grotius 4.
- Open: Burlamaqui's *Principes* was printed in 1747, and parts of the Essai were written by 1742 (note to § 29). The 8 Burlamaqui notes compare Vattel with the printed text; Vattel could have known Burlamaqui's Geneva lectures, not the print. The verify verdicts (with the reasons for the 7 rejected pairs) and the 17 merged notes are in `audit/essai-divergences-2026-11-22.json`.

