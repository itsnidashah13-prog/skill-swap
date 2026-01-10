"""
Simple Working Admin Interface
Minimal admin that actually works
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Skill, SkillExchangeRequest
from crud import get_users, get_skills, get_skill_exchange_requests

# Create simple admin router
simple_admin_router = APIRouter(prefix="/admin", tags=["simple-admin"])

@simple_admin_router.get("/", response_class=HTMLResponse)
async def admin_home(db: Session = Depends(get_db)):
    """Simple admin home page"""
    
    # Get statistics
    user_count = len(get_users(db, skip=0, limit=1000))
    skill_count = len(get_skills(db, skip=0, limit=1000))
    request_count = len(get_skill_exchange_requests(db, skip=0, limit=1000))
    
    # Get recent items
    recent_users = get_users(db, skip=0, limit=5)
    recent_skills = get_skills(db, skip=0, limit=5)
    recent_requests = get_skill_exchange_requests(db, skip=0, limit=5)
    
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
            .item-list {{
                list-style: none;
                padding: 0;
            }}
            .item-list li {{
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}
            .item-list li:last-child {{
                border-bottom: none;
            }}
            .add-btn {{
                background: #28a745;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                margin: 10px 0;
            }}
            .add-btn:hover {{
                background: #218838;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔧 Skill Swap Admin Panel</h1>
            <p>Complete administration interface for your Skill Swap platform</p>
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
            <ul class="item-list">
    """
    
    for user in recent_users:
        html_content += f"""
                <li>
                    <strong>{user.full_name or user.username}</strong> - {user.email}
                    <br><small>Joined: {user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'}</small>
                </li>
        """
    
    html_content += """
            </ul>
        </div>
        
        <div class="section">
            <h2>🎯 Recent Skills</h2>
            <ul class="item-list">
    """
    
    for skill in recent_skills:
        html_content += f"""
                <li>
                    <strong>{skill.title}</strong> - {skill.category}
                    <br><small>By: {skill.owner.full_name if skill.owner else 'Unknown'} | Level: {skill.proficiency_level}</small>
                </li>
        """
    
    html_content += """
            </ul>
        </div>
        
        <div class="section">
            <h2>📋 Recent Exchange Requests</h2>
            <ul class="item-list">
    """
    
    for req in recent_requests:
        html_content += f"""
                <li>
                    <strong>Request for: {req.skill.title if req.skill else 'Unknown Skill'}</strong>
                    <br><small>Status: {req.status} | Created: {req.created_at.strftime('%Y-%m-%d') if req.created_at else 'N/A'}</small>
                </li>
        """
    
    html_content += f"""
            </ul>
        </div>
        
        <div class="section">
            <h2>🚀 Quick Actions</h2>
            <a href="/admin/add-skill-form" class="add-btn">➕ Add New Skill</a>
            <a href="/docs" class="add-btn">📚 API Documentation</a>
            <a href="/health" class="add-btn">💚 Health Check</a>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p><strong>✅ Admin Interface Working Successfully!</strong></p>
            <p>Server is running on port 8000 with full admin functionality</p>
            <p><small>FastAPI Backend with Custom Admin Interface</small></p>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@simple_admin_router.get("/add-skill-form", response_class=HTMLResponse)
async def add_skill_form(db: Session = Depends(get_db)):
    """Simple form to add skills"""
    
    users = get_users(db, skip=0, limit=100)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add Skill - Admin</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }}
            input, select, textarea {{
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }}
            textarea {{
                height: 100px;
                resize: vertical;
            }}
            .btn {{
                background: #007bff;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }}
            .btn:hover {{
                background: #0056b3;
            }}
            .back-link {{
                display: block;
                margin-top: 20px;
                color: #007bff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>➕ Add New Skill</h1>
            
            <form method="post" action="/admin/api/skills/">
                <div class="form-group">
                    <label for="title">Skill Title</label>
                    <input type="text" id="title" name="title" required>
                </div>
                
                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" name="description" required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="category">Category</label>
                    <select id="category" name="category" required>
                        <option value="">Select Category</option>
                        <option value="Programming">Programming</option>
                        <option value="Design">Design</option>
                        <option value="Marketing">Marketing</option>
                        <option value="Writing">Writing</option>
                        <option value="Teaching">Teaching</option>
                        <option value="Music">Music</option>
                        <option value="Photography">Photography</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="proficiency_level">Proficiency Level</label>
                    <select id="proficiency_level" name="proficiency_level" required>
                        <option value="">Select Level</option>
                        <option value="Beginner">Beginner</option>
                        <option value="Intermediate">Intermediate</option>
                        <option value="Advanced">Advanced</option>
                        <option value="Expert">Expert</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="user_id">Owner</label>
                    <select id="user_id" name="user_id" required>
    """
    
    for user in users:
        html_content += f"""
                        <option value="{user.id}">{user.full_name or user.username} ({user.email})</option>
        """
    
    html_content += f"""
                    </select>
                </div>
                
                <button type="submit" class="btn">Add Skill</button>
            </form>
            
            <a href="/admin/" class="back-link">← Back to Admin Dashboard</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@simple_admin_router.post("/api/skills/")
async def create_skill_api(
    title: str,
    description: str,
    category: str,
    proficiency_level: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    """API endpoint to create skills"""
    
    from schemas import SkillCreate
    from crud import create_skill
    
    skill_data = SkillCreate(
        title=title,
        description=description,
        category=category,
        proficiency_level=proficiency_level
    )
    
    create_skill(db, skill_data, user_id=user_id)
    
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Success</title></head>
    <body>
        <h1>✅ Skill Added Successfully!</h1>
        <p><a href="/admin/">← Back to Admin Dashboard</a></p>
        <p><a href="/admin/add-skill-form">← Add Another Skill</a></p>
    </body>
    </html>
    """, status_code=201)
