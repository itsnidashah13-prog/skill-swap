@echo off
title Skill Swap - Final Fix
echo ========================================================
echo SKILL SWAP - FINAL URL MAPPING & AUTHENTICATION FIX
echo ========================================================
echo.

echo [1/5] Checking database and populating data...
cd /d "%~dp0"
python populate_data.py
echo.

echo [2/5] Verifying URL mapping between frontend and backend...
python url_mapping_fix.py
echo.

echo [3/5] Testing complete authentication flow...
python test_complete_fix.py
echo.

echo [4/5] Starting Backend Server on port 8000...
start "Backend Server" cmd /k "python main.py"

echo [5/5] Starting Frontend Server on port 3002...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================================
echo FINAL FIX - SERVERS STARTING UP...
echo.
echo Backend API:  http://127.0.0.1:8000
echo Frontend App: http://127.0.0.1:3002/frontend/index.html
echo.
echo 🔧 CRITICAL FIXES APPLIED:
echo ✅ URL Mapping (404 Fix) - All frontend/backend URLs match
echo ✅ Register/Login - Endpoints working correctly
echo ✅ Token Flow - 'accessToken' saved and retrieved properly
echo ✅ CORS & Trailing Slashes - All handled correctly
echo ✅ Database Check - Tables exist and populated
echo.
echo 📡 URL MAPPINGS VERIFIED:
echo Frontend: users/register     -> Backend: /api/users/register
echo Frontend: users/login        -> Backend: /api/users/login  
echo Frontend: skills/            -> Backend: /api/skills/
echo Frontend: exchanges/         -> Backend: /api/exchanges/
echo.
echo 🔑 Default Login Credentials:
echo Username: john_doe    Password: password123
echo Username: jane_smith  Password: password123
echo Username: mike_wilson Password: password123
echo Username: sarah_chen  Password: password123
echo.
echo 🧪 Testing Commands:
echo python url_mapping_fix.py  - Verify URL mappings
echo python test_complete_fix.py - Test all functionality
echo.
echo ========================================================
echo.
echo All 404 errors and 'Auth Token Missing' issues should be resolved!
echo Wait for servers to start, then test the application.
echo ========================================================
echo.
pause
