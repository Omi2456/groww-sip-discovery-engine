# Data provenance

## Included evidence

The application bundles 3,273 Groww app-review candidates and 27 source-linked public discussions (3,300 records in total).

The Groww review candidates were selected from the [Groww app reviews dataset on Hugging Face](https://huggingface.co/datasets/Avaneeshkarthik/groww-app-reviews) using the literal term “SIP”. They are keyword candidates, not individually verified SIP experiences. The source export contains original review IDs but does not provide verified individual Google Play review URLs.

The public-discussion pilot contains 27 source-linked records. Reddit discussions are self-selected and self-reported; the author's claims have not been independently verified.

## Repository data files

- `groww_sip_explicit_candidates.csv`: 3,273 Groww review candidates used by the app.
- `groww_sip_reddit_pilot.csv`: 27 public discussions with source IDs and direct URLs.
- `groww_sip_discovery_evidence.csv`: combined evidence table with stable evidence IDs and original source identifiers.
- `dataset_manifest.json`: corpus counts and provenance summary.
- `golden_set.csv`: fixed 20-record evaluation benchmark with preserved reference labels.

## Traceability

Reddit records retain direct discussion URLs. Groww review IDs are preserved, but individual Play Store review URLs were not supplied by the source dataset. The general Groww app listing must not be presented as a direct link to an individual review.

## Limitations

The corpus is a discovery input, not a representative sample of Groww customers. Public comments do not establish issue prevalence, causal drivers, or whether an investor maintained an active SIP 12 months after starting one. The dataset is not a longitudinal cohort.
