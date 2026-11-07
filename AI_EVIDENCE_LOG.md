# AI Evidence Log — Groww SIP Discovery Engine

**Working branch:** `ai-discovery-gemini`  
**Prepared:** 7 November 2026  
**Status:** Evidence inventory and Golden Set selection prepared; human annotation and AI evaluation are still pending.

## 1. Evidence corpus used

The deployed discovery app currently reports 3,273 Groww app-review records and 27 source-linked public discussions. The 27 discussions are stored in `groww_sip_reddit_pilot.csv`. This Golden Set is sampled from those 27 discussions only, as agreed with the project owner.

The larger Groww review export has original review IDs but no verified individual Google Play review URLs or app/package ID in the downloaded source file. For this evaluation, the source-linked public discussions are preferred because each selected record has a direct Reddit URL. A source page confirms that text is visible at that URL; it does not independently verify the user's financial or product claims.

## 2. Golden Set selection

- Selected: **20 of the 27** source-linked discussions.
- Selection is purposive/stratified for coverage, not random and not statistically representative.
- The selected records include positive experience, SIP setup/step-up, pause/skip/cancellation, AutoPay/mandate, payment failure, transaction/unit status, holding-format concerns, and adjacent/general SIP questions.
- The seven unselected records are not treated as invalid; they were excluded to keep this first evaluation set to 20 and reduce near-duplicate theme concentration.
- Full source text, URL, source ID, displayed date, subreddit, source scope and verification status are preserved in `golden_set_20.csv`.

## 3. Annotation protocol

Complete the `human_*` columns in `golden_set_20.csv` before running or viewing AI classifications. Use only what the feedback text says. Do not infer that a reported issue was caused by Groww or that it is common.

Suggested label definitions:

### Relevance
- `Explicit SIP`: directly describes a SIP, SIP instalment, SIP mandate, SIP setup/control, or SIP status.
- `Adjacent SIP`: related mutual-fund journey or general SIP question, but not clearly a Groww-specific SIP experience.
- `Not relevant`: no meaningful SIP/mutual-fund journey relevance.

### Journey stage
Use one primary stage: `Discover/Choose`, `Setup/Start`, `Pay/AutoPay`, `Manage/Pause/Cancel`, `Track/Status/Allocation`, `Change/Step-up`, `Withdraw/Sell`, or `Other/Unclear`.

### Primary theme
Use one concise, specific theme grounded in the text, e.g. `Mandate removal uncertainty`, `Step-up timing confusion`, `Payment failure`, `Transaction visibility mismatch`, `Unit allocation delay`, `Positive ease of use`. Avoid adding a cause not stated by the author.

### Sentiment
Use `Positive`, `Negative`, `Mixed`, or `Neutral/Question`. A question seeking help is not automatically proof of a negative product outcome.

### Impact/workaround
Record only an impact or workaround explicitly reported. If absent, write `Not stated`.

### Rationale
One short sentence explaining the labels with a direct link to the text. If uncertain, record uncertainty rather than forcing a precise label.

Set `human_annotator` to the actual person who reviewed the record and change `human_label_status` from `PENDING` to `REVIEWED` only after that person has checked the label. The current CSV intentionally leaves all human labels blank; no human annotation or agreement score is being claimed yet.

## 4. AI evaluation protocol

After all 20 human labels are reviewed:
1. Run the same fixed classification prompt/model configuration on each of the 20 raw feedback records independently.
2. Save the AI's raw structured output and model/date/prompt details in the `ai_*` columns or a linked evaluation log.
3. Compare AI labels against the human labels using exact-match agreement for relevance, journey stage, primary theme and sentiment. Theme labels should use a pre-agreed controlled vocabulary or adjudicated mapping before scoring.
4. Report each field's agreement separately: exact matches / 20. Also show a confusion table or list disagreements and why they differ.
5. Do not calculate an overall agreement percentage by mixing fields unless the method is explicitly defined.

**Current evaluation status:** Not run. AI agreement rate: **Not yet measured**. The app's Groq synthesis feature is not itself a 20-record classifier or a completed Golden Set evaluation.

## 5. Limitations

- The 20 records are a small, purposive sample from 27 public discussions, not a representative sample of Groww investors.
- Reddit authors are self-selected; the content is self-reported and claims are unverified.
- Some source dates are relative or indexed-date approximations; preserve the date as displayed rather than treating it as exact.
- Some records are general SIP category discussions, not direct Groww-specific experiences; their scope must remain visible.
- These records do not establish 12-month SIP continuation, churn, prevalence, causality, or retention impact.
- The existing app's 3,273 Groww review records are keyword-screened candidates, not individually source-verified SIP labels.

## 6. Actual AI corrections/rejections

No AI output has yet been independently audited against this 20-record Golden Set. Do not claim 2–3 corrected/rejected outputs until actual model outputs are captured, checked against the cited source text, and the correction rationale is recorded here.

## 7. Existing deployed engine

- Repository: https://github.com/Omi2456/groww-sip-discovery-engine
- Live app: https://groww-sip-discovery-engine123.streamlit.app/
- AI provider: Groq (the app's optional synthesis step analyzes the top retrieved excerpts).
- Retrieval and theme counts are deterministic; AI synthesis is a separate interpretation layer.
