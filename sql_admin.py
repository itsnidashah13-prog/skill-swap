"""
SQLAdmin Setup for Skill Swap FastAPI Application
Database admin interface jo FastAPI ke saath kaam kare
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from database import get_db, engine
from models import User, Skill, SkillExchangeRequest, Notification
import json
from datetime import datetime

# SQLAdmin router banate hain
sql_admin_router = APIRouter(prefix="/admin", tags=["sql-admin"])

@sql_admin_router.get("/", response_class=HTMLResponse)
async def sql_admin_home(db: Session = Depends(get_db)):
    """SQLAdmin home page - Database tables aur statistics dikhaata hai"""
    
    try:
        # Database statistics nikalte hain
        with engine.connect() as connection:
            # User count
            user_result = connection.execute(text("SELECT COUNT(*) FROM users"))
            user_count = user_result.scalar() or 0
            
            # Skill count  
            skill_result = connection.execute(text("SELECT COUNT(*) FROM skills"))
            skill_count = skill_result.scalar() or 0
            
            # Exchange request count
            request_result = connection.execute(text("SELECT COUNT(*) FROM skill_exchange_requests"))
            request_count = request_result.scalar() or 0
            
            # Recent users
            recent_users_result = connection.execute(text("""
                SELECT TOP 5 id, username, full_name, email, created_at 
                FROM users ORDER BY created_at DESC
            """))
            recent_users = recent_users_result.fetchall()
            
            # Recent skills
            recent_skills_result = connection.execute(text("""
                SELECT TOP 5 s.id, s.title, s.category, s.proficiency_level, s.created_at,
                       u.full_name as owner_name
                FROM skills s 
                LEFT JOIN users u ON s.user_id = u.id 
                ORDER BY s.created_at DESC
            """))
            recent_skills = recent_skills_result.fetchall()
            
            # Recent requests
            recent_requests_result = connection.execute(text("""
                SELECT TOP 5 r.id, r.status, r.created_at,
                       s.title as skill_title,
                       req.full_name as requester_name,
                       owner.full_name as skill_owner_name
                FROM skill_exchange_requests r
                LEFT JOIN skills s ON r.skill_id = s.id
                LEFT JOIN users req ON r.requester_id = req.id  
                LEFT JOIN users owner ON r.skill_owner_id = owner.id
                ORDER BY r.created_at DESC
            """))
            recent_requests = recent_requests_result.fetchall()
        
        # HTML response banate hain
        html_content = f"""
        <!DOCTYPE html>
        <html lang="hi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Skill Swap - SQLAdmin Dashboard</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }}
                .admin-header {{
                    background: rgba(255,255,255,0.95);
                    color: #333;
                    padding: 1.5rem 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    border-radius: 0 0 15px 15px;
                }}
                .admin-header h1 {{
                    font-size: 2rem;
                    margin-bottom: 0.5rem;
                    color: #667eea;
                }}
                .admin-header p {{
                    color: #666;
                    font-size: 1rem;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 1.5rem;
                    margin-bottom: 2rem;
                }}
                .stat-card {{
                    background: rgba(255,255,255,0.95);
                    padding: 2rem;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    transition: transform 0.3s ease;
                }}
                .stat-card:hover {{
                    transform: translateY(-5px);
                }}
                .stat-number {{
                    font-size: 3rem;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 0.5rem;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 1.1rem;
                    font-weight: 600;
                }}
                .section {{
                    background: rgba(255,255,255,0.95);
                    border-radius: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    margin-bottom: 2rem;
                    overflow: hidden;
                }}
                .section-header {{
                    background: #667eea;
                    color: white;
                    padding: 1.5rem 2rem;
                    font-size: 1.3rem;
                    font-weight: 600;
                }}
                .section-content {{
                    padding: 2rem;
                }}
                .table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 1rem;
                }}
                .table th, .table td {{
                    padding: 1rem;
                    text-align: left;
                    border-bottom: 1px solid #eee;
                }}
                .table th {{
                    background: #f8f9fa;
                    font-weight: 600;
                    color: #333;
                }}
                .table tr:hover {{
                    background: #f8f9fa;
                }}
                .success-message {{
                    background: #28a745;
                    color: white;
                    padding: 1rem 2rem;
                    border-radius: 10px;
                    text-align: center;
                    margin: 2rem 0;
                    font-size: 1.1rem;
                }}
                .nav-tabs {{
                    display: flex;
                    background: rgba(255,255,255,0.9);
                    border-radius: 10px;
                    padding: 0.5rem;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                .nav-tab {{
                    padding: 1rem 2rem;
                    background: none;
                    border: none;
                    cursor: pointer;
                    border-radius: 8px;
                    font-weight: 600;
                    color: #666;
                    transition: all 0.3s ease;
                }}
                .nav-tab:hover, .nav-tab.active {{
                    background: #667eea;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="admin-header">
                <h1>🗄️ Skill Swap SQLAdmin</h1>
                <p>Database Administration Panel - आपके सभी data को manage करें</p>
            </div>
            
            <div class="container">
                <!-- Statistics Section -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{user_count}</div>
                        <div class="stat-label">👥 कुल उपयोगर</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{skill_count}</div>
                        <div class="stat-label">🎯 कुल स्किल्स</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{request_count}</div>
                        <div class="stat-label">📋 कुल अनुरोध</div>
                    </div>
                </div>
                
                <!-- Navigation Tabs -->
                <div class="nav-tabs">
                    <button class="nav-tab active" onclick="showSection('overview')">📊 Overview</button>
                    <button class="nav-tab" onclick="showSection('users')">👥 Users</button>
                    <button class="nav-tab" onclick="showSection('skills')">🎯 Skills</button>
                    <button class="nav-tab" onclick="showSection('requests')">📋 Requests</button>
                    <button class="nav-tab" onclick="showSection('query')">🔍 Query</button>
                </div>
                
                <!-- Overview Section -->
                <div id="overview-section" class="section">
                    <div class="section-header">
                        📊 Database Overview
                    </div>
                    <div class="section-content">
                        <div class="success-message">
                            ✅ SQLAdmin Successfully Connected!<br>
                            Server running on port 8000<br>
                            Database: blogDb (SQL Server)<br>
                            Total Records: {user_count + skill_count + request_count}
                        </div>
                        
                        <h3>👥 Recent Users</h3>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Username</th>
                                    <th>Full Name</th>
                                    <th>Email</th>
                                    <th>Joined Date</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for user in recent_users:
            html_content += f"""
                                <tr>
                                    <td>{user[0]}</td>
                                    <td>{user[1]}</td>
                                    <td>{user[2] or 'N/A'}</td>
                                    <td>{user[3]}</td>
                                    <td>{user[4].strftime('%Y-%m-%d') if user[4] else 'N/A'}</td>
                                </tr>
            """
        
        html_content += f"""
                            </tbody>
                        </table>
                        
                        <h3>🎯 Recent Skills</h3>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Title</th>
                                    <th>Category</th>
                                    <th>Level</th>
                                    <th>Owner</th>
                                    <th>Created Date</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for skill in recent_skills:
            html_content += f"""
                                <tr>
                                    <td>{skill[0]}</td>
                                    <td>{skill[1]}</td>
                                    <td>{skill[2]}</td>
                                    <td>{skill[3]}</td>
                                    <td>{skill[4] or 'Unknown'}</td>
                                    <td>{skill[5].strftime('%Y-%m-%d') if skill[5] else 'N/A'}</td>
                                </tr>
            """
        
        html_content += f"""
                            </tbody>
                        </table>
                        
                        <h3>📋 Recent Exchange Requests</h3>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Skill</th>
                                    <th>Requester</th>
                                    <th>Skill Owner</th>
                                    <th>Status</th>
                                    <th>Created Date</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for req in recent_requests:
            html_content += f"""
                                <tr>
                                    <td>{req[0]}</td>
                                    <td>{req[1] or 'Unknown'}</td>
                                    <td>{req[2] or 'Unknown'}</td>
                                    <td>{req[3] or 'Unknown'}</td>
                                    <td><span style="color: {'green' if req[2] == 'completed' else 'orange' if req[2] == 'accepted' else 'red'}">{req[2]}</span></td>
                                    <td>{req[4].strftime('%Y-%m-%d') if req[4] else 'N/A'}</td>
                                </tr>
            """
        
        html_content += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Users Section -->
                <div id="users-section" class="section" style="display: none;">
                    <div class="section-header">
                        👥 Users Management
                    </div>
                    <div class="section-content">
                        <p><strong>Total Users:</strong> {user_count}</p>
                        <p>View complete user list with API endpoint: <code>/admin/users-json</code></p>
                    </div>
                </div>
                
                <!-- Skills Section -->
                <div id="skills-section" class="section" style="display: none;">
                    <div class="section-header">
                        🎯 Skills Management
                    </div>
                    <div class="section-content">
                        <p><strong>Total Skills:</strong> {skill_count}</p>
                        <p>View complete skill list with API endpoint: <code>/admin/skills-json</code></p>
                    </div>
                </div>
                
                <!-- Requests Section -->
                <div id="requests-section" class="section" style="display: none;">
                    <div class="section-header">
                        📋 Exchange Requests Management
                    </div>
                    <div class="section-content">
                        <p><strong>Total Requests:</strong> {request_count}</p>
                        <p>View complete request list with API endpoint: <code>/admin/requests-json</code></p>
                    </div>
                </div>
                
                <!-- Query Section -->
                <div id="query-section" class="section" style="display: none;">
                    <div class="section-header">
                        🔍 Custom Database Query
                    </div>
                    <div class="section-content">
                        <p>Execute custom SQL queries on your database:</p>
                        <textarea id="sql-query" style="width: 100%; height: 150px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: monospace;" placeholder="SELECT * FROM users LIMIT 10;"></textarea>
                        <br><br>
                        <button onclick="executeQuery()" style="background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">🔍 Execute Query</button>
                        <div id="query-result" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; display: none;"></div>
                    </div>
                </div>
            </div>
            
            <script>
                function showSection(sectionName) {{
                    // Hide all sections
                    document.querySelectorAll('.section').forEach(section => {{
                        section.style.display = 'none';
                    }});
                    
                    // Remove active class from all tabs
                    document.querySelectorAll('.nav-tab').forEach(tab => {{
                        tab.classList.remove('active');
                    }});
                    
                    // Show selected section
                    document.getElementById(sectionName + '-section').style.display = 'block';
                    
                    // Add active class to clicked tab
                    event.target.classList.add('active');
                }}
                
                async function executeQuery() {{
                    const query = document.getElementById('sql-query').value;
                    const resultDiv = document.getElementById('query-result');
                    
                    if (!query.trim()) {{
                        resultDiv.innerHTML = '<p style="color: red;">Please enter a SQL query</p>';
                        resultDiv.style.display = 'block';
                        return;
                    }}
                    
                    try {{
                        const response = await fetch('/admin/execute-query', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                            }},
                            body: JSON.stringify({{ query: query }})
                        }});
                        
                        const result = await response.json();
                        
                        if (result.success) {{
                            let html = '<h4>Query Results:</h4><table style="width: 100%; border-collapse: collapse;"><thead><tr>';
                            
                            if (result.columns && result.columns.length > 0) {{
                                html += '<th style="padding: 10px; background: #f0f0f0; border: 1px solid #ddd;">#</th>';
                                result.columns.forEach(col => {{
                                    html += `<th style="padding: 10px; background: #f0f0f0; border: 1px solid #ddd;">${{col}}</th>`;
                                }});
                                html += '</tr></thead><tbody>';
                            }}
                            
                            if (result.data && result.data.length > 0) {{
                                result.data.forEach(row => {{
                                    html += '<tr>';
                                    result.columns.forEach((col, index) => {{
                                        html += '<td style="padding: 10px; border: 1px solid #ddd;">' + (row[index] || 'NULL') + '</td>';
                                    }});
                                    html += '</tr>';
                                }});
                            }} else {{
                                html += '<tr><td colspan="100" style="padding: 20px; text-align: center;">No results found</td></tr>';
                            }}
                            
                            html += '</tbody></table>';
                            resultDiv.innerHTML = html;
                        }} else {{
                            resultDiv.innerHTML = `<p style="color: red;">Error: ${{result.error}}</p>`;
                        }}
                        
                        resultDiv.style.display = 'block';
                        
                    }} catch (error) {{
                        resultDiv.innerHTML = `<p style="color: red;">Error: ${{error.message}}</p>`;
                        resultDiv.style.display = 'block';
                    }}
                }}
            </script>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head><title>Database Error</title></head>
        <body>
            <h1>❌ Database Connection Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><strong>Solution:</strong> Check database connection and try again</p>
        </body>
        </html>
        """, status_code=500)

@sql_admin_router.get("/users-json")
async def users_json(db: Session = Depends(get_db)):
    """Users data as JSON"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT id, username, full_name, email, is_active, created_at 
                FROM users 
                ORDER BY created_at DESC
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
                        "is_active": bool(user[4]),
                        "created_at": user[5].isoformat() if user[5] else None
                    } for user in users
                ]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@sql_admin_router.get("/skills-json")
async def skills_json(db: Session = Depends(get_db)):
    """Skills data as JSON"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT s.id, s.title, s.description, s.category, s.proficiency_level, 
                       s.is_active, s.created_at, u.full_name as owner_name
                FROM skills s 
                LEFT JOIN users u ON s.user_id = u.id 
                ORDER BY s.created_at DESC
            """))
            skills = result.fetchall()
            
            return {
                "success": True,
                "count": len(skills),
                "data": [
                    {
                        "id": skill[0],
                        "title": skill[1],
                        "description": skill[2],
                        "category": skill[3],
                        "proficiency_level": skill[4],
                        "is_active": bool(skill[5]),
                        "created_at": skill[6].isoformat() if skill[6] else None,
                        "owner_name": skill[7]
                    } for skill in skills
                ]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@sql_admin_router.get("/requests-json")
async def requests_json(db: Session = Depends(get_db)):
    """Exchange requests data as JSON"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT r.id, r.status, r.message, r.created_at, r.updated_at,
                       s.title as skill_title,
                       req.full_name as requester_name,
                       owner.full_name as skill_owner_name
                FROM skill_exchange_requests r
                LEFT JOIN skills s ON r.skill_id = s.id
                LEFT JOIN users req ON r.requester_id = req.id  
                LEFT JOIN users owner ON r.skill_owner_id = owner.id
                ORDER BY r.created_at DESC
            """))
            requests = result.fetchall()
            
            return {
                "success": True,
                "count": len(requests),
                "data": [
                    {
                        "id": req[0],
                        "status": req[1],
                        "message": req[2],
                        "created_at": req[3].isoformat() if req[3] else None,
                        "updated_at": req[4].isoformat() if req[4] else None,
                        "skill_title": req[5],
                        "requester_name": req[6],
                        "skill_owner_name": req[7]
                    } for req in requests
                ]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@sql_admin_router.post("/execute-query")
async def execute_query(request: dict, db: Session = Depends(get_db)):
    """Execute custom SQL query"""
    try:
        query = request.get("query", "").strip()
        
        if not query:
            return {"success": False, "error": "No query provided"}
        
        # Security: Allow only SELECT queries for safety
        if not query.upper().startswith('SELECT'):
            return {"success": False, "error": "Only SELECT queries are allowed for safety"}
        
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            columns = list(result.keys()) if result else []
            
            return {
                "success": True,
                "columns": columns,
                "data": [dict(zip(columns, row)) for row in rows],
                "count": len(rows)
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}
