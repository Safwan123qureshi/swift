@echo off
REM Launch the Swift Sign Chatbot backend.
REM The virtual environment lives at the project root (.\venv), so we run from
REM the project root using run.py, which sets up sys.path to the backend folder.
cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "backend\venv\Scripts\activate.bat" (
    call backend\venv\Scripts\activate.bat
)

python run.py
pause