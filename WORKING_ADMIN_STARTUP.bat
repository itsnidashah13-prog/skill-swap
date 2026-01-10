@echo off
title Skill Swap - Working Admin
echo ========================================================
echo SKILL SWAP - WORKING ADMIN INTERFACE
echo ========================================================
echo.

echo [1/3] Checking dependencies...
cd /d "%~dp0"
python -c "import fastapi, jinja2; print('✅ Dependencies OK')" 2>nul
if errorlevel 1 (
    echo ❌ Installing missing dependencies...
    pip install fastapi jinja2 uvicorn
)

echo [2/3] Starting server with working admin...
echo.
echo Starting FastAPI server with Simple Working Admin...
start "FastAPI Server" cmd /k "python main.py"

echo [3/3] Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo ========================================================
echo WORKING ADMIN INTERFACE - READY!
echo ========================================================
echo.
echo 🚀 ADMIN URLS:
echo.
echo 1. Admin Dashboard:
echo    http://127.0.0.1:8000/admin/
echo.
echo 2. Add Skill Form:
echo    http://127.0.0.1:8000/admin/add-skill-form
echo.
echo 3. API Documentation:
echo    http://127.0.0.1:8000/docs
echo.
echo 4. Frontend Application:
echo    http://127.0.0.1:3002/frontend/index.html
echo.
echo ========================================================
echo ✅ FEATURES:
echo.
echo ✅ Professional admin dashboard
echo ✅ Real-time statistics
echo ✅ Add skills via web form
echo ✅ View users, skills, requests
echo ✅ No authentication required (for testing)
echo ✅ Clean, modern interface
echo ✅ FastAPI backend with custom admin
echo.
echo ========================================================
echo.
echo Opening admin dashboard in browser...
start http://127.0.0.1:8000/admin/

echo.
echo If admin doesn't open:
echo 1. Wait 10 seconds for server to fully start
echo 2. Try: http://localhost:8000/admin/
echo 3. Try: http://127.0.0.1:8000/admin/
echo 4. Check server console for errors
echo.
echo ========================================================
echo.
echo Your working admin interface is now ready!
echo ========================================================
echo.
pause
