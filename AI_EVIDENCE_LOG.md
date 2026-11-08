# AI Evidence Log — Groww SIP Discovery Engine

**Prepared:** 8 November 2026  
**Repository:** https://github.com/Omi2456/groww-sip-discovery-engine  
**Branch:** `ai-discovery-gemini`  
**Live Discovery Engine:** https://groww-sip-discovery-engine123.streamlit.app/  
**Status:** Discovery workflow and one Groq synthesis test documented. Golden Set contains 20 assistant-proposed reference labels; independent human validation and per-record AI classification have not been completed. Agreement is not measured.

> **Scope and integrity note:** This log distinguishes (a) functionality verified in the code, (b) prompts available in the deployed app, (c) the one user-reported Groq test whose output was shared in the project conversation, and (d) evaluation work that remains incomplete. It does not claim that every preset prompt was executed or that an AI accuracy score was measured.

## 1. Project purpose and AI role

The Discovery Engine supports product discovery for Groww's SIP-retention challenge: understand customer-reported friction that may affect whether first-time mutual-fund SIP investors continue. The business outcome of interest is an active SIP 12 months after the first SIP starts, where active means at least one successful instalment in the last 30 days.

The application combines:
- Deterministic BM25 retrieval and query expansion to find relevant feedback.
- Deterministic theme-counting over the retrieved records.
- Optional Groq-assisted synthesis that interprets only the top five retrieved excerpts for the current question.

Groq does not search the entire corpus directly, independently validate customer claims, calculate the displayed theme counts, or establish 12-month retention outcomes.

## 2. Data sources, volume and provenance

The deployed app's bundled corpus contains **3,300 records**:

| Source | Records | How used | Traceability |
|---|---:|---|---|
| Groww app-review candidate subset | 3,273 | Keyword-screened records containing the literal term “SIP” | Original review IDs retained; no verified individual Google Play review URLs in the downloaded source |
| Public discussions | 27 | Source-linked Reddit discussions | Direct Reddit URLs retained |
| **Total** | **3,300** | Discovery corpus | See manifest and CSVs |

### Source links
- Original Groww reviews dataset: https://huggingface.co/datasets/Avaneeshkarthik/groww-app-reviews
- Dataset manifest: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/dataset_manifest.json
- Groww review candidates: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_explicit_candidates.csv
- Public discussions: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_reddit_pilot.csv
- Combined evidence export: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_discovery_evidence.csv
- Dataset assessment: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/DATASET_ASSESSMENT.md
- Public discussion assessment: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/PUBLIC_DISCUSSION_ASSESSMENT.md

### Important dataset limitations

The source Hugw Face export contained 322,726 raw reviews dated 28 September 2020 to 26 September 2025. The app uses 3,273 records containing “SIP”; these are keyword candidates, not individually human-verified SIP experiences. The export contains review IDs but no per-review Google Play URL or app/package ID field. The 27 Reddit URLs lead to public discussion pages, but author claims are self-reported and not independently verified. The public discussion corpus is self-selected and not representative of Groww investors.

## 3. Discovery questions available in the app

The deployed application contains six preset research questions. These are the prompts offered by the interface; this log does not claim all six were executed.

1. **Pausing/reducing/stopping:** “What reasons do Groww reviewers give for pausing, reducing, or stopping an SIP?”
2. **AutoPay and mandates:** “What problems do reviewers report with AutoPay, mandates, or SIP debits?”
3. **Payment and allocation status:** “What do reviewers say when their SIP payment, order status, or mutual fund units are unclear?”
4. **Off-platform behaviour:** “What do users do outside Groww when they’re unsure whether an SIP payment went through?”
5. **Positive counterexamples:** “Are there positive SIP experiences that differ from the problem reports?”
6. **12-month retention data gap:** “Can these reviews tell us what separates investors with an active SIP after 12 months from those who stop?”

The sixth prompt is intentionally framed as a data-gap check. The app warns that public reviews do not follow the same investors over time and cannot establish who remained active after 12 months.

## 4. Recorded Groq interaction

### Interaction 01 — AutoPay, missed instalments and payment failures

**Execution status:** User ran this question in the deployed app and shared the resulting output in the project conversation.

**Question entered:**
“What problems do investors experience with SIP AutoPay, missed instalments and payment failures?”

**Retrieval shown by the app:**
- 5 evidence examples retrieved.
- 1 public discussion and 4 Groww app reviews.
- Theme counts within those five retrieved examples: AutoPay/mandate 5 of 5; payment/debit 3 of 5; pausing/cancellation 1 of 5.
- Representative feedback included a request for easier manual SIP transaction / e-mandate options.

**Groq output as reported from the user's app test:**
- Described limited AutoPay options as a possible friction point.
- Described debit-priority confusion as another possible friction point.
- Described mandate-status and pause/delete uncertainty.
- Suggested hypotheses around mandate options, debit priority, and clearer mandate status/control.
- Included evidence references R01–R05 and limitations.

**Interpretation and decision:**
Treat these as reported experiences and hypotheses, not verified statements about Groww's current product capabilities or the prevalence of a problem. The five retrieved examples are a small, query-selected subset. Before prioritising a proposed feature, verify current product behaviour and validate the need with investors.

**Evidence status:** The user shared a screenshot of the deployed app showing Groq-generated synthesis, and separately pasted the retrieval counts and a summary of the response. The complete raw JSON response was not archived in this repository. Therefore, this is a documented interaction summary, not a verbatim full model transcript.

## 5. AI configuration and safeguards

- Provider: Groq
- Model configured in code: `openai/gpt-oss-20b`
- API base URL: `https://api.groq.com/openai/v1`
- SDK: OpenAI-compatible Python SDK
- Secret name: `GROQ_API_KEY`, stored in Streamlit secrets
- Retrieved context passed to Groq: at most five excerpts for the current question
- Response format: JSON object
- Maximum completion tokens configured: 900
- Request timeout: 25 seconds; one retry configured

The prompt instructs the model to use only supplied excerpts, not invent counts, prevalence, causes, product capabilities or retention outcomes, cite only evidence IDs supplied by the app, state limitations, and frame opportunities as hypotheses. Returned evidence IDs are filtered against the IDs provided to the model.

## 6. Golden Set: selection and provisional coding

**Golden Set file:** https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/golden_set_20.csv

Twenty records were purposively selected from the 27 source-linked public discussions to cover positive experiences, setup, step-up, pausing, AutoPay, payment failures, status visibility, allocation and adjacent/general SIP questions. The selection is for qualitative coverage, not random sampling or statistical representation.

The CSV includes the original source ID, URL, displayed date, subreddit, source scope, source-verification note and full feedback text. It also includes proposed labels for relevance, journey stage, theme, sentiment, impact/workaround and rationale.

### Label definitions

- **Relevance:** Explicit SIP; Adjacent SIP; Not relevant.
- **Journey stage:** Discover/Choose; Setup/Start; Pay/AutoPay; Manage/Pause/Cancel; Track/Status/Allocation; Change/Step-up; Withdraw/Sell; Other/Unclear.
- **Sentiment:** Positive; Negative; Mixed; Neutral/Question.
- **Impact/workaround:** only what the author explicitly reported; otherwise state that it was not stated.
- **Rationale:** concise explanation grounded in the record.

### Annotation provenance

The 20 labels were proposed by ChatGPT GPT-6 after reviewing the source text. They were **not independently hand-labelled or approved by the project owner**. Every row is explicitly marked `ASSISTANT_PROPOSED_NOT_HUMAN_REVIEWED`; the annotator field identifies ChatGPT. These labels are provisional reference coding, not validated human ground truth.

### Provisional distributions

Under the assistant-proposed labels:
- Relevance: 18 Explicit SIP; 2 Adjacent SIP.
- Sentiment: 2 Positive; 12 Negative; 3 Mixed; 3 Neutral/Question.
- Journey stage: Setup/Start 2; Pay/AutoPay 3; Manage/Pause/Cancel 3; Track/Status/Allocation 7; Change/Step-up 4; Other/Unclear 1.

These counts describe only the selected 20 records and are not market estimates.

## 7. AI agreement evaluation

**Status: Not completed. No agreement score is available.**

The deployed Groq feature performs retrieval-grounded synthesis of up to five records for a research question. It is not currently a per-record classifier that returns the same relevance, journey-stage, theme and sentiment labels for all 20 Golden Set records.

The `ai_*` fields in the Golden Set are intentionally blank. No exact-match agreement, classifier accuracy, or overall score is claimed.

A valid evaluation would require:
1. Independent human review/adjudication of the 20 reference labels.
2. A fixed per-record classification prompt and model configuration.
3. Captured raw AI output for each of the 20 records.
4. Field-wise comparison for relevance, journey stage, theme and sentiment.
5. Disagreement review and a documented calculation method.

Because the current reference labels are assistant-proposed and unreviewed, even a future model comparison against them should be described as exploratory until an independent human reviewer validates the labels.

## 8. AI output audit: correction and rejection principles

The recorded AutoPay interaction supports the following audit observations. These are **three review decisions about the same recorded synthesis**, not three separate model runs or three independently captured model failures.

| AI interpretation / risk | Human-review decision | Reason |
|---|---|---|
| A few comments may imply that certain AutoPay options are unavailable generally | Qualify as “some users reported difficulty/options limitations” | A small set of comments cannot verify current product-wide capability or prevalence |
| Debit-priority behaviour was proposed as a product opportunity | Retain only as an unvalidated hypothesis | The evidence shows a reported preference/concern, not validated demand or feasibility |
| New mandate options were suggested as a solution | Do not treat as a recommendation ready for prioritisation | Existing product behaviour must first be checked and investor demand validated |

These observations demonstrate critical review of the shared synthesis. They should not be presented as three separate corrected outputs. No other raw model outputs were supplied or archived, so additional correction examples are not fabricated.

## 9. What the evidence can and cannot establish

**Can support:**
- Discovery of customer-reported friction themes.
- Retrieval of source-linked public discussion examples.
- Hypothesis generation for interviews and product exploration.
- Identification of information gaps in the available dataset.

**Cannot establish:**
- How common an issue is among all Groww investors.
- That a reported issue was caused by Groww.
- That a proposed feature will improve SIP retention.
- Which users remained active after 12 months.
- Causal drivers of churn or long-term retention.

The 20-record Reddit sample is small and purposive. The 3,273 Groww review candidates are keyword-filtered, not semantically validated. Public posts are self-selected and self-reported.

## 10. Key learnings and next steps

1. AI synthesis is useful for organising retrieved feedback and generating hypotheses, but source-level checking is essential.
2. A cited evidence ID improves traceability but does not independently prove the claim.
3. Deterministic retrieval/counting should be distinguished from generative AI interpretation.
4. A Golden Set requires independent human reference labels and actual model outputs before agreement can be reported.
5. Retention measurement requires a longitudinal cohort with SIP start date and subsequent active/paused/stopped status, supplemented by qualitative interviews.

## 11. Project links

- Live Discovery Engine: https://groww-sip-discovery-engine123.streamlit.app/
- GitHub repository: https://github.com/Omi2456/groww-sip-discovery-engine
- Working branch: `ai-discovery-gemini`
- Dataset manifest: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/dataset_manifest.json
- Groww review candidate CSV: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_explicit_candidates.csv
- Reddit pilot CSV: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_reddit_pilot.csv
- Combined evidence CSV: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_discovery_evidence.csv
- Golden Set CSV: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/golden_set_20.csv
- Dataset assessment: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/DATASET_ASSESSMENT.md
- Public discussion assessment: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/PUBLIC_DISCUSSION_ASSESSMENT.md

**Submission note:** This log documents the AI-assisted discovery workflow and its current evidence status. It does not claim a completed human-vs-AI accuracy evaluation. If the rubric requires a measured agreement rate and two or three separately captured corrections, those items remain outstanding and should not be marked complete until the underlying records exist.
