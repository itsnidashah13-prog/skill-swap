@echo off
title Skill Swap - Admin Interface
echo ========================================================
echo SKILL SWAP - ADMIN INTERFACE SETUP
echo ========================================================
echo.

echo [1/4] Installing required dependencies...
cd /d "%~dp0"
pip install -r requirements_admin.txt
echo.

echo [2/4] Checking database and creating admin user...
python populate_data.py
echo.

echo [3/4] Starting Backend Server with Admin Interface...
start "Backend with Admin" cmd /k "python main.py"

echo [4/4] Starting Frontend Server...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3002"

echo.
echo ========================================================
echo ADMIN INTERFACE - SERVERS STARTING UP...
echo.
echo Backend API:      http://127.0.0.1:8000
echo Frontend App:     http://127.0.0.1:3002/frontend/index.html
echo.
echo 🔧 ADMIN INTERFACE:
echo Admin Login:      http://127.0.0.1:8000/admin/login
echo Admin Dashboard:   http://127.0.0.1:8000/admin/
echo.
echo 🔑 ADMIN CREDENTIALS:
echo Username: admin
echo Password: admin123
echo.
echo 📋 ADMIN FEATURES:
echo ✅ User Management - View and manage all users
echo ✅ Skill Management - Add, edit, delete skills
echo ✅ Request Management - Monitor exchange requests
echo ✅ Statistics Dashboard - View platform statistics
echo ✅ Database Access - Full CRUD operations
echo.
echo 🛠️ TROUBLESHOOTING:
echo If admin page shows JSON error, ensure:
echo 1. All dependencies are installed
echo 2. Database tables are created
echo 3. Admin user exists
echo 4. Server is running on port 8000
echo.
echo ========================================================
echo.
echo Wait for servers to start, then visit admin interface!
echo ========================================================
echo.
pause
