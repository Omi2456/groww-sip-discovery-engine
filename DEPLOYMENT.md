# Deployment

## Current application configuration

- Platform: Streamlit Community Cloud
- Repository: `Omi2456/groww-sip-discovery-engine`
- Branch: `ai-discovery-gemini`
- Entrypoint: `streamlit_app.py`
- Python test workflow: Python 3.11

The live application URL is https://groww-sip-discovery-engine123.streamlit.app/. A repository commit does not by itself confirm that Community Cloud has completed deployment.

## Verify an update

1. Commit changes to `ai-discovery-gemini`.
2. Confirm the Streamlit app uses that branch and `streamlit_app.py`.
3. Wait for deployment to complete.
4. Test research retrieval, AI interpretation, automatic Golden Set loading and the separate custom-upload workspace.

Configure `GROQ_API_KEY` only in Streamlit Community Cloud Secrets. Never store credentials in the repository.

See the [Streamlit Community Cloud deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app).
