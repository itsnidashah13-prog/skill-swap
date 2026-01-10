@echo off
title Skill Swap - Django-Style Admin
echo ========================================================
echo SKILL SWAP - DJANGO-STYLE ADMIN INTERFACE
echo ========================================================
echo.

echo [1/4] Installing required dependencies...
cd /d "%~dp0"
pip install jinja2
echo.

echo [2/4] Checking database and populating data...
python populate_data.py
echo.

echo [3/4] Starting Backend Server with Django-Style Admin...
start "Backend with Django Admin" cmd /k "python main.py"

echo [4/4] Starting Frontend Server...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================================
echo DJANGO-STYLE ADMIN INTERFACE - SERVERS STARTING UP...
echo.
echo Backend API:           http://127.0.0.1:8000
echo Frontend App:          http://127.0.0.1:3002/frontend/index.html
echo.
echo 🔧 DJANGO-STYLE ADMIN INTERFACE:
echo Admin Home:            http://127.0.0.1:8000/admin/
echo User Management:        http://127.0.0.1:8000/admin/auth/user/
echo Skill Management:       http://127.0.0.1:8000/admin/skills/skill/
echo Request Management:     http://127.0.0.1:8000/admin/exchanges/skillexchangerequest/
echo.
echo 🎯 DJANGO-STYLE FEATURES:
echo ✅ Django-style admin home page with app list
echo ✅ User list and management interface
echo ✅ Skill list and add forms
echo ✅ Exchange request monitoring
echo ✅ Django-like URL structure (/admin/app/model/)
echo ✅ Clean, professional admin interface
echo.
echo 📋 ADMIN FEATURES:
echo ✅ View all users, skills, and requests
echo ✅ Add new skills via web forms
echo ✅ Django-style navigation and layout
echo ✅ Professional admin interface
echo ✅ No authentication required (for testing)
echo.
echo 🛠️ TROUBLESHOOTING:
echo If admin page shows JSON error:
echo 1. Ensure jinja2 is installed: pip install jinja2
echo 2. Ensure server is running on port 8000
echo 3. Check that admin router is included first in main.py
echo 4. Verify database tables exist
echo.
echo ========================================================
echo.
echo Wait for servers to start, then visit Django-style admin!
echo ========================================================
echo.
pause
