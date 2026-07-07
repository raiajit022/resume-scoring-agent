# 🤖 Resume Scoring Agent

A web application built on top of [HackerRank's hiring-agent](https://github.com/interviewstreet/hiring-agent) that lets you **upload a PDF resume** and get an AI-powered score enriched with GitHub signals.

---

## 🚀 Features

- Upload any PDF resume via a clean web UI
- Automatically detects GitHub username from the resume
- Fetches GitHub repos and enriches the evaluation
- Scores across: Open Source, Self Projects, Production, Technical Skills
- Shows bonus points, deductions, evidence, and a summary
- Fully local with Ollama OR cloud with Google Gemini

---

## 🛠️ Quick Setup

### 1. Clone this repo

```bash
git clone https://github.com/raiajit022/resume-scoring-agent.git
cd resume-scoring-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set one of:

**Option A — Google Gemini (Recommended for beginners)**
```
LLM_PROVIDER=gemini
DEFAULT_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your_api_key_here
```
Get your free API key at: https://aistudio.google.com/api-keys

**Option B — Ollama (Fully Local)**
```
LLM_PROVIDER=ollama
DEFAULT_MODEL=gemma3:4b
```
Install Ollama from https://ollama.com then run:
```bash
ollama pull gemma3:4b
ollama serve
```

### 5. Run the web app

```bash
uvicorn app:app --reload --port 8000
```

### 6. Open in browser

Go to: **http://localhost:8000**

Upload a PDF resume and click **Analyze Resume**!

---

## 📁 Project Structure

```
.
├── app.py                  ← FastAPI web server (NEW)
├── score.py                ← Orchestrates the pipeline
├── pdf.py                  ← PDF → structured JSON
├── github.py               ← GitHub profile enrichment
├── evaluator.py            ← LLM-based scoring
├── models.py               ← Pydantic schemas + LLM providers
├── llm_utils.py            ← Provider init
├── transform.py            ← JSON normalization
├── prompt.py               ← Provider routing
├── config.py               ← Dev mode flag
├── pymupdf_rag.py          ← PDF to Markdown
├── prompts/
│   ├── template_manager.py
│   └── templates/          ← Jinja templates for each section
├── templates/
│   └── index.html          ← Web UI (NEW)
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚠️ Notes

- Analysis takes **30–90 seconds** depending on your LLM and internet speed
- GitHub enrichment only works if the resume contains a GitHub profile URL
- Set `DEVELOPMENT_MODE = True` in `config.py` to cache results and export CSV

---

## 📄 License

MIT © Built on top of [HackerRank hiring-agent](https://github.com/interviewstreet/hiring-agent)
