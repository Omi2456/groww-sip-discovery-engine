# Groww App Reviews dataset assessment

**Audited from:** the downloaded `groww_reviews_last5y.csv` published on the [Hugging Face dataset page](https://huggingface.co/datasets/Avaneeshkarthik/groww-app-reviews).  
**Audit date:** 2026-11-02.

## Dataset profile

- **322,726 records** in the downloaded file (the dataset viewer rounds this to 323K).
- **Date coverage:** 2020-09-28 through 2025-09-26, based on the file's `at` timestamps.
- **Fields:** `reviewId`, `content`, `score`, `at`, `userName`, `thumbsUpCount`, `appVersion`.
- **Duplicates:** 0 exact duplicate rows; 0 repeated nonblank review IDs.
- **Missing values:** 0 blank review IDs, 0 blank review texts, and 0 missing/unparseable dates.
- Every ID is 36 characters. The file has no app/package ID field and no individual review URL field. The only `userName` value is “A Google user”; the file has 326 distinct raw `appVersion` values.

## Keyword screen

Counts below are records containing each case-insensitive term or phrase in `content`. Counts overlap: one record can match multiple groups.

| Search term | Matching records |
|---|---:|
| SIP | 3,273 |
| mutual fund | 9,642 |
| AutoPay | 290 |
| mandate | 274 |
| instalment / installment | 111 |
| pause | 74 |
| stop | 2,183 |
| redemption / redeem | 780 |
| **Any listed term** | **15,137** |

The strongest first-pass SIP set is the **3,273 reviews that explicitly contain “SIP”**. Of these, **3,089** pass a transparent nontrivial-text screen (at least 20 characters, at least 4 whitespace-separated words, and not an exact generic response such as “good” or “nice”). Across all 15,137 keyword matches, 14,893 pass that same text screen.

These are candidate counts, not semantic labels. “Mutual fund” alone matches 8,594 records, and “stop” alone matches 2,059, illustrating why a broad keyword union includes unrelated feedback. The nontrivial-text threshold removes short generic comments but cannot establish that a review describes SIP behaviour. A reviewed sample or classifier with human adjudication is needed to estimate true relevance.

## Source traceability

The records have unique 36-character IDs, but **the CSV alone does not support a verified individual Google Play page link**: it contains neither a per-review URL nor app/package ID metadata, and the IDs have not been matched against original Play pages. The dataset attribution and app identity are useful corpus provenance, but should not be represented as per-record source verification. Keep the `source_review_url` blank in the filtered files until a specific original URL is established.

## Comparison with the earlier 200-review CSV

`Groww_Raw_Reviews.csv` in Downloads contains 200 rows and fields `Review_ID`, `Review_Text`, `Rating`, `Review_Date`, `Helpful_Votes`, and `App_Version`. Compared with the downloaded 322,726-row file, it has **58 exact text overlaps** and **1 matching ID**. Treat the remaining rows as not matched by these exact checks; text edits, normalization, or different ID conventions can prevent a match.

## Reusable outputs

- `groww_sip_explicit_candidates.csv` — 3,273 records with an explicit SIP token, plus matched terms and clear provenance/URL-status fields.
- `groww_sip_keyword_candidates.csv` — 15,137 broader candidate records matching any requested term.
- `groww_reviews_hf_audit.json` — machine-readable counts, schema, examples, keyword overlaps, and prior-CSV comparison.
- `audit_groww_reviews_csv.py` — standard-library-only script to reproduce the audit and filtered exports from a local CSV.

The candidate exports identify records to analyze; they do not claim that every candidate is meaningful or source-verified. The 200-review comparison is exact text/ID matching only.
