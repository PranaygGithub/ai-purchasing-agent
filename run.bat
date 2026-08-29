@echo off
title Procura AI - Purchasing Agent
echo ==========================================
echo       PROCURA AI PURCHASING AGENT
echo ==========================================
echo.
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting FastAPI server...
echo Open http://127.0.0.1:8000
echo.
uvicorn backend.main:app --reload
pause
