# Vattel in American documents, 1762–1776: a search of thirty volumes

*Data report, built by `tools/reports/vattel_american_reuse.py` from [data/vattel-american-reuse.json](data/vattel-american-reuse.json), which `tools/american/` builds. The edition vattel-1773 1.19 gives Vattel's English (London, 1797), his French and the sources of each French passage. Thirty volumes and pamphlets were searched against Vattel's English; candidate passages were read by one language model and every match by a second.*

The corpus holds the pamphlets of Otis (1762, 1764, 1765), Thacher, Dulany, Bland, Dickinson (1768, 1774), Jefferson's *Summary View*, Wilson, Hamilton, Seabury and Paine's *Common Sense*; the Boston *Votes and Proceedings* of 1772; Bradford's *Speeches of the Governors of Massachusetts* (1765–1775); the writings of Samuel Adams to 1776; John Adams's diary to 1776, his essays and *Novanglus* with Leonard's *Massachusettensis*; and the *Journals of the Continental Congress*, 1774–1776.

The search finds 29 reuses of 17 sections of Vattel in 18 documents, from 1764 to 1775. 16 are among the citations that Ossipow and Gerber, Somos and Schmeeckle report ([Which Vattel did the colonists cite?](?r=vattel-american-sources)); 13 are not. The journals of Congress, *Common Sense*, the *Summary View*, Wilson, Dickinson, Hamilton, Dulany, Seabury and Otis's *Vindications* have none. 9 of the 18 documents are by Samuel Adams or by the House in his drafting.

No document in the corpus names Wolff.

## Sources of the reused passages

For each reuse, the second reader found the French words that the English renders and the edition's sources for those words. *Wolff, close*: a close paraphrase or translation of Wolff covers them. *Wolff, loose*: only a loose paraphrase of Wolff. *Against Wolff*: a divergence note, where Vattel had Wolff's passage before him and reached the opposite point. *Other source*: Grotius, Pufendorf or Burlamaqui only. *Vattel's own*: no source in the tables.

| source of the French words | reported in the studies | found here only |
|---|---|---|
| Wolff, close | 11 | 0 |
| Wolff, loose | 1 | 3 |
| against Wolff | 3 | 0 |
| other source | 0 | 3 |
| Vattel's own | 1 | 5 |
| other source and Vattel's own | 0 | 1 |
| Vattel's own and other source | 0 | 1 |

All 11 reuses of passages that Vattel took closely from Wolff are among those the studies report. None of the 13 reuses found here only is one. They render sentences of Vattel's own or of Grotius, Pufendorf and Burlamaqui, or loose paraphrases of Wolff.

The last sentence of [I § 34](../viewer/?ed=vattel-1773#I.34), on a nation's silence as consent to a change of its constitution, has no source in the tables. Four documents of 1768–1771 use it: Massachusetts House of Representatives, Letter to the Earl of Shelburne, 15 January 1768 (Bradford 140; Cushing I, 158); Massachusetts House of Representatives, Letter to Benjamin Franklin, 29 June 1771 (Cushing II, 178); Samuel Adams, "Candidus", Boston Gazette, 19 August 1771 (Cushing II, 202); Samuel Adams, "Candidus", Boston Gazette, 14 October 1771 (Cushing II, 254-255). The House's answer to Hutchinson of 26 January 1773 restates it without the words: the Governor's speech had left the House the choice "either of appearing by our silence to acquiesce in your Excellency's sentiments, or of thus freely discussing this point" (Bradford, 364).

## The reuses

| date | document | § | form | Vattel named | source of the French words | in the studies | pages | 1760 / 1797 |
|---|---|---|---|---|---|---|---|---|
| 1764 | James Otis, The Rights of the British Colonies Asserted and Proved (Boston, 1764): the memorial of the House and its notes | [I.210](../viewer/?ed=vattel-1773#I.210) | quotation | yes | Wolff, close | yes | 106, 110 | 0.52 / 0.45 |
| 1764 | Oxenbridge Thacher, The Sentiments of a British American (Boston, 1764) | [I.24](../viewer/?ed=vattel-1773#I.24) | quotation | yes | Vattel's own | yes | Thacher, 4 | 0.47 / 0.47 |
| 1764 | James Otis, The Rights of the British Colonies Asserted and Proved (Boston, 1764): the memorial of the House and its notes | [I.34](../viewer/?ed=vattel-1773#I.34) | quotation |  | Wolff, close | yes | 109 | 0.48 / 0.35 |
| 1764 | James Otis, The Rights of the British Colonies Asserted and Proved (Boston, 1764): the memorial of the House and its notes | [III.201](../viewer/?ed=vattel-1773#III.201) | quotation | yes | against Wolff | yes | 111–112 | 0.58 / 0.46 |
| 1765-12-27 | John Adams, Diary, 27 December 1765 | [II.282](../viewer/?ed=vattel-1773#II.282) | quotation | yes | Wolff, close | yes | Works of John Adams, 166 | 0.40 / 0.40 |
| 1765-12-27 | John Adams, Diary, 27 December 1765 | [II.292](../viewer/?ed=vattel-1773#II.292) | quotation | yes | Wolff, close | yes | Works of John Adams, 166 | 0.79 / 0.38 |
| 1765-12-27 | John Adams, Diary, 27 December 1765 | [II.297](../viewer/?ed=vattel-1773#II.297) | quotation | yes | Wolff, loose | yes | Works of John Adams, 166 | 0.71 / 0.45 |
| 1766 | Richard Bland, An Inquiry into the Rights of the British Colonies (Williamsburg, 1766) | [I.2](../viewer/?ed=vattel-1773#I.2) | close paraphrase | yes | Wolff, loose |  | [10] | 0.35 / 0.29 |
| 1766 | Richard Bland, An Inquiry into the Rights of the British Colonies (Williamsburg, 1766) | [III.290](../viewer/?ed=vattel-1773#III.290) | close paraphrase |  | Wolff, loose |  | [27] | 0.25 / 0.29 |
| 1768-01-15 | Massachusetts House of Representatives (Samuel Adams), Letter to the Earl of Shelburne, 15 January 1768 | [I.34](../viewer/?ed=vattel-1773#I.34) | verbatim |  | Vattel's own |  | Bradford 140; Cushing I, 158 | 0.52 / 0.41 |
| 1768-01-29 | Massachusetts House of Representatives (Samuel Adams), Letter to Lord Camden, 29 January 1768 | [I.35](../viewer/?ed=vattel-1773#I.35) | close paraphrase |  | other source |  | Cushing I, 176 | 0.33 / 0.33 |
| 1768-01-29 | Massachusetts House of Representatives (Samuel Adams), Letter to Lord Camden, 29 January 1768 | [I.36](../viewer/?ed=vattel-1773#I.36) | close paraphrase |  | other source |  | Cushing I, 177 | 0.22 / 0.11 |
| 1771-01-21 | Samuel Adams, "Vindex", Boston Gazette, 21 January 1771 | [I.24](../viewer/?ed=vattel-1773#I.24) | quotation |  | Vattel's own |  | Cushing II, 143 | 0.46 / 0.13 |
| 1771-01-21 | Samuel Adams, "Vindex", Boston Gazette, 21 January 1771 | [I.30](../viewer/?ed=vattel-1773#I.30) | quotation |  | other source and Vattel's own |  | Cushing II, 151 | 0.54 / 0.42 |
| 1771-06-29 | Massachusetts House of Representatives (Samuel Adams), Letter to Benjamin Franklin, 29 June 1771 | [I.34](../viewer/?ed=vattel-1773#I.34) | close paraphrase |  | Vattel's own |  | Cushing II, 178 | 0.13 / 0.08 |
| 1771-08-19 | Samuel Adams, "Candidus", Boston Gazette, 19 August 1771 | [I.34](../viewer/?ed=vattel-1773#I.34) | close paraphrase |  | Vattel's own |  | Cushing II, 202 | 0.03 / 0.00 |
| 1771-10-14 | Samuel Adams, "Candidus", Boston Gazette, 14 October 1771 | [I.34](../viewer/?ed=vattel-1773#I.34) | quotation |  | Vattel's own and other source |  | Cushing II, 254-255 | 0.50 / 0.36 |
| 1771-10-28 | Samuel Adams, "Valerius Poplicola", Boston Gazette, 28 October 1771 | [I.220](../viewer/?ed=vattel-1773#I.220) | quotation | yes | against Wolff | yes | Cushing II, 258 | 0.52 / 0.35 |
| 1771-10-28 | Samuel Adams, "Valerius Poplicola", Boston Gazette, 28 October 1771 | [I.223](../viewer/?ed=vattel-1773#I.223) | quotation | yes | against Wolff | yes | Cushing II, 258 | 0.71 / 0.88 |
| 1772-01-27 | Samuel Adams, "Candidus", Boston Gazette, 27 January 1772 | [I.34](../viewer/?ed=vattel-1773#I.34) | quotation | yes | Wolff, close | yes | Cushing II, 325-326 | 0.40 / 0.29 |
| 1772-01-27 | Samuel Adams, "Candidus", Boston Gazette, 27 January 1772 | [III.290](../viewer/?ed=vattel-1773#III.290) | quotation | yes | other source |  | Cushing II, 323 | 0.67 / 0.43 |
| 1772-11-20 | Boston town meeting (Samuel Adams), The State of the Rights of the Colonists, 20 November 1772 | [I.1](../viewer/?ed=vattel-1773#I.1) | close paraphrase | yes | Wolff, loose |  | Cushing II, 356 | 0.24 / 0.12 |
| 1773-01-06 | Thomas Hutchinson, Speech to the two Houses, 6 January 1773 | [I.210](../viewer/?ed=vattel-1773#I.210) | quotation |  | Wolff, close | yes | Bradford 337 | 0.75 / 0.91 |
| 1773-01-26 | Massachusetts House of Representatives, Answer to the Governor, 26 January 1773 | [I.34](../viewer/?ed=vattel-1773#I.34) | quotation |  | Wolff, close | yes | Cushing II, 421–422; Bradford 362 | 0.83 / 0.61 |
| 1773-01-26 | Massachusetts House of Representatives, Answer to the Governor, 26 January 1773 | [II.265](../viewer/?ed=vattel-1773#II.265) | quotation |  | Wolff, close | yes | Cushing II, 410; Bradford 356 | 0.33 / 0.11 |
| 1773-01-26 | Massachusetts House of Representatives, Answer to the Governor, 26 January 1773 | [II.283](../viewer/?ed=vattel-1773#II.283) | quotation |  | Vattel's own |  | Cushing II, 411; Bradford 356 | 0.60 / 0.53 |
| 1773-03-02 | Massachusetts House of Representatives, Answer to the Governor, 2 March 1773 | [I.34](../viewer/?ed=vattel-1773#I.34) | close paraphrase |  | Wolff, close | yes | Cushing II, 452; Bradford 395 | 0.17 / 0.06 |
| 1775-01-09 | Daniel Leonard, "Massachusettensis", Massachusetts Gazette, 9 January 1775 | [I.210](../viewer/?ed=vattel-1773#I.210) | verbatim |  | Wolff, close | yes | 1819, 170 | 0.51 / 0.58 |
| 1775-03-06 | John Adams, "Novanglus" no. VII, Boston Gazette, 6 March 1775 | [I.210](../viewer/?ed=vattel-1773#I.210) | quotes Leonard |  | Wolff, close | yes | 1819, 80 | 0.51 / 0.58 |

## Which English

The first English translation (London, 1760; vol. II dated 1759) was compared with each quotation and paraphrase: the share of its word sequences of four found in the 1760 text, and in the section's text of 1797. Of 28, 16 share more with 1760 and 2 more with 1797. The two nearer 1797 are Hutchinson's I § 210 and Samuel Adams's I § 223; in both the 1760 copy's OCR prints a word that breaks the comparison ("mothercountry"; a marginal note run into the text). No American text follows a reading peculiar to 1797.

- I § 210 in 1760 has both sentences, in the words of Otis's memorial: "antient possessions", "ought also to extend to its colonies". Hutchinson's quotation leaves out the second sentence and the words "a colony".
- I § 34 in 1760 has the memorial's and the House's words: "It is here demanded whether, if their power extends so far as to the fundamental laws", "the constitution of the state ought to be fixed" (1797: "It is asked whether their power extends to the fundamental laws", "ought to possess stability"). Somos's remark that the 1764 memorial was "not using the 1760 English translation" (2021, 210) does not hold.
- I § 24 in 1760 reads "it has cost rivers of blood". Thacher's "seas of blood" is his.
- III § 201 stands in chapter XIII in 1760, as in the French. Otis's "B. 3. C. 10." is a slip; Ossipow and Gerber's text gives the same chapter (2017, 534), their table XIII.
- I § 36 in 1760 reads "to judge and determine them, in conformity to its political constitution", the House's words of 1768 (1797: "conformably to"). II § 265 reads "neither the one nor the other of the interested, or contracting powers, has a right to interpret the act, or treaty, at his pleasure", the House's words of 1773 (1797: "according to his own fancy").

## The Declaration of Independence

The *Journals* hold Jefferson's draft and the adopted text. No passage of either shares wording with Vattel: the nearest sections reach a cosine of 0.11 to 0.14, against 0.25 to 0.55 for the quotations above. The sections that Ossipow and Gerber and Schmeeckle propose as its sources share a phrase or nothing.

One sentence joins Locke and Vattel. "All experience hath shewn, that mankind are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing the forms to which they are accustomed" takes Locke's "the people, who are more disposed to suffer than right themselves by resistance, are not apt to stir" (*Second Treatise* § 230) and adds "while evils are sufferable". That clause is the distinction of [III § 290](../viewer/?ed=vattel-1773#III.290), which the 1760 translation words "Every citizen should even patiently suffer supportable evils, rather than disturb the public peace" (1797: "patiently endure evils which are not insupportable"). Bland had paraphrased the same sentence at Williamsburg in 1766: "to suffer patiently rather than disturb the publick Peace". Samuel Adams quoted another passage of III § 290 in 1772. Schmeeckle proposes III § 290 for the Declaration's sentence; the wording shows a shared verb and noun, not a quotation.


## Checks

- Every quotation of Vattel that the three studies report in these volumes was found, except the House's quotation of [II § 265](../viewer/?ed=vattel-1773#II.265) in its answer of 26 January 1773, which the search for the wording of [II § 283](../viewer/?ed=vattel-1773#II.283) beside it brought up, and Samuel Adams's phrase of 1776 "with M. de Vattel, I account a state a moral person".
- The studies propose further silent sources in these volumes: Bland and Préliminaires §§ 4–5, the Circular Letter of 1768 and I § 34, Novanglus and I § 9, the Declaration on Taking Up Arms and III §§ 51–52, the Declaration of Independence. The search finds no shared wording at those places. Adams's "Distinct states may be united under one king" (Novanglus VII) states the point of I § 9 without its words.
- A probe of 36 candidates below the threshold gave no match.
- Three uses of the silence clause (the House to Franklin, 29 June 1771; Candidus, 19 August 1771) and the House's quotation of II § 265 were found by searching the corpus for the wording of verified matches, not by the retrieval.
- Several documents stand in two volumes (Bradford and Cushing; Adams's *Works* and the 1819 *Novanglus*). Each counts once.
- The pages are those of the editions named; Cushing is *The Writings of Samuel Adams* (1904–1906).
