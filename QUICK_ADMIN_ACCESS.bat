@echo off
title Skill Swap - Admin Access Test
echo ========================================================
echo SKILL SWAP - ADMIN INTERFACE ACCESS TEST
echo ========================================================
echo.

echo [1/3] Checking if server is running...
cd /d "%~dp0"

echo Testing server connection...
curl -s http://127.0.0.1:8000/ >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Server is RUNNING on port 8000
) else (
    echo ❌ Server is NOT running on port 8000
    echo.
    echo Starting server now...
    start "Backend Server" cmd /k "python main.py"
    echo Waiting for server to start...
    timeout /t 5 /nobreak >nul
)

echo.
echo [2/3] Testing admin URLs...
echo.

echo Testing Admin Dashboard...
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:8000/admin/ > temp_status.txt
set /p admin_status=<temp_status.txt
if "%admin_status%"=="200" (
    echo ✅ Admin Dashboard: http://127.0.0.1:8000/admin/ - WORKING
) else (
    echo ❌ Admin Dashboard: http://127.0.0.1:8000/admin/ - Status %admin_status%
)

echo Testing API Root...
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:8000/ > temp_status.txt
set /p api_status=<temp_status.txt
if "%api_status%"=="200" (
    echo ✅ API Root: http://127.0.0.1:8000/ - WORKING
) else (
    echo ❌ API Root: http://127.0.0.1:8000/ - Status %api_status%
)

del temp_status.txt >nul 2>&1

echo.
echo [3/3] Opening admin interface...
echo.

echo ========================================================
echo ADMIN INTERFACE URLS:
echo ========================================================
echo.
echo 1. Admin Dashboard:
echo    http://127.0.0.1:8000/admin/
echo.
echo 2. User Management:
echo    http://127.0.0.1:8000/admin/auth/user/
echo.
echo 3. Skill Management:
echo    http://127.0.0.1:8000/admin/skills/skill/
echo.
echo 4. Add New Skill:
echo    http://127.0.0.1:8000/admin/skills/skill/add/
echo.
echo 5. API Documentation:
echo    http://127.0.0.1:8000/docs
echo.
echo 6. Frontend Application:
echo    http://127.0.0.1:3002/frontend/index.html
echo.
echo ========================================================
echo.
echo Opening admin dashboard in browser...
start http://127.0.0.1:8000/admin/

echo.
echo If admin dashboard doesn't open:
echo 1. Check that server is running (python main.py)
echo 2. Try alternative URL: http://localhost:8000/admin/
echo 3. Check if port 8000 is blocked by firewall
echo 4. Install dependencies: pip install jinja2 fastapi
echo.
pause
