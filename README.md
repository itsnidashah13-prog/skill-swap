# Community Skill Swap Platform 

A modern web application for community-based skill exchange, where users can share their expertise and learn from others.

## Features

- **User Authentication**: Secure registration and login with JWT
- **Skill Management**: Add, edit, and showcase skills
- **Skill Exchange**: Request skills from community members
- **Request Management**: Accept, reject, or complete exchanges
- **Category Filtering**: Browse by Programming, Design, Music, etc.
- **Responsive Design**: Works on all devices

## Tech Stack

**Backend**: FastAPI, SQLAlchemy, JWT, Uvicorn
**Frontend**: HTML5, CSS3, JavaScript
**Database**: SQLite (dev), PostgreSQL (prod)

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd skill-swap
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Run backend
python main.py
# Backend: http://127.0.0.1:8001

# Run frontend
cd frontend
python -m http.server 3002
# Frontend: http://127.0.0.1:3002
```

## Project Structure

```
skill-swap/
├── main.py              # FastAPI app
├── database.py          # DB config
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # DB operations
├── routers/             # API routes
├── frontend/            # Frontend files
├── requirements.txt      # Dependencies
├── Procfile            # Deployment config
└── README.md           # This file
```

## Configuration

Create `.env` from `.env.example`:

```env
DATABASE_URL=sqlite:///./skill_swap.db
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=["http://localhost:3002"]
```

## Deployment

### Render
1. Connect repo to Render
2. Set build: `pip install -r requirements.txt`
3. Set start: `gunicorn main:app --bind 0.0.0.0:$PORT`
4. Add env vars
5. Deploy

### Railway
1. Connect repo
2. Set env vars
3. Auto-deploy

## API Docs

- Swagger: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

### Main Endpoints

**Auth**:
- `POST /users/register` - Register
- `POST /users/login` - Login

**Skills**:
- `GET /api/skills/` - Get skills (filter by category)
- `POST /api/skills/` - Create skill
- `GET /api/skills/my-skills` - User's skills

**Exchanges**:
- `GET /api/exchanges/` - Get requests
- `POST /api/exchanges/request-skill` - Request skill
- `PATCH /api/exchanges/requests/{id}` - Update status

## Testing

```bash
# Run tests
pytest

# Manual testing
python test_ui_functionality.py
python test_category_filter.py
```

## Security

- JWT authentication
- Password hashing (bcrypt)
- CORS protection
- Input validation
- SQL injection prevention

## UI Features

- Responsive design
- Single-page app
- Real-time updates
- Category filtering
- Status indicators

## Status

**Complete**:
- User auth
- Skill management
- Exchange requests
- Category filtering
- Responsive UI
- API docs
- Deployment ready

**In Development**:
- Real-time notifications
- Advanced search

## Contributing

1. Fork
2. Feature branch
3. Commit & push
4. Pull request

## License

MIT License

---
**Built with for community skill sharing!**
