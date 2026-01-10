# 🚀 Vercel Deployment Guide - Skill Swap

## 🎯 **Why Vercel?**
- ✅ **FREE** - No credit card required
- ✅ **Easy** - One-click deployment
- ✅ **Fast** - Automatic deployments
- ✅ **HTTPS** - Free SSL certificate
- ✅ **GitHub Integration** - Auto-deploy on push

---

## 📋 **Step-by-Step Vercel Deployment**

### **Step 1: Create Vercel Account**

1. **Go to**: [https://vercel.com](https://vercel.com)
2. **Sign Up**: 
   - Click "Sign Up"
   - Choose "Continue with GitHub"
   - Authorize Vercel to access your GitHub
3. **Verify**: Email address (if required)

### **Step 2: Import Your Repository**

1. **Dashboard**: Click "Add New..." → "Project"
2. **Import**: 
   - Find `skill-swap` repository
   - Click "Import"
3. **Configure**: Vercel will auto-detect settings

### **Step 3: Project Configuration**

Vercel will show these settings (keep as-is):

```json
{
  "Framework Preset": "Other",
  "Root Directory": "./",
  "Build Command": "pip install -r requirements.txt",
  "Output Directory": "frontend",
  "Install Command": "pip install -r requirements.txt"
}
```

### **Step 4: Environment Variables**

Add these in Vercel dashboard:

```bash
DATABASE_URL=sqlite:///./skill_swap.db
SECRET_KEY=your-vercel-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["https://your-app-name.vercel.app", "https://your-app-name.vercel.app/*"]
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=production
```

**Important**: 
- Generate a strong `SECRET_KEY`
- Update `ALLOWED_ORIGINS` with your Vercel URL

### **Step 5: Deploy**

1. **Click**: "Deploy"
2. **Wait**: 2-3 minutes
3. **Success**: Your app is live!

---

## 🔧 **Alternative: Vercel CLI (Optional)**

If you prefer command line:

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd "c:/Users/Javy/Desktop/skill swap"
vercel --prod
```

---

## 🌐 **After Deployment**

### **Your Live URLs**
- **Main App**: `https://skill-swap-xxxx.vercel.app`
- **API Endpoints**: `https://skill-swap-xxxx.vercel.app/api/`
- **API Docs**: `https://skill-swap-xxxx.vercel.app/docs`

### **Update Frontend API URL**

In `frontend/script.js`, update this line:

```javascript
// Change to your Vercel URL
const API_BASE_URL = 'https://skill-swap-xxxx.vercel.app';
```

---

## 📁 **Files Added for Vercel**

### ✅ **vercel.json** (Configuration)
```json
{
  "version": 2,
  "name": "skill-swap",
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.9"
  }
}
```

### ✅ **Updated requirements.txt** (Vercel Compatible)
- All dependencies already included
- Python 3.9 compatible

---

## 🧪 **Testing Your Live App**

### **Backend API Tests**
```bash
# Test API docs
curl https://skill-swap-xxxx.vercel.app/docs

# Test user registration
curl -X POST https://skill-swap-xxxx.vercel.app/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Test login
curl -X POST https://skill-swap-xxxx.vercel.app/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### **Frontend Tests**
1. **Open**: Your Vercel URL
2. **Register**: Create new account
3. **Login**: With your credentials
4. **Add Skill**: Test "Python Expert" skill
5. **Verify**: Skill appears in My Skills

---

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### 1. Build Failed
**Problem**: Dependencies not installing
**Solution**: Check `requirements.txt` format
```txt
# Correct format
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

#### 2. Database Connection Error
**Problem**: Database URL incorrect
**Solution**: Use SQLite for Vercel (free)
```bash
DATABASE_URL=sqlite:///./skill_swap.db
```

#### 3. CORS Error
**Problem**: Frontend can't access API
**Solution**: Update ALLOWED_ORIGINS
```bash
ALLOWED_ORIGINS=["https://your-app-name.vercel.app"]
```

#### 4. 404 Not Found
**Problem**: API endpoints not accessible
**Solution**: Check vercel.json routes
```json
"routes": [
  {
    "src": "/api/(.*)",
    "dest": "/main.py"
  }
]
```

#### 5. 500 Server Error
**Problem**: Application not starting
**Solution**: Check Vercel logs
- Go to Vercel dashboard
- Click your project
- Check "Functions" tab for logs

---

## 🎯 **Success Checklist**

After deployment, verify:

- [ ] App accessible at Vercel URL
- [ ] API docs working: `/docs`
- [ ] User registration working
- [ ] Login working
- [ ] Add Skill form working
- [ ] "Python Expert" skill appears in My Skills
- [ ] No CORS errors
- [ ] Skills persisting

---

## 🔄 **Auto-Deploy Setup**

### **Automatic Deployments**
1. **Vercel Dashboard**: Your project → Settings → Git
2. **Enable**: "Automatic Deployments"
3. **Result**: Every GitHub push auto-deploys

### **Preview Deployments**
- **Feature Branches**: Auto-create preview URLs
- **Testing**: Test changes before production
- **Safe**: Production remains stable

---

## 🌟 **Vercel vs Render**

| Feature | Vercel | Render |
|----------|---------|---------|
| **Cost** | FREE | Free tier available |
| **Setup** | 2 minutes | 5-10 minutes |
| **Database** | SQLite (free) | PostgreSQL (free tier) |
| **SSL** | Free | Free |
| **Custom Domain** | Free | Paid |
| **Auto-Deploy** | Yes | Yes |
| **Preview URLs** | Yes | No |

---

## 🎉 **Congratulations!**

Your Skill Swap platform is now live on Vercel! 🚀

**Benefits:**
- ✅ **Free hosting** - No charges
- ✅ **Global CDN** - Fast worldwide
- ✅ **HTTPS** - Secure connection
- ✅ **Auto-deploy** - Git integration
- ✅ **Preview URLs** - Test safely

**Your Live URLs:**
- **App**: `https://skill-swap-xxxx.vercel.app`
- **API**: `https://skill-swap-xxxx.vercel.app/api/`
- **Docs**: `https://skill-swap-xxxx.vercel.app/docs`

**Share your live Skill Swap platform with the world!** 🌍
