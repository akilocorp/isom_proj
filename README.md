<!-- @language Markdown -->
<!-- @updated 2026-11-19 -->
<!-- @changed Documented the retail exercise dashboard and submission files. -->

# ISOM Project

A retail dashboard for In-Class Exercise 5, completed from the supplied starter.
Enter a monthly sales target, select a region, and click Submit to see a summary.
Targets above 100000 also display the challenge message.

## Run locally

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Use these settings, then click **Deploy**:

- Repository: `akilocorp/isom_proj`
- Branch: `main`
- Main file path: `streamlit_app.py`

No secrets or additional settings are required.

`streamlit_app.py` mirrors `app.py` so the existing cloud entry point works.
For the course submission, fill in the student information in `app.py` and zip
only `app.py` and `requirements.txt` as `{StudentID}_InclassEx5.zip`.
