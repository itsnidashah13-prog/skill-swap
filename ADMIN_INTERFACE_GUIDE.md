# Skill Swap Admin Interface Guide

## 🚨 IMPORTANT: You're Using FastAPI, Not Django!

Your project uses **FastAPI**, not Django. FastAPI doesn't have a built-in admin panel like Django's `/admin/`. I've created a custom admin interface for you.

## 🔧 Admin Interface Setup

### Method 1: Simple JSON Admin Interface (Recommended)

1. **Start the server:**
   ```bash
   cd "c:/Users/Javy/Desktop/skill swap"
   python main.py
   ```

2. **Access admin endpoints:**
   - **Admin Dashboard:** http://127.0.0.1:8000/admin/
   - **Users Management:** http://127.0.0.1:8000/admin/users
   - **Skills Management:** http://127.0.0.1:8000/admin/skills
   - **Requests Management:** http://127.0.0.1:8000/admin/requests

3. **Authentication:**
   - **Username:** `admin`
   - **Password:** `admin123`
   - Uses HTTP Basic Authentication

### Method 2: Quick Start Script

1. **Run the admin startup script:**
   ```bash
   START_ADMIN_INTERFACE.bat
   ```

2. **Wait for servers to start**

3. **Visit admin interface**

## 📋 Admin Endpoints

### Dashboard
- **URL:** `GET /admin/`
- **What it shows:** Platform statistics, recent users, skills, and requests
- **Example:** http://127.0.0.1:8000/admin/

### Users Management
- **List Users:** `GET /admin/users`
- **Get User:** `GET /admin/users/{user_id}`
- **Create User:** `POST /admin/users`
- **Example:** http://127.0.0.1:8000/admin/users

### Skills Management
- **List Skills:** `GET /admin/skills`
- **Create Skill:** `POST /admin/skills`
- **Update Skill:** `PUT /admin/skills/{skill_id}`
- **Delete Skill:** `DELETE /admin/skills/{skill_id}`
- **Example:** http://127.0.0.1:8000/admin/skills

### Requests Management
- **List Requests:** `GET /admin/requests`
- **Update Request:** `PUT /admin/requests/{request_id}`
- **Example:** http://127.0.0.1:8000/admin/requests

## 🛠️ How to Add Skills via Admin

### Using curl (Command Line):
```bash
# Create a new skill
curl -X POST "http://127.0.0.1:8000/admin/skills" \
  -u "admin:admin123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Web Development",
    "description": "Full-stack web development with React and Node.js",
    "category": "Programming",
    "proficiency_level": "Advanced"
  }'
```

### Using Python:
```python
import requests

# Create a new skill
skill_data = {
    "title": "Graphic Design",
    "description": "Professional graphic design services",
    "category": "Design",
    "proficiency_level": "Expert"
}

response = requests.post(
    "http://127.0.0.1:8000/admin/skills",
    auth=("admin", "admin123"),
    json=skill_data
)

print(response.json())
```

### Using Browser:
1. **Open:** http://127.0.0.1:8000/admin/skills
2. **Use browser dev tools** to make POST requests
3. **Or use API tools** like Postman/Insomnia

## 🔍 Troubleshooting

### "Not Found" Error
- **Cause:** Server not running or wrong URL
- **Fix:** Ensure `python main.py` is running and use correct URLs

### Authentication Error
- **Cause:** Wrong admin credentials
- **Fix:** Use `admin` / `admin123`

### Database Issues
- **Cause:** Tables not created
- **Fix:** Run `python populate_data.py`

### CORS Issues
- **Cause:** Frontend trying to access admin
- **Fix:** Admin endpoints are backend-only, not for frontend

## 📊 Alternative: Use Existing Data Population

If you just want to add data to test your application:

1. **Run the data population script:**
   ```bash
   python populate_data.py
   ```

2. **This creates:**
   - 28 sample users
   - Multiple skills across different categories
   - Sample exchange requests

3. **Login with any user:**
   - Username: `john_doe`, Password: `password123`
   - Username: `jane_smith`, Password: `password123`

## 🎯 Summary

- **FastAPI ≠ Django:** No built-in `/admin/` panel
- **Custom Admin:** Created REST API endpoints at `/admin/`
- **Authentication:** HTTP Basic with `admin:admin123`
- **Data Management:** Use REST API calls or existing data
- **Testing:** Use `START_ADMIN_INTERFACE.bat` for easy setup

The admin interface provides all the functionality you need to manage users, skills, and requests without requiring Django's admin panel.
