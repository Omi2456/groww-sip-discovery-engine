# AI provider setup

The app uses deterministic BM25 retrieval for evidence discovery. Groq provides optional AI-assisted interpretation and Golden Set classification.

## Configure Streamlit Community Cloud

1. Open the deployed app in Streamlit Community Cloud.
2. Open app settings and select Secrets.
3. Add `GROQ_API_KEY = "your-key"` using your own Groq Console key.
4. Save the setting and allow the app to restart.

Never paste the key into chat, screenshots, source code or GitHub. Never commit credentials or a `.env` file.

## Request scope

Research synthesis sends the current research question and up to five retrieved excerpts to Groq. The model is instructed to use only supplied evidence and cite only supplied evidence IDs. Counts are calculated by application code. Opportunities are hypotheses, not validated solutions.

The fixed benchmark is separate from custom feedback uploads. Public feedback is self-selected and does not establish prevalence, causality or 12-month SIP retention.
