# Enable Gemini-assisted discovery

The BM25 evidence search works without Gemini. Gemini adds an optional interpretation step over only the top five records already retrieved for the current question.

## Configure the key on Streamlit Community Cloud

1. Open the deployed app in Streamlit Community Cloud.
2. Open the app menu and choose Settings, then Secrets.
3. Add this TOML, replacing the placeholder with your Google AI Studio key:

```toml
GEMINI_API_KEY = "paste-your-key-here"
```

4. Save the secrets. Streamlit will restart the app.
5. Run a research question that returns evidence, then choose Analyze retrieved evidence with Gemini.

Do not paste the key into chat, source code, GitHub files, screenshots, or the evidence log. Do not commit a .env file. If the key has been exposed, revoke it in Google AI Studio and create a replacement.

## What is sent to Gemini

Only the current question and up to five BM25-retrieved excerpts, with their displayed evidence IDs and limited source metadata. Do not upload private interviews, account details, or sensitive personal information.

## Evidence safeguards

- Gemini may interpret only the retrieved excerpts; it must not invent counts or customer prevalence.
- The app filters returned citations to the evidence IDs supplied in that request.
- Counts remain calculated by deterministic app code.
- Opportunities are explicitly hypotheses, not validated solutions.
- Public reviews do not establish 12-month SIP continuation or causality.
- If Gemini is unavailable or no key is configured, deterministic search still works.

## Evaluation still required

Before presenting AI quality as proven, manually label a golden set, compare AI outputs with human labels, record agreement, and document examples where an AI output was corrected or rejected. Do not invent those results.