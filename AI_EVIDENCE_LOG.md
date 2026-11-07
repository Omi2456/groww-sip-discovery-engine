# AI Evidence Log — Groww SIP Discovery Engine

**Working branch:** `ai-discovery-gemini`  
**Prepared:** 7 November 2026  
**Status:** Provisional assistant-coded reference labels completed for 20 records. Independent model classification and human validation have not been completed. No agreement score is claimed.

## 1. Evidence corpus

The deployed discovery app reports 3,273 Groww app-review records and 27 source-linked public discussions. The 20-record evaluation sample is drawn from the 27 public discussions and is stored in `golden_set_20.csv`.

The app-review export has original review IDs but no verified individual Google Play review URLs in the downloaded source. The public discussions were selected because they retain direct source URLs. A source page confirms that text is visible at that URL; it does not independently verify the author's product or financial claims.

## 2. Sample selection

- 20 of 27 source-linked discussions selected.
- Purposive coverage sample, not random or statistically representative.
- Topics include positive experience, setup, step-up, pausing, payment, AutoPay, status/visibility, unit allocation and adjacent/general SIP questions.
- Source scope is retained. In particular, GS12 and GS15 are marked Adjacent SIP rather than treated as verified Groww-specific experiences.

## 3. Provisional reference coding

To meet the deadline, ChatGPT GPT-6 reviewed the raw text of all 20 selected records and populated the proposed classification fields in `golden_set_20.csv`.

**Important provenance distinction:** these are assistant-proposed labels, not annotations independently completed or approved by the project owner or a second human annotator. The CSV marks every row `ASSISTANT_PROPOSED_NOT_HUMAN_REVIEWED`. The `human_*` column names are retained for compatibility with the evaluation template, but the annotator field explicitly discloses the actual source of the labels. They must not be represented as user-verified ground truth.

### Label definitions

**Relevance**
- `Explicit SIP`: directly describes a SIP, instalment, mandate, setup/control or status.
- `Adjacent SIP`: general SIP or mutual-fund journey evidence without a clear Groww-specific experience.
- `Not relevant`: no meaningful SIP journey relevance.

**Journey stage:** one primary stage from Discover/Choose, Setup/Start, Pay/AutoPay, Manage/Pause/Cancel, Track/Status/Allocation, Change/Step-up, Withdraw/Sell, Other/Unclear.

**Sentiment:** Positive, Negative, Mixed, or Neutral/Question. A question alone is not automatically negative.

**Impact/workaround:** only what the author explicitly reports; no unstated causal inference.

### Provisional label distribution

- Relevance: 18 Explicit SIP; 2 Adjacent SIP; 0 Not relevant.
- Sentiment: 2 Positive; 12 Negative; 3 Mixed; 3 Neutral/Question.
- Journey stage: Setup/Start 2; Pay/AutoPay 3; Manage/Pause/Cancel 3; Track/Status/Allocation 7; Change/Step-up 4; Other/Unclear 1.

These are counts of the 20 selected records under assistant-proposed labels, not population estimates.

## 4. AI model evaluation status

The deployed Groq feature is a retrieval-grounded synthesis feature: it interprets the top five records retrieved for a user question. It is **not** currently a per-record classifier configured to label all 20 records using the same taxonomy.

No independent Groq classification run across all 20 records has been captured. Therefore:
- AI classification fields remain blank in the CSV.
- Exact-match agreement is **not measured**.
- No classifier accuracy or agreement percentage is claimed.
- The successful in-app Groq synthesis test demonstrates that the API integration works; it does not constitute a 20-record classification evaluation.

A valid next evaluation would require a fixed per-record classification prompt, model/version and date, raw structured outputs for all 20 records, then a comparison against independently human-reviewed labels. The assistant-proposed labels in this file are not independent human ground truth, so even that comparison should be described as exploratory unless a human annotator reviews/adjudicates them.

## 5. Actual AI output audit and corrections

The user-tested Groq synthesis for the question about AutoPay, missed instalments and payment failures produced hypotheses about payment options, debit priority and mandate status, citing retrieved evidence IDs R01–R05.

Audit note: the output should be phrased as reported experiences, not verified product facts. A few public comments cannot establish that a payment method is universally unavailable or that a feature gap is prevalent. The app's cited excerpts and counts should be checked before using the hypotheses in the deck. This is a cautionary review, not a fabricated record of a model correction. No 2–3 corrected/rejected per-record classifier outputs are claimed because no such evaluation run has been captured.

## 6. Limitations

- Small, purposive sample of 20 public discussions from 27; not representative.
- Self-selected, self-reported public comments; claims are unverified.
- Some dates are relative or indexed approximations.
- Adjacent/general SIP posts are not Groww-specific evidence.
- The records do not track the same investors over 12 months and cannot establish continuation, churn, prevalence, causality or retention impact.
- The 3,273 app-review records are keyword-screened candidates, not individually verified SIP-labelled records.
- Assistant-proposed labels require human review before they can be called a human-annotated Golden Set.

## 7. Deployed product

- Repository: https://github.com/Omi2456/groww-sip-discovery-engine
- Working branch: `ai-discovery-gemini`
- Live app: https://groww-sip-discovery-engine123.streamlit.app/
- AI provider: Groq; model configured in code: `openai/gpt-oss-20b`.
- Retrieval and theme counts are deterministic; Groq generates interpretation of retrieved excerpts.
- API credentials are stored in Streamlit secrets, not source code.

## 8. Recommended next steps

1. Have a human reviewer validate or correct the 20 proposed labels.
2. Implement or run a separate per-record Groq classifier with a fixed prompt and capture raw outputs.
3. Calculate field-wise agreement only after independent human labels and AI outputs both exist.
4. Complete genuine interviews and usability tests; record participant consent and actual observations. Do not substitute public comments or survey responses for interviews.
5. In the final deck, clearly separate desk-research signals, assistant-proposed coding, verified user research and unvalidated product hypotheses.
