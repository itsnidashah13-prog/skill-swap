@echo off
title Skill Swap - Complete Fix
echo ========================================================
echo SKILL SWAP - COMPLETE PROJECT FIX
echo ========================================================
echo.

echo [1/4] Checking database and populating data...
cd /d "%~dp0"
python populate_data.py
echo.

echo [2/4] Testing complete project fixes...
python test_complete_fix.py
echo.

echo [3/4] Starting Backend Server on port 8000...
start "Backend Server" cmd /k "python main.py"

echo [4/4] Starting Frontend Server on port 3002...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================================
echo COMPLETE PROJECT FIX - SERVERS STARTING UP...
echo.
echo Backend API:  http://127.0.0.1:8000
echo Frontend App: http://127.0.0.1:3002/frontend/index.html
echo Test Page:    http://127.0.0.1:3002/frontend/test_fixed_auth.html
echo.
echo 🔧 COMPLETE FIXES APPLIED:
echo ✅ Fixed API Endpoints (404 Error) - Added /api prefix
echo ✅ Fixed Authentication Flow - Uses 'accessToken' key
echo ✅ Fixed Connection (Failed to Fetch) - Enhanced CORS
echo ✅ Auto-Generated Data - Database populated with skills
echo ✅ Cleaned up Frontend - Redirects to login on auth errors
echo.
echo 🔑 Default Login Credentials:
echo Username: john_doe    Password: password123
echo Username: jane_smith  Password: password123
echo Username: mike_wilson Password: password123
echo Username: sarah_chen  Password: password123
echo.
echo 🧪 Testing Commands:
echo python test_complete_fix.py    - Test all fixes
echo python -m http.server 3002  - Start frontend only
echo python main.py                - Start backend only
echo.
echo ========================================================
echo.
echo Wait for both servers to start, then test the application.
echo All major issues should be resolved!
echo ========================================================
echo.
pause
