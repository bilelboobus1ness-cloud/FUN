# 🚀 Deploy BLAAN Backend to Render.com

**Render** = Cloud platform that runs Python Flask apps for FREE (with optional paid tiers)

---

## 📋 What is Render?

| Feature | Details |
|---------|---------|
| **Cost** | FREE tier (perfect for testing) |
| **What it does** | Runs your Flask backend in the cloud |
| **Uptime** | 99.99% (reliable) |
| **Storage** | PostgreSQL, MongoDB-friendly |
| **Domain** | Free subdomain + custom domain support |
| **Deployment** | Auto-deploy from GitHub (1 click) |

**Example**: Your backend runs at `https://blaan-api.onrender.com`

---

## 🎯 Step-by-Step Deployment

### Step 1: Create Render Account (2 minutes)

**a) Go to https://render.com**

**b) Click "Sign Up"**
- Email: your email
- Password: strong password
- Click "Create Free Account"

**c) Verify email**
- Check inbox for verification link
- Click it

**✓ You now have a Render account**

---

### Step 2: Prepare Backend for Render (5 minutes)

Render needs 2 files from your backend:

#### File 1: `runtime.txt` (in `/backend/` folder)
```
python-3.11.0
```

**Why?** Tells Render which Python version to use

---

#### File 2: Update `requirements.txt` (already done, verify)
```
Flask==2.3.3
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.2
python-dotenv==1.0.0
bcrypt==4.1.1
pymongo==4.4.0
newsapi==0.1.2
requests==2.31.0
Pillow==10.0.0
email-validator==2.1.0
pytz==2023.3
gunicorn==21.2.0
```

**Why?** Render installs these packages automatically

---

### Step 3: Update `.env` Configuration (3 minutes)

Create (or update) `backend/.env` with these:

```
# Required for Render
FLASK_ENV=production
DEBUG=False

# Database - CHOOSE ONE:
# Option A: MongoDB Atlas (RECOMMENDED)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/blaan

# Option B: Local MongoDB (won't work on Render, skip this)
# MONGODB_URI=mongodb://localhost:27017

# API Keys
NEWSAPI_KEY=your_key_from_newsapi.org

# Optional: Notifications
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
GMAIL_EMAIL=your_email
GMAIL_PASSWORD=your_app_password

# JWT
JWT_SECRET_KEY=your-super-secret-key-12345
```

**⚠️ IMPORTANT**: 
- Use **MongoDB Atlas** (cloud) instead of local MongoDB
- Get free MongoDB Atlas account: https://www.mongodb.com/cloud/atlas

**How to get MongoDB Atlas URI:**
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free)
3. Create cluster
4. Click "Connect"
5. Copy connection string
6. Replace `<password>` with your password
7. Change `myFirstDatabase` to `blaan`

Example:
```
mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/blaan?retryWrites=true&w=majority
```

---

### Step 4: Push to GitHub (2 minutes)

Render deploys from GitHub automatically.

**a) Initialize git (if not already)**
```bash
cd /workspaces/FUN/blaan
git init
git add .
git commit -m "Ready for Render deployment"
```

**b) Create GitHub repo**
- Go to https://github.com/new
- Name: `blaan` (or anything)
- Public (free) or Private
- Create

**c) Connect local to GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/blaan.git
git branch -M main
git push -u origin main
```

**✓ Your code is now on GitHub**

---

### Step 5: Deploy on Render (5 minutes)

**a) Go to https://dashboard.render.com**

**b) Click "+ New +"** → Choose **"Web Service"**

**c) Connect GitHub**
- Click "Connect account"
- Authorize Render to access GitHub
- Select your `blaan` repository
- Click "Connect"

**d) Configure Service**

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `blaan-api` |
| **Environment** | `Python 3` |
| **Region** | `Oregon (us-west)` |
| **Branch** | `main` |
| **Root Directory** | `blaan/backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn main:app` |

**e) Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

```
FLASK_ENV = production
DEBUG = False
MONGODB_URI = mongodb+srv://user:pass@cluster.mongodb.net/blaan
NEWSAPI_KEY = your_newsapi_key
JWT_SECRET_KEY = your-secret-key-123
```

**f) Review & Deploy**

- Scroll down
- Click **"Create Web Service"**
- Watch the build happen (takes 2-3 minutes)

**✓ Backend is now LIVE!**

---

### Step 6: Get Your Backend URL (1 minute)

After deployment succeeds:

**a) Go to your service dashboard**
- You'll see a URL like: `https://blaan-api.onrender.com`

**b) Test it**
```bash
curl https://blaan-api.onrender.com/health
```

Should respond with:
```json
{
  "status": "✓ Connected",
  "database": "MongoDB",
  "message": "BLAAN API is running"
}
```

**✓ Backend is working!**

---

### Step 7: Connect Frontend to Backend (3 minutes)

**a) Update frontend `.env`**

File: `frontend/.env`
```
VITE_API_URL=https://blaan-api.onrender.com
```

**b) Update API calls in React**

File: `frontend/src/services/api.js` (or similar):
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});
```

**c) Commit and push**
```bash
cd /workspaces/FUN/blaan
git add .
git commit -m "Connect frontend to Render backend"
git push
```

**✓ Frontend now calls your live backend!**

---

### Step 8: Deploy Frontend to Netlify (5 minutes)

**a) Build React**
```bash
cd frontend
npm run build
```

Creates `dist/` folder

**b) Go to https://app.netlify.com**
- Sign up or login
- Click **"Add new site"** → **"Deploy manually"**
- Drag & drop the `frontend/dist/` folder
- Wait ~1 minute

**c) You get a URL**
- Example: `https://blaan-abc123.netlify.app`

**✓ Frontend is LIVE!**

---

## 📊 Your Architecture Now

```
┌─────────────────────────────────────────┐
│  User opens: https://blaan-xyz.netlify.app
│         (Frontend - Netlify)
└──────────────────┬──────────────────────┘
                   │
                ↓ API calls
                   │
┌──────────────────▼──────────────────────┐
│  https://blaan-api.onrender.com
│       (Backend - Render)
└──────────────────┬──────────────────────┘
                   │
                ↓ Database queries
                   │
┌──────────────────▼──────────────────────┐
│  MongoDB Atlas (Cloud Database)
│     mongodb+srv://...
└──────────────────────────────────────────┘
```

---

## ✅ Testing Your Live System

### Test 1: Health Check
```bash
curl https://blaan-api.onrender.com/health
```

Should return database status ✓

### Test 2: Register User
```bash
curl -X POST https://blaan-api.onrender.com/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@test.com",
    "password": "TestPass123",
    "full_name": "Test User"
  }'
```

Should return `✓ Registration successful`

### Test 3: Get News
```bash
curl https://blaan-api.onrender.com/api/news/categorized
```

Should return real forex news from NewsAPI

### Test 4: Load Frontend
```
Open: https://your-netlify-url.netlify.app
Click "Register"
Fill in form
Click "Login"
See dashboard
```

---

## 🐛 Troubleshooting

### Backend Deploy Fails

**Problem**: Build fails with Python error

**Solution**:
1. Check `requirements.txt` is in `backend/` folder
2. Check `runtime.txt` has Python version
3. Check `main.py` is in `backend/` folder
4. Go to Render dashboard → Logs tab → see what's wrong

---

### "Cannot connect to database"

**Problem**: API returns database connection error

**Solution**:
1. Check MONGODB_URI is correct
2. Make sure `<password>` doesn't have special characters
   - If it does: URL-encode it
   - Example: `pass@word` → `pass%40word`
3. In MongoDB Atlas: Network Access → Allow All IPs
4. Test connection: `curl /health`

---

### Frontend calls are 404

**Problem**: API returns 404 errors

**Solution**:
1. Check `VITE_API_URL` in frontend `.env`
2. Check URL matches Render domain
3. Check backend is actually running (visit /health)
4. Check CORS is enabled (should be by default)

---

### Slow API Responses

**Problem**: Requests take 5+ seconds

**Likely causes**:
1. Render free tier is "spinning down" (wakes after 15 min idle)
2. NewsAPI is slow (takes 2-3 seconds)
3. MongoDB query is slow

**Solution**:
1. Upgrade to Render paid ($7/month) to prevent spindown
2. Or: Accept slow first request (subsequent ones are fast)
3. Use caching for news data

---

## 💰 Costs

### FREE Plan (Recommended for testing)
- Frontend: Netlify (free forever)
- Backend: Render (free, but sleeps after 15 min)
- Database: MongoDB Atlas (free, 512MB)
- **Total: $0/month**
- ⚠️ First request after sleep takes 30 seconds

### PAID Plan (Recommended for real use)
- Frontend: Netlify (free)
- Backend: Render paid tier ($7/month) - no sleep
- Database: MongoDB Atlas (free)
- **Total: $7/month**
- ✓ Instant responses always

---

## 🎯 Your Live BLAAN Platform

After following all steps:

```
✓ Backend running on Render
✓ Frontend running on Netlify
✓ Database on MongoDB Atlas
✓ Automatic deployments from GitHub
✓ Free SSL/HTTPS
✓ Auto-restart if crashes
✓ Real-time logs
✓ NewAPI integration LIVE
✓ User authentication REAL
✓ Risk calculations WORKING
```

---

## 📝 Quick Checklist

- [ ] Created Render account
- [ ] Created MongoDB Atlas account
- [ ] Created GitHub repo
- [ ] Pushed code to GitHub
- [ ] Deployed backend to Render
- [ ] Added environment variables to Render
- [ ] Tested `/health` endpoint
- [ ] Deployed frontend to Netlify
- [ ] Updated frontend API URL
- [ ] Tested registration/login
- [ ] Tested news API
- [ ] Tested in browser

---

## 🎉 You're Done!

Your BLAAN trading platform is now LIVE on the internet!

**Share your app:**
```
"Check out my trading platform: https://your-netlify-url.netlify.app"
```

**Monitor your app:**
- Render dashboard: See logs, restart if needed
- Netlify dashboard: See deployments, speed metrics
- MongoDB Atlas: See database usage

**Next steps (Optional):**
- Add custom domain
- Set up CI/CD pipeline
- Add more features
- Scale to paid tier

---

**Questions?** Check logs:
1. Render: Dashboard → Logs
2. Netlify: Deploys → Logs
3. MongoDB: Activity Feed

Happy trading! 📈
