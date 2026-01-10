# 🚀 Skill Swap Deployment Guide - Render.com

## 📋 Prerequisites
- GitHub account with your project repository
- Render.com account (free tier available)
- All deployment files ready (requirements.txt, Procfile, .env.example)

## 🔧 Step-by-Step Deployment Instructions

### Step 1: Push Code to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Ready for deployment - Add Skill functionality working"

# Add remote repository (replace YOUR_USERNAME/YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2: Setup Render.com Account
1. Go to [https://render.com](https://render.com)
2. Sign up/login with your GitHub account
3. Click "New +" button
4. Select "Web Service"

### Step 3: Connect Your Repository
1. **Connect Repository**: 
   - Choose "Build and deploy from a Git repository"
   - Select your GitHub repository
   - Click "Connect"

2. **Configure Deployment**:
   ```
   Name: skill-swap-api
   Environment: Python 3
   Branch: main
   Root Directory: (leave empty)
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn main:app --bind 0.0.0.0:$PORT --workers 3 --worker-class uvicorn.workers.UvicornWorker --timeout 120
   ```

### Step 4: Environment Variables Setup
1. **Add Environment Variables** in Render dashboard:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database_name
   SECRET_KEY=your-very-secure-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALLOWED_ORIGINS=["https://your-app-name.onrender.com", "https://your-app-name.onrender.com/*"]
   HOST=0.0.0.0
   PORT=8001
   ENVIRONMENT=production
   ```

2. **Database Setup** (Render provides PostgreSQL):
   - Render will automatically create PostgreSQL database
   - Copy the DATABASE_URL from Render dashboard
   - Update ALLOWED_ORIGINS with your Render URL

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-5 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

## 🔍 Verification Steps

### Backend API Test
```bash
# Test your deployed API
curl https://your-app-name.onrender.com/docs
```

### Frontend Update
Update your frontend `API_BASE_URL` in `script.js`:
```javascript
// Change from local to production
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

### Database Migration
```bash
# Run database migrations on Render
# Render will automatically run: alembic upgrade head
```

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### 1. Build Failed
**Problem**: Dependencies not installing
**Solution**: Check `requirements.txt` format
```txt
# Correct format
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

#### 2. Database Connection Error
**Problem**: DATABASE_URL incorrect
**Solution**: Use Render's PostgreSQL connection string
```
# Format provided by Render
postgresql://username:password@host:port/database_name
```

#### 3. CORS Error
**Problem**: Frontend can't access API
**Solution**: Update ALLOWED_ORIGINS
```
ALLOWED_ORIGINS=["https://your-app-name.onrender.com"]
```

#### 4. 502 Bad Gateway
**Problem**: App not starting
**Solution**: Check logs in Render dashboard
- Verify start command
- Check for missing environment variables

#### 5. 404 Not Found
**Problem**: API endpoints not accessible
**Solution**: Check API_BASE_URL in frontend
```javascript
// Update this line in script.js
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

## 📁 Final Project Structure
```
skill-swap/
├── main.py                 # FastAPI application
├── requirements.txt          # Python dependencies
├── Procfile               # Render deployment config
├── .env.example          # Environment variables template
├── alembic/             # Database migrations
├── routers/              # API endpoints
├── models/               # Database models
├── crud.py               # Database operations
├── frontend/             # Static frontend files
│   ├── index.html
│   ├── script.js
│   └── style_fixed.css
└── DEPLOYMENT_GUIDE.md   # This file
```

## 🎯 Success Checklist

After deployment, verify:

- [ ] Backend API accessible at `https://your-app-name.onrender.com/docs`
- [ ] Database connection working
- [ ] User registration/login working
- [ ] Add Skill functionality working
- [ ] My Skills page displaying skills
- [ ] No CORS errors in browser console
- [ ] Skills persisting in database

## 🌐 Live URL Setup

### Frontend Deployment Options

#### Option 1: GitHub Pages (Free)
1. Push `frontend/` folder to GitHub Pages branch
2. Enable GitHub Pages in repository settings
3. Update API_BASE_URL to your Render backend URL

#### Option 2: Netlify (Free)
1. Connect your GitHub repository to Netlify
2. Set publish directory to `frontend/`
3. Update API_BASE_URL in script.js

#### Option 3: Vercel (Free)
1. Import your GitHub repository
2. Configure to deploy `frontend/` folder
3. Update API_BASE_URL in script.js

## 📞 Support

If you encounter issues:

1. **Check Render Logs**: Dashboard → Your Service → Logs
2. **Verify Environment Variables**: Dashboard → Your Service → Environment
3. **Test API Locally**: Ensure backend works before deployment
4. **Check GitHub**: Ensure code is pushed to correct branch

## 🎉 Deployment Complete!

Once deployed, your Skill Swap application will be live at:
- **Backend**: `https://your-app-name.onrender.com`
- **Frontend**: Your chosen hosting platform

Users can:
- Register and login
- Add skills via functional form
- View their skills in My Skills page
- Request skill exchanges
- Manage their profile

**Congratulations! Your Skill Swap platform is now live!** 🚀
