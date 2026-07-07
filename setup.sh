#!/bin/bash
# Quick setup script for Linux/macOS
echo "🤖 Setting up Resume Scoring Agent..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GEMINI_API_KEY"
echo "  2. Run: uvicorn app:app --reload --port 8000"
echo "  3. Open: http://localhost:8000"
