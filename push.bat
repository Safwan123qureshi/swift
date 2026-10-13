@echo off
REM ============================================================
REM  One-click push to GitHub (triggers Vercel auto-deploy)
REM  Double-click this file, or run: push.bat
REM ============================================================
cd /d "%~dp0"

echo.
echo === Pushing Swift Sign Chatbot to GitHub ===
echo A GitHub login window may appear - sign in to authorize.
echo.

git push origin main

if %ERRORLEVEL%==0 (
    echo.
    echo [SUCCESS] Code pushed! Vercel will auto-deploy in ~1-2 minutes.
    echo Remember: set GEMINI_API_KEY in Vercel Settings ^> Environment Variables.
) else (
    echo.
    echo [FAILED] Push did not complete. Check your GitHub login and try again.
)

echo.
pause
