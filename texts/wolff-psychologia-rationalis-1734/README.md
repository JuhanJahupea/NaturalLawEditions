# Wolff, *Psychologia rationalis methodo scientifica pertractata* (Frankfurt and Leipzig, Renger, 1734)

Page transcription of Sectio II (*De facultate appetendi*) and Sectio III (*De commercio inter mentem et corpus*), made for the reuse comparison with Vattel's *Défense du système leibnitien* (1741). Vattel cites the work twenty-one times, all in these sections: §§ 527, 536, 546, 604, 605 nota, 625 and nota, 628, 632 nota, 633, 638 and nota ("Psychol. ration. §. 638.").

| File | Scans | Copy | Contents |
|---|---|---|---|
| `PSR34.json` | 193 pages (scans 413–605) | archive.org [bub_gb_vMM9AAAAcAAJ](https://archive.org/details/bub_gb_vMM9AAAAcAAJ) (Google Books scan) | Sectio II–III, §§ 480–642 (printed pp. 395–587) |

Scan numbers are the PDF pages of the archive.org item; printed page = scan − 18. A second copy, [bub_gb_szJNAAAAMAAJ](https://archive.org/details/bub_gb_szJNAAAAMAAJ), cuts off the right edge of many pages; its OCR serves the checks only.

## Method

- Claude Sonnet subagents, about 24 pages each, read each page image (at most 1300 × 1560 px). Prompt: `tools/transcription/TRANSCRIBE_PROMPT_PSR34.md`.
- Diplomatic rules as for the other Wolff transcriptions: spelling, accents, capitals and punctuation as printed; long s as `ſ`; line breaks and line-end hyphens kept; italics as `<i>…</i>`.
- `body` has marker lines `<<SECTIO n>>`, `<<CAPUT n>>`, `<<§ n>>` and `<<NOTA>>`. `<<NOTA>>` opens Wolff's note to a § (the paragraphs in smaller type after the demonstration), which Vattel cites as "in notâ". `margin` holds the marginal summaries with the § they stand beside.

## Checks

- `tools/transcription/qc_psr34.py`: every scan has a file; printed page numbers agree with scan − 18; the § markers run 480–642, each once, in order; the two SECTIO and six CAPUT headings are marked; catchwords lead into the next page, except on p. 398, where the print's catchword "ſoria" stands for "ſenſoria".
- `tools/transcription/fix_psr34.py`: on 113 pages a reader had written the catchword as the last body line as well; that line is dropped. Three catchwords misread by the readers are corrected from the images.
- Agreement with archive.org's OCR of the same page in either copy (words of six letters or more, long s and f, u and v, i and j folded): 11 pages fall below 60 per cent. The OCR of both copies is poor.
- SECOND_READING

## Known limits

- The scans show through from the other side and are blurred on many pages. `notes_scan` names the pages and the words read from context.
- The boundary between demonstration and note rests on type size. Where blur hides it, the `<<NOTA>>` marker may stand a paragraph early or late.
- Sectio I (§§ 1–479, with § 66, Wolff's definition of the soul's essence, which Roques quotes) and Sectio IV are not transcribed. archive.org's OCR of them serves the reuse search only.
