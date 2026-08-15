# Streamlit résumé demo

This repository now includes a lightweight public-facing Streamlit dashboard while preserving the original application architecture.

## Run locally

```powershell
py -m pip install -r requirements-streamlit.txt
py -m streamlit run streamlit_app.py
```

Open the URL Streamlit prints, normally `http://localhost:8501`.

## Deploy for a résumé link

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from that repository.
3. Set the app entry point to `streamlit_app.py`.
4. If the deployment interface expects `requirements.txt`, either select/use `requirements-streamlit.txt` if supported or copy its two dependencies into the deployment requirements file.
5. Deploy and use the resulting `*.streamlit.app` URL as the Live Demo link on your résumé.

The Streamlit page is intentionally self-contained. It does not require database, Gemini, or GCP credentials to render the public portfolio demo. The original production-style code remains available in the repository for technical review.
