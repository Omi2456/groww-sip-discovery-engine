# Publish the Groww SIP Discovery Engine

This version runs without Ollama, a model download, API key, or paid AI endpoint.

## 1. Create a GitHub repository

On GitHub, create a repository named `groww-sip-discovery-engine`. Set it to **Public** so judges can view the app source and included evidence files. Do not initialize it with a README, license, or `.gitignore` because this folder already contains those project files.

## 2. Upload the project from PowerShell

Extract this ZIP to a folder such as `Desktop\Groww SIP Discovery Engine`. Open PowerShell and run the following, replacing `YOUR_GITHUB_USERNAME` with your GitHub username:

```powershell
$folder = Join-Path $env:USERPROFILE 'Desktop\Groww SIP Discovery Engine'
$repoUrl = 'https://github.com/YOUR_GITHUB_USERNAME/groww-sip-discovery-engine.git'
Set-Location -LiteralPath $folder
git init
git add .
git commit -m 'Publish Groww SIP Discovery Engine'
git branch -M main
git remote add origin $repoUrl
git push -u origin main
```

GitHub may ask you to sign in or authorize Git Credential Manager during the push.

## 3. Deploy on Streamlit Community Cloud

1. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) using the GitHub account that owns the repository.
2. Choose **Create app** and select `groww-sip-discovery-engine`.
3. Select branch `main` and set the app file path to `streamlit_app.py`.
4. Leave Secrets empty and deploy.
5. When deployment finishes, copy the generated `*.streamlit.app` URL. Test that link in a private/incognito window before submitting it.

Official instructions: [Deploy an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app). Community Cloud apps without traffic for 12 hours sleep; a judge can wake an app by visiting it. [App management](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app).

## 4. Judge-ready checks

- Try all six preset research questions.
- Confirm references open their public source where an individual source URL is available.
- Note that Groww review IDs are preserved, while their individual Play Store URLs are absent from the source dataset; those cards link to the general Groww listing.
- Try a CSV upload. A text column is required (`user_statement`, `content`, `text`, `review`, `review_text`, `body`, or `comment`).
- Confirm that the 12-month continuation question reports the evidence limitation rather than claiming that the reviews show investor retention.
