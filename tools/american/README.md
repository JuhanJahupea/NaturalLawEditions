# Vattel in American documents, 1762–1776

The search behind `reports/data/vattel-american-reuse.json` and the data report `vattel-american-reuse`. The scripts run in a working folder outside the repository (the current directory); the repository is found from the scripts' own place. Needs Python 3, NumPy, scikit-learn and NLTK (Porter stemmer).

1. `dl.py`: the archive.org OCR (`_djvu.txt`) of every item in `items.tsv` into `raw/`. Bradford's *Speeches of the Governors* (archive.org `speechesofgovern00brad`) and *Novanglus, and Massachusettensis* (Project Gutenberg 45205, without Adams's letters to Tudor of 1818) are added by hand as `raw/bradford_speeches_1765_1775.txt` and `raw/novanglus_massachusettensis_1774_1775.txt`.
2. `norm.py`: long s, OCR "f" for long s (a word with f becomes its s form when that form is far more frequent in the clean texts), line-end hyphens; the volumes of collected writings are cut to 1776 (`CUT`). Writes `norm/`.
3. `retr.py`: windows of 90 words (step 40) against windows of Vattel's English sentences (the edition's English layer, London 1797). Tf-idf on stemmed words and word pairs; z-score of each Vattel window within the American window's row; shared word 5-grams rare in both. Writes `retr.json`. `gold.py` checks the quotations the three studies report.
4. `cluster.py` and `build_judge.py`: candidates merged per passage; judged when the cosine reaches 0.15 or three rare 5-grams are shared (210 passages, 236 sections). Judge prompt `AM_JUDGE_PROMPT.md`, twelve passages per batch. A probe of 36 candidates under the threshold gave no match.
5. `collect.py`: the matches, with a letters-only quote check on both sides. `build_verify.py`: each match with its context, the French of 1773, the edition's source rows and divergence notes, for the second reading (`AM_VERIFY_PROMPT.md`): verdict, document and page, the French words the English renders, and the sources that cover them.
6. `final.py`: one row per document and section; three uses found by searching the corpus for the wording of verified matches are added by hand (`ADD`).

The judge, probe and second-reading outputs are in `audit/american-reuse-2026-11-23.json`.
