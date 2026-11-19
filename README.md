<!-- @language Markdown -->
<!-- @updated 2026-11-19 -->
<!-- @changed Added local setup and Streamlit Community Cloud deployment instructions. -->

# ISOM Project

A simple Streamlit app with a personalized greeting and an interactive chart.

## Run locally

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Use these settings, then click **Deploy**:

- Repository: `akilocorp/isom_proj`
- Branch: `main`
- Main file path: `streamlit_app.py`

No secrets or additional settings are required.
