@echo off
echo Starting Skill Swap Application Servers...
echo.

echo [1/2] Starting Backend Server on port 8000...
cd /d "%~dp0"
start "Backend Server" cmd /k "python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting Frontend Server on port 3002...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================
echo Servers Starting Up...
echo.
echo Frontend: http://127.0.0.1:3002/frontend/index.html
echo Backend:  http://127.0.0.1:8000
echo Test Page: http://127.0.0.1:3002/frontend/test_auth_complete.html
echo.
echo Wait for both servers to start before testing!
echo ========================================
echo.
pause
