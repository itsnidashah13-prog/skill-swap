@echo off
title Skill Swap - Quick Start
echo ========================================
echo SKILL SWAP APPLICATION - QUICK START
echo ========================================
echo.

echo [1/3] Checking database...
cd /d "%~dp0"
python populate_data.py
echo.

echo [2/3] Starting Backend Server on port 8000...
start "Backend Server" cmd /k "python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo [3/3] Starting Frontend Server on port 3002...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================
echo SERVERS STARTING UP...
echo.
echo Backend API:  http://127.0.0.1:8000
echo Frontend App: http://127.0.0.1:3002/frontend/index.html
echo Test Page:    http://127.0.0.1:3002/frontend/test_fixed_auth.html
echo.
echo Default Login Credentials:
echo Username: john_doe    Password: password123
echo Username: jane_smith  Password: password123
echo Username: mike_wilson Password: password123
echo Username: sarah_chen  Password: password123
echo.
echo Wait for both servers to start, then open the frontend in your browser.
echo ========================================
echo.
pause
