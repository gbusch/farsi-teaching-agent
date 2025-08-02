# Farsi Learning Assistant

## Configure Google Auth
You need to register a Google Auth App and set the parameters in `app/.streamlit/secrets.toml`:
https://docs.streamlit.io/develop/tutorials/authentication/google

## Externalized config in Google Storage
Create a GCP storage with the following files:
- `admin/allowed_users.txt`: Email-adresses of allowed users (one row per user)
- `sentences/<name of unit>.txt`: Files with sentences that users should translate (one row per sentence).

## Start local app
You need a Gemini API key. Start streamlit locally with:
```
GEMINI_API_KEY="<your key>" streamlit run app/app.py
```

## Deploy app
Deploy to Google Cloud Run with the commands from `deploy.sh`. You need to source the variables from the `.env` file.
