@echo off
:: ============================================================
:: 🌲 Forest Fire Alert Agent — Windows Quick Launcher
:: ============================================================
:: Double-click this file to set up and start the agent.
:: ============================================================

title Forest Fire Alert Agent

echo.
echo ============================================================
echo   🌲  Forest Fire Alert Agent — Setup ^& Launch
echo ============================================================
echo.

:: ── Check Python ─────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  ❌  Python not found! Please install Python 3.11+ from:
    echo      https://www.python.org/downloads/
    pause
    exit /b 1
)
echo  ✅  Python found:
python --version

:: ── Create venv if it doesn't exist ─────────────────────────
if not exist "venv\" (
    echo.
    echo  📦  Creating virtual environment...
    python -m venv venv
)
echo  ✅  Virtual environment ready

:: ── Activate venv ────────────────────────────────────────────
call venv\Scripts\activate.bat

:: ── Install / update dependencies ────────────────────────────
echo.
echo  📦  Installing dependencies (this may take a moment)...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo  ❌  pip install failed! Check your internet connection.
    pause
    exit /b 1
)
echo  ✅  Dependencies installed

:: ── Check for .env file ──────────────────────────────────────
if not exist ".env" (
    echo.
    echo  ⚠️   No .env file found! Creating from template...
    copy .env.template .env >nul
    echo  📝  Please open .env and set your OPENAI_API_KEY, then re-run this script.
    echo.
    notepad .env
    pause
    exit /b 0
)
echo  ✅  .env file found

:: ── Launch the app ───────────────────────────────────────────
echo.
echo  🚀  Launching Forest Fire Alert Agent...
echo  🔗  URL: http://127.0.0.1:7860
echo  ⌨️   Press Ctrl+C to stop
echo.
python app.py

pause
