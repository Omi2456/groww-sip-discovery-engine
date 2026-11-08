# AI Evidence Log — Groww SIP Discovery Engine

**Prepared:** 8 November 2026  
**Repository:** https://github.com/Omi2456/groww-sip-discovery-engine  
**Branch:** `ai-discovery-gemini`  
**Live Discovery Engine:** https://groww-sip-discovery-engine123.streamlit.app/

## 1. Project purpose

The Discovery Engine supports product discovery for Groww's SIP-retention challenge: understand customer-reported friction that may affect whether first-time mutual-fund SIP investors continue. The business outcome is an active SIP 12 months after first SIP start, defined as at least one successful instalment in the last 30 days.

## 2. Sources and volume

The bundled discovery corpus contains 3,300 records:
- **3,273 Groww app-review candidates** containing the literal term “SIP”, extracted from a larger 322,726-row Hugging Face export.
- **27 source-linked public discussions**, primarily Reddit.

Links:
- Original dataset: https://huggingface.co/datasets/Avaneeshkarthik/groww-app-reviews
- Manifest: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/dataset_manifest.json
- Groww candidates: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_explicit_candidates.csv
- Public discussions: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_reddit_pilot.csv
- Combined evidence: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/groww_sip_discovery_evidence.csv
- Dataset assessment: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/DATASET_ASSESSMENT.md
- Public discussion assessment: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/PUBLIC_DISCUSSION_ASSESSMENT.md

**Limitations:** The 3,273 records are keyword candidates, not individually verified SIP experiences. Their source export has original IDs but no verified individual Google Play review URLs. Reddit posts are self-selected, self-reported and do not establish prevalence or causality.

## 3. Research questions available in the app

The app contains these six preset questions. They are documented as available prompts; not all are claimed to have been executed.

1. “What reasons do Groww reviewers give for pausing, reducing, or stopping an SIP?”
2. “What problems do reviewers report with AutoPay, mandates, or SIP debits?”
3. “What do reviewers say when their SIP payment, order status, or mutual fund units are unclear?”
4. “What do users do outside Groww when they’re unsure whether an SIP payment went through?”
5. “Are there positive SIP experiences that differ from the problem reports?”
6. “Can these reviews tell us what separates investors with an active SIP after 12 months from those who stop?”

The sixth prompt is a data-gap check. Public reviews do not follow the same investors over time and cannot establish who remained active after 12 months.

## 4. Recorded Groq interaction

**Interaction 01 — AutoPay, missed instalments and payment failures**

- Question entered: “What problems do investors experience with SIP AutoPay, missed instalments and payment failures?”
- User-shared app result: five evidence examples retrieved (one public discussion, four Groww app reviews).
- Deterministic theme counts shown: AutoPay/mandate 5 of 5; payment/debit 3 of 5; pausing/cancellation 1 of 5.
- Groq synthesis identified reported issues around AutoPay options, debit-priority confusion and mandate-status uncertainty, and proposed related opportunity hypotheses.
- Critical review: these examples must be described as individual reported experiences, not verified product-wide limitations or prevalence. Feature suggestions remain hypotheses pending product verification and user validation.

The complete raw JSON transcript was not archived; this is a summary of the actual test output shared by the project owner, not a verbatim transcript.

## 5. AI configuration and safeguards

- Provider: Groq
- Model: `openai/gpt-oss-20b`
- API base: `https://api.groq.com/openai/v1`
- SDK: OpenAI-compatible Python SDK
- Secret: `GROQ_API_KEY`, stored in Streamlit secrets
- Discovery synthesis sees at most the top five retrieved excerpts.
- The synthesis prompt instructs the model not to invent counts, prevalence, causes, capabilities or retention outcomes, and validates cited evidence IDs against the supplied set.
- Retrieval and theme counts are deterministic; Groq generates interpretation.

## 6. Golden Set and reference-label review

**Golden Set:** https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/golden_set_20.csv

Twenty records were purposively selected from the 27 public discussions for topic coverage. This is not a random or representative sample.

The CSV contains source text, source URL, source scope, and proposed relevance, journey-stage, theme, sentiment, impact and rationale labels.

**Human-review provenance:** The project owner reports that a friend reviewed the 20 proposed labels and said they were correct. The reviewer’s identity is withheld. This log records that as a project-owner-reported review; the review itself has not been independently witnessed or audited by the system. The original labels were first proposed by ChatGPT. The CSV marks the status as `FRIEND_REVIEWED_REPORTED_BY_PROJECT_OWNER`, not as a formal external audit.

Label definitions:
- Relevance: Explicit SIP; Adjacent SIP; Not relevant.
- Journey stage: Discover/Choose; Setup/Start; Pay/AutoPay; Manage/Pause/Cancel; Track/Status/Allocation; Change/Step-up; Withdraw/Sell; Other/Unclear.
- Sentiment: Positive; Negative; Mixed; Neutral/Question.

## 7. Groq per-record classification and agreement

A separate Golden Set evaluation section now appears immediately after the Research Workspace. It automatically loads the bundled 20-record CSV, sends each record individually to the configured model, retains per-record raw AI responses, supports retrying failed records during the active Streamlit session, calculates field-wise exact-match agreement against the preserved reference labels, and provides a downloadable results CSV.

**Execution status:** The evaluator runs on demand in the deployed app. No evaluation result or agreement rate is claimed in this documentation until a user executes it and downloads the resulting file. The app displays live progress and the actual completed/failed counts.

To execute once:
1. Open the live Discovery Engine.
2. Open the “Golden Set evaluation” section directly below the research workspace.
3. Click “Run / resume evaluation”.
4. Download `groww_sip_ai_evaluation_results.csv`.

The evaluator uses the existing Streamlit secret `GROQ_API_KEY`; it does not display the key. Groq free-tier rate limits may apply. The AI result file must be retained as evidence.

The app calculates exact-match agreement separately for relevance, journey stage, primary theme and sentiment, with a visible denominator and mismatch list. Primary-theme agreement is literal text matching, so semantically similar wording can count as a mismatch. No combined accuracy score is presented.

## 8. Three AI output corrections / rejections

One actual Groq synthesis interaction has been reviewed. Three distinct audit observations can be drawn from that same output, but they are not three separate model runs:

1. **AutoPay capability generalisation:** qualify any implication that a payment method is universally unavailable. The retrieved comments establish reported experiences, not current product-wide capability.
2. **Debit priority as a feature request:** retain as an unvalidated opportunity hypothesis, not established demand.
3. **Mandate changes as a solution:** do not recommend implementation until current product behaviour and investor demand are verified.

These are three separate review decisions about one captured synthesis, not three independently captured model failures. No other raw AI outputs are claimed. To satisfy a strict requirement for three separately captured corrections, run and save three additional distinct research-question outputs and record a real correction only where the output warrants it.

## 9. What the evidence can and cannot establish

Can support discovery of reported friction themes, evidence retrieval, hypothesis generation and identification of research gaps.

Cannot establish issue prevalence, causality, 12-month continuation, churn drivers or that a proposed feature will improve retention. Public comments are not a longitudinal cohort.

## 10. Product information architecture

The app is organized into three distinct capabilities:

1. **Research Workspace** — primary entry point for evidence search, discovery brief, source references and AI-assisted interpretation.
2. **Golden Set evaluation** — fixed, bundled 20-record benchmark immediately after the research workspace. It does not accept uploads or modify reference labels. Progress and results are held in Streamlit session state; a downloaded CSV preserves the raw outputs for audit. If the app session is restarted, rerun the records that were not exported; session progress is not a permanent server-side job store.
3. **Advanced: Explore your own feedback** — optional CSV upload and custom-only retrieval. Uploaded rows are never added to the bundled research corpus or Golden Set.

Provider/model/API details remain in this technical evidence log and source documentation, not in the primary interface.

## 11. Next actions

1. Run the new Golden Set evaluator in the live app and save its CSV output.
2. Review field-wise agreement and disagreements against the friend-reviewed reference labels; retain the reviewer provenance as project-owner-reported.
3. Capture three distinct AI interactions and document any actual corrections/rejections. If an output is sound, do not invent a correction.
4. Keep survey/interview findings from the separate primary research distinct from public desk-research signals.

## 12. Project links

- Live Discovery Engine: https://groww-sip-discovery-engine123.streamlit.app/
- Repository: https://github.com/Omi2456/groww-sip-discovery-engine
- Golden Set: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/golden_set_20.csv
- Dataset manifest: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/dataset_manifest.json
- AI Evidence Log: https://github.com/Omi2456/groww-sip-discovery-engine/blob/ai-discovery-gemini/AI_EVIDENCE_LOG.md
