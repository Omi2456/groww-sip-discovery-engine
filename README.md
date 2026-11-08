# Groww SIP Discovery Engine

An evidence-first discovery tool for exploring customer feedback about Groww SIP experiences. The app retrieves relevant review and public-discussion records, shows source references and recurring signals, and frames a possible opportunity as a hypothesis to investigate.

## Try the live app

The app is deployed on Streamlit Community Cloud from the `ai-discovery-gemini` branch with `streamlit_app.py` as its entrypoint. Evidence retrieval works without an API key; AI interpretation and Golden Set evaluation use the configured API secret. See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment steps.

## What the engine does

- Research Workspace searches the bundled Groww review subset and source-linked public discussions.
- Displays matching evidence with R01-style reference numbers and source details.
- Summarizes recurring themes within retrieved examples. Counts describe the selected records, not the entire customer population.
- Provides six preset research questions covering SIP pauses/stops, AutoPay and debits, payment or unit status, off-app behavior, positive versus problem reports, and 12-month continuation.
- Compares high- and low-rated SIP-related reviews for the positive-experience question. Star ratings are only a rough proxy for review sentiment.
- Flags 12-month retention as a data gap: the included reviews do not follow the same investors over time.
- Suggests an opportunity to investigate, clearly marked as an unvalidated hypothesis.

The search uses BM25 lexical ranking with SIP terminology expansion. AI-assisted interpretation analyzes only the top retrieved excerpts, validates returned evidence IDs against the displayed records, and labels opportunities as hypotheses. Deterministic search remains available if Groq is not configured or unavailable. Unsupported questions receive a no-match response.

## Evidence and provenance

The app uses **3,273 SIP-related Groww review records** and **27 source-linked public discussions**. It does not use all ~323K reviews in the original source dataset.

- [Original Groww app reviews dataset on Hugging Face](https://huggingface.co/datasets/Avaneeshkarthik/groww-app-reviews)
- `groww_sip_explicit_candidates.csv`: review subset loaded by the app, with original review IDs and available metadata.
- `groww_sip_reddit_pilot.csv`: public discussions loaded by the app, with source IDs and direct URLs.
- `groww_sip_discovery_evidence.csv`: combined, structured evidence table with stable evidence IDs and original IDs preserved.
- `dataset_manifest.json` and `DATA_PROVENANCE.md`: counts, fields, and traceability notes.

Reddit references link to original discussions. Groww review IDs are preserved, but the source dataset does not provide verified individual Play Store review URLs; the app links to the general Groww listing and identifies it as such.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The deterministic evidence search works without a key. To enable AI-assisted interpretation and Golden Set evaluation, add GROQ_API_KEY to Streamlit Community Cloud app Settings → Secrets. Use TOML such as GROQ_API_KEY = YOUR_KEY in quotes. Never commit the key to GitHub. The app sends only the top retrieved excerpts for the current question to Groq; do not upload private or sensitive interview data.

## Advanced: Explore your own feedback

The optional custom-feedback workspace accepts CSV files up to 20 MB and indexes up to 5,000 non-empty rows per upload. This dataset is explored separately and is never merged into the fixed Golden Set. A text column is required: `user_statement`, `content`, `text`, `review`, `review_text`, `body`, or `comment`. Optional columns include an ID, source URL, source/platform, and date. Uploads remain in the app session.
