# AI Evidence Log — Groww SIP Discovery Engine

## Purpose

This log documents how the AI-assisted discovery workflow was evaluated against a 20-example labelled benchmark, what the model returned, where it failed or disagreed with the reference labels, and what those findings mean for the product.

This is a project evidence record, not a claim of production-grade model accuracy.

## 1. Golden set

- Benchmark size: 20 examples.
- Source: public online discussions included in the project corpus.
- Reference dimensions: relevance, journey stage, primary theme, and sentiment.
- The full benchmark and reference labels are maintained in [`golden_set.csv`](./golden_set.csv).
- Annotation provenance: the project owner reports that a friend reviewed the 20 proposed labels and said they were correct. The reviewer’s identity is withheld. The original labels were first proposed by ChatGPT. This review was not independently witnessed or audited, and it is not a formal expert annotation or inter-rater reliability exercise.
- The reference labels should therefore be treated as project reference labels, not independently validated ground truth.

The corpus and source limitations are documented in [`DATA_PROVENANCE.md`](./DATA_PROVENANCE.md) and [`AI_EVALUATION.md`](./AI_EVALUATION.md).

## 2. Evaluation run and agreement

The submitted evaluation export contains 20 attempted records:

| Result | Records |
|---|---:|
| Successful model responses | 14 |
| Failed model responses | 6 |
| Total attempted | 20 |

Exact agreement is calculated only across the 14 records with successful, parseable model responses. Failed records are excluded from each agreement denominator and are reported separately.

| Dimension | Exact matches | Successful denominator | Exact agreement |
|---|---:|---:|---:|
| Relevance | 13 | 14 | 92.9% |
| Journey stage | 10 | 14 | 71.4% |
| Primary theme | 1 | 14 | 7.1% |
| Sentiment | 11 | 14 | 78.6% |

These are results from one evaluation run on this benchmark. They are not a stable estimate of general model accuracy. Exact string matching is especially restrictive for primary themes because the model often uses semantically related wording that differs from the reference label. The low exact-match result must still be disclosed; it should not be presented as a high theme-classification score.

## 3. Failed outputs

Six records failed to produce a complete, parseable JSON response after the configured attempts:

| Record | Observed failure |
|---|---|
| GS10 | No JSON object found in model response |
| GS11 | No JSON object found in model response |
| GS12 | Model response did not contain a complete JSON object |
| GS14 | Model response did not contain a complete JSON object |
| GS17 | No JSON object found in model response |
| GS20 | No JSON object found in model response |

These are output-format / parsing failures, not successful classifications. They are not counted as correct or incorrect predictions in the agreement calculations. Their presence indicates that structured-output reliability remains a limitation of the current workflow.

## 4. Human-reviewed disagreement and correction examples

The examples below document how a reviewer should correct or interpret the model output against the supplied reference labels. They are human-review examples from this evaluation export; they do not imply that the model automatically learned from the correction or that a retraining cycle was completed.

### Example A — GS03: Pause and penalty uncertainty

- User feedback: the person expects expenses to rise and asks how to pause a SIP and whether a penalty applies.
- AI primary theme: `Pause SIP`.
- Reference primary theme: `Pause and penalty uncertainty`.
- Disagreement: the AI captured the requested action but its theme wording did not capture the penalty concern.
- Human-reviewed correction: retain the more complete theme, `Pause and penalty uncertainty`.
- Learning: theme extraction should preserve both the user's intended action and the uncertainty or consequence motivating the question.

### Example B — GS13: Allocated units missing from dashboard

- User feedback: the person says units were allotted but are not reflected in the Groww dashboard.
- AI journey stage: `Setup/Start`.
- Reference journey stage: `Track/Status/Allocation`.
- Disagreement: the AI placed a post-allocation visibility issue in the initial setup stage.
- Human-reviewed correction: `Track/Status/Allocation`.
- Learning: journey-stage classification must distinguish starting an SIP from tracking an already-processed investment.

### Example C — GS15: General question about skipping an SIP instalment

- User feedback: a new investor asks what happens if an SIP payment is skipped; the discussion does not describe a specific Groww experience.
- AI relevance: `Explicit SIP`; AI journey stage: `Discover/Choose`.
- Reference relevance: `Adjacent SIP`; reference journey stage: `Other/Unclear`.
- Disagreement: the AI recognised the SIP topic but overstated the connection to a specific Groww experience and assigned a more specific journey stage than the feedback supports.
- Human-reviewed correction: `Adjacent SIP` and `Other/Unclear`.
- Learning: the engine should distinguish general category-level questions from platform-specific feedback and avoid assigning a precise journey stage when the evidence does not support one.

## 5. What the evaluation tells us

1. The model performed best on relevance in this run (13/14 exact matches), but one general SIP question was incorrectly treated as explicit Groww feedback.
2. Journey-stage classification was less consistent (10/14 exact matches), including a post-allocation issue incorrectly labelled as setup.
3. Primary-theme exact agreement was weak (1/14). The current theme output is not sufficiently consistent with the reference taxonomy.
4. Sentiment agreement was 11/14. Neutral questions and mixed experiences need careful interpretation.
5. Six of 20 attempted records failed at the structured-output stage. The workflow needs stronger output reliability before it can be treated as dependable at scale.

## 6. Limitations and next steps

- The benchmark is small (20 examples) and drawn from public, self-selected discussions; it is not representative of all Groww users.
- The reference labels have project-owner-reported friend review, not independent expert validation.
- Results reflect one run and may vary across runs or model responses.
- Exact-match scoring does not capture semantic similarity. Any future taxonomy-normalised or adjudicated scoring must be reported separately from the exact-match figures above.
- Failed outputs remain failures and must not be silently removed from the reported completion rate.
- The three correction examples are documented human-review corrections; no claim is made that these corrections were used for model fine-tuning.

## 7. Supporting project files

- [Golden set and reference labels](./golden_set.csv)
- [AI evaluation methodology and run notes](./AI_EVALUATION.md)
- [Data provenance](./DATA_PROVENANCE.md)
- [Evaluation implementation](./golden_set_evaluation.py)

---
*Prepared from the 20-record evaluation export supplied for this project. Metrics and failure IDs above describe that specific export.*
