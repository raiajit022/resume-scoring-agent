@echo off
echo 🤖 Setting up Resume Scoring Agent...
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Edit .env and add your GEMINI_API_KEY
echo   2. Run: uvicorn app:app --reload --port 8000
echo   3. Open: http://localhost:8000
