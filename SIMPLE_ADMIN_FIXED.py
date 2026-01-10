"""
Simple Admin Interface - Working version
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from database import get_db, engine
from sqlalchemy import text

# Simple admin router
simple_admin_router = APIRouter(prefix="/admin", tags=["simple-admin"])

@simple_admin_router.get("/", response_class=HTMLResponse)
async def admin_home(db: Session = Depends(get_db)):
    """Simple admin home page"""
    
    try:
        # Get statistics
        with engine.connect() as connection:
            user_count = connection.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
            skill_count = connection.execute(text("SELECT COUNT(*) FROM skills")).scalar() or 0
            request_count = connection.execute(text("SELECT COUNT(*) FROM skill_exchange_requests")).scalar() or 0
            
            # Get recent data
            recent_users = connection.execute(text("""
                SELECT TOP 5 username, full_name, email FROM users ORDER BY created_at DESC
            """)).fetchall()
            
            recent_skills = connection.execute(text("""
                SELECT TOP 5 title, category FROM skills ORDER BY created_at DESC
            """)).fetchall()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Skill Swap Admin</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .header {{
                    background: #007bff;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 20px;
                }}
                .stat-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #007bff;
                }}
                .section {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .section h2 {{
                    color: #007bff;
                    margin-top: 0;
                }}
                .list {{
                    list-style: none;
                    padding: 0;
                }}
                .list li {{
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .list li:last-child {{
                    border-bottom: none;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔧 Skill Swap Admin Panel</h1>
                <p>Database Administration Interface</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{user_count}</div>
                    <div>Total Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{skill_count}</div>
                    <div>Total Skills</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{request_count}</div>
                    <div>Total Requests</div>
                </div>
            </div>
            
            <div class="section">
                <h2>👥 Recent Users</h2>
                <ul class="list">
        """
        
        for user in recent_users:
            html_content += f"""
                    <li>
                        <strong>{user[1] or user[0]}</strong> - {user[2]}
                    </li>
            """
        
        html_content += f"""
                </ul>
            </div>
            
            <div class="section">
                <h2>🎯 Recent Skills</h2>
                <ul class="list">
        """
        
        for skill in recent_skills:
            html_content += f"""
                    <li>
                        <strong>{skill[0]}</strong> - {skill[1]}
                    </li>
            """
        
        html_content += f"""
                </ul>
            </div>
            
            <div class="section">
                <h2>🔗 Quick Links</h2>
                <ul class="list">
                    <li><a href="/admin/users-json">📊 Users JSON Data</a></li>
                    <li><a href="/admin/skills-json">📊 Skills JSON Data</a></li>
                    <li><a href="/admin/requests-json">📊 Requests JSON Data</a></li>
                    <li><a href="/docs">📚 API Documentation</a></li>
                    <li><a href="/health">💚 Health Check</a></li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #666;">
                <p><strong>✅ Admin Interface Working Successfully!</strong></p>
                <p>Server running on port 8000</p>
                <p><small>FastAPI Backend with Simple Admin Interface</small></p>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head><title>Admin Error</title></head>
        <body>
            <h1>❌ Admin Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><strong>Solution:</strong> Check database connection</p>
        </body>
        </html>
        """, status_code=500)

@simple_admin_router.get("/users-json")
async def users_json(db: Session = Depends(get_db)):
    """Users data as JSON"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT TOP 10 id, username, full_name, email, created_at 
                FROM users ORDER BY created_at DESC
            """))
            users = result.fetchall()
            
            return {
                "success": True,
                "count": len(users),
                "data": [
                    {
                        "id": user[0],
                        "username": user[1], 
                        "full_name": user[2],
                        "email": user[3],
                        "created_at": user[4].isoformat() if user[4] else None
                    } for user in users
                ]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@simple_admin_router.get("/skills-json")
async def skills_json(db: Session = Depends(get_db)):
    """Skills data as JSON"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT TOP 10 id, title, category, proficiency_level, created_at
                FROM skills ORDER BY created_at DESC
            """))
            skills = result.fetchall()
            
            return {
                "success": True,
                "count": len(skills),
                "data": [
                    {
                        "id": skill[0],
                        "title": skill[1],
                        "category": skill[2],
                        "proficiency_level": skill[3],
                        "created_at": skill[4].isoformat() if skill[4] else None
                    } for skill in skills
                ]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@simple_admin_router.get("/requests-json")
async def requests_json(db: Session = Depends(get_db)):
    """Exchange requests data as JSON"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT TOP 10 id, status, created_at
                FROM skill_exchange_requests ORDER BY created_at DESC
            """))
            requests = result.fetchall()
            
            return {
                "success": True,
                "count": len(requests),
                "data": [
                    {
                        "id": req[0],
                        "status": req[1],
                        "created_at": req[2].isoformat() if req[2] else None
                    } for req in requests
                ]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
