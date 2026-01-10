@echo off
title Skill Swap - Fixed Servers
echo ========================================
echo SKILL SWAP - FIXED BACKEND STARTUP
echo ========================================
echo.

echo [1/3] Checking database...
cd /d "%~dp0"
python populate_data.py
echo.

echo [2/3] Starting FIXED Backend Server on port 8000...
echo Using backend_fix.py with enhanced CORS and debugging
start "Fixed Backend Server" cmd /k "python backend_fix.py"

echo [3/3] Starting Frontend Server on port 3002...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================
echo FIXED SERVERS STARTING UP...
echo.
echo Backend API:  http://127.0.0.1:8000
echo Frontend App: http://127.0.0.1:3002/frontend/index.html
echo Test Page:    http://127.0.0.1:3002/frontend/test_fixed_auth.html
echo.
echo DEBUG ENDPOINTS:
echo - Health:     http://127.0.0.1:8000/health
echo - Endpoints:  http://127.0.0.1:8000/debug/endpoints
echo - CORS:       http://127.0.0.1:8000/debug/cors
echo - Database:   http://127.0.0.1:8000/debug/database
echo.
echo Default Login Credentials:
echo Username: john_doe    Password: password123
echo Username: jane_smith  Password: password123
echo Username: mike_wilson Password: password123
echo Username: sarah_chen  Password: password123
echo.
echo ========================================
echo.
echo 🔧 BACKEND FIXES APPLIED:
echo ✅ Enhanced CORS configuration
echo ✅ API endpoints with /api prefix
echo ✅ Comprehensive error handling
echo ✅ Debug endpoints for troubleshooting
echo ✅ Global exception handler
echo ✅ Database connection verification
echo.
echo Wait for both servers to start, then test the application.
echo ========================================
echo.
pause
