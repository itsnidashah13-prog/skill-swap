# 🚀 Render.com Deployment - Complete Guide

## ✅ **Current Status**
- **Backend API**: ✅ Fully working (POST/GET endpoints tested)
- **Database**: ✅ PostgreSQL ready (14 skills including "Python Expert")
- **Frontend**: ✅ Updated to use backend API
- **Deployment Files**: ✅ All ready

---

## 📋 **Step-by-Step Render Deployment**

### **Step 1: GitHub Repository Setup**

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Skill Swap - Ready for Render deployment"

# Add your GitHub repository (replace YOUR_USERNAME/YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### **Step 2: Create Render Account**

1. Go to [https://render.com](https://render.com)
2. **Sign up** with your GitHub account
3. **Verify** your email address
4. **Click** "New +" button

### **Step 3: Create Web Service**

1. **Select**: "Web Service"
2. **Connect Repository**: 
   - Choose "Build and deploy from a Git repository"
   - Select your GitHub repository
   - Click "Connect"

3. **Configure Settings**:
   ```
   Name: skill-swap-api
   Environment: Python 3
   Branch: main
   Root Directory: (leave empty)
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn main:app --bind 0.0.0.0:$PORT --workers 3 --worker-class uvicorn.workers.UvicornWorker --timeout 120
   ```

### **Step 4: Environment Variables**

In Render dashboard → Your Service → Environment, add:

```bash
DATABASE_URL=postgresql://[get-from-render-dashboard]
SECRET_KEY=your-super-secure-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["https://your-app-name.onrender.com"]
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=production
```

**Important**: 
- Copy `DATABASE_URL` from Render's PostgreSQL service
- Generate a strong `SECRET_KEY`
- Update `ALLOWED_ORIGINS` with your Render URL

### **Step 5: Database Setup**

1. **Create PostgreSQL Database**:
   - In Render dashboard: "New +" → "PostgreSQL"
   - Name: `skill-swap-db`
   - Wait for database to be ready
   - Copy the `DATABASE_URL` from database settings

2. **Run Database Migrations**:
   - Render will automatically run: `alembic upgrade head`
   - Or manually run in Render shell if needed

### **Step 6: Deploy**

1. **Click**: "Create Web Service"
2. **Wait**: 2-5 minutes for deployment
3. **Check**: Status becomes "Live"
4. **Access**: Your API at `https://your-app-name.onrender.com`

---

## 🔧 **Post-Deployment Setup**

### **Update Frontend API URL**

In `frontend/script.js`, update this line:

```javascript
// Change from local to your Render URL
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

### **Deploy Frontend (Choose One)**

#### Option 1: GitHub Pages (Free)
```bash
# Create gh-pages branch
git checkout --orphan gh-pages
git rm -rf .
cp -r frontend/* .
git add .
git commit -m "Deploy frontend to GitHub Pages"
git push origin gh-pages
```

#### Option 2: Netlify (Free)
1. Go to [https://netlify.com](https://netlify.com)
2. Connect your GitHub repository
3. Set publish directory: `frontend/`
4. Deploy

#### Option 3: Vercel (Free)
1. Go to [https://vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set output directory: `frontend/`
4. Deploy

---

## 🧪 **Testing Your Live App**

### **Backend API Tests**

```bash
# Test API docs
curl https://your-app-name.onrender.com/docs

# Test user registration
curl -X POST https://your-app-name.onrender.com/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Test login
curl -X POST https://your-app-name.onrender.com/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### **Frontend Tests**

1. **Open**: Your frontend URL
2. **Register**: Create new account
3. **Login**: With your credentials
4. **Add Skill**: Test "Python Expert" skill
5. **Verify**: Skill appears in My Skills

---

## 📁 **Deployment Files Verification**

### ✅ **requirements.txt** (Complete)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pyodbc==5.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
gunicorn==21.2.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

### ✅ **Procfile** (Complete)
```procfile
web: gunicorn main:app --bind 0.0.0.0:$PORT --workers 3 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100
```

### ✅ **.env.example** (Complete)
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "https://your-app-name.onrender.com"]
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=development
```

---

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### 1. Build Failed
- **Check**: `requirements.txt` format
- **Fix**: Ensure exact package names and versions

#### 2. Database Connection Error
- **Check**: `DATABASE_URL` format
- **Fix**: Use Render's PostgreSQL connection string

#### 3. CORS Error
- **Check**: `ALLOWED_ORIGINS` environment variable
- **Fix**: Include your Render URL

#### 4. 502 Bad Gateway
- **Check**: Render logs for startup errors
- **Fix**: Verify all environment variables

#### 5. Frontend Not Connecting
- **Check**: `API_BASE_URL` in script.js
- **Fix**: Update to your Render URL

---

## 🎯 **Success Checklist**

After deployment, verify:

- [ ] Backend API accessible: `https://your-app-name.onrender.com/docs`
- [ ] Database connection working
- [ ] User registration/login working
- [ ] Add Skill form working
- [ ] "Python Expert" skill appears in My Skills
- [ ] No CORS errors in browser
- [ ] Skills persisting in database

---

## 🌐 **Your Live URLs**

After successful deployment:

- **Backend API**: `https://your-app-name.onrender.com`
- **API Documentation**: `https://your-app-name.onrender.com/docs`
- **Frontend**: Your chosen hosting platform

---

## 🎉 **Congratulations!**

Your Skill Swap platform is now live! Users can:

- ✅ Register and login
- ✅ Add skills via functional form
- ✅ View skills in My Skills page
- ✅ Request skill exchanges
- ✅ Manage their profile

**Ready to share your live Skill Swap platform!** 🚀
