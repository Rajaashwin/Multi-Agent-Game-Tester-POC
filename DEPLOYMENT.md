# Deployment Guide: GitHub & Vercel

This guide walks you through deploying the Multi-Agent Game Tester POC on **GitHub** and **Vercel** following a similar pattern shown in the Vercel deployment video.

## Prerequisites

1. Git installed on your machine
2. GitHub account
3. Vercel account (free tier available at https://vercel.com)
4. GitHub CLI (optional but recommended) or standard Git flow

---

## Step 1: Project Preparation (Already Done ✓)

The following have been configured:
- ✅ `.gitignore` - excludes `venv/`, `.env`, `__pycache__/`, etc.
- ✅ `.env.example` - template for environment variables
- ✅ `vercel.json` - FastAPI/Python build configuration
- ✅ `main.py` - updated to use environment variables for CORS
- ✅ `frontend/index.html` - frontend automatically detects backend URL

---

## Step 2: Push to GitHub

### Option A: Using GitHub CLI (Recommended - Quickest)

```powershell
# Navigate to project directory
cd "f:\Intern Multi-Agent Game Tester POC"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-Agent Game Tester POC"

# Create repository on GitHub and push
gh repo create multi-agent-game-tester --public --source=. --remote=origin --push
```

### Option B: Using Standard Git (Manual Steps)

```powershell
# Navigate to project directory
cd "f:\Intern Multi-Agent Game Tester POC"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-Agent Game Tester POC"

# Add GitHub remote (replace YOUR_USERNAME and repo name)
git remote add origin https://github.com/YOUR_USERNAME/multi-agent-game-tester.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**After pushing, your repository URL will be:** `https://github.com/YOUR_USERNAME/multi-agent-game-tester`

---

## Step 3: Deploy Backend on Vercel

1. **Go to Vercel Dashboard:**
   - Visit https://vercel.com/dashboard
   - Click **"Add New..."** → **"Project"**

2. **Import from GitHub:**
   - Click **"Import Project"**
   - Paste your GitHub repository URL or select from list
   - Click **"Import"**

3. **Configure Build Settings:**
   - **Project Name:** `multi-agent-game-tester-backend` (or your choice)
   - **Framework Preset:** Select **"Other"** (since Vercel auto-detects Python)
   - **Root Directory:** Keep as default (project root)

4. **Add Environment Variables:**
   - Click **"Environment Variables"**
   - Add: `FRONTEND_URL` = `https://<your-frontend-url-will-go-here>.vercel.app`
     (You'll update this after deploying frontend - for now use placeholder like `https://frontend-tbd.vercel.app`)
   - Click **"Deploy"**

5. **Wait for Deployment:**
   - Vercel will build and deploy your backend
   - You'll get a URL like: `https://multi-agent-game-tester-backend.vercel.app`
   - **Save this URL** - you need it for frontend deployment

6. **Test Backend (Optional):**
   ```
   curl https://multi-agent-game-tester-backend.vercel.app/health
   ```
   Should return: `{"status":"healthy"}`

---

## Step 4: Deploy Frontend on Vercel

1. **Create a New Project in Vercel:**
   - Go to https://vercel.com/dashboard
   - Click **"Add New..."** → **"Project"**

2. **Import Same Repository:**
   - Click **"Import Project"**
   - Select your `multi-agent-game-tester` repository
   - Click **"Import"**

3. **Configure for Frontend:**
   - **Project Name:** `multi-agent-game-tester-frontend`
   - **Framework Preset:** Detect `Other` (static files)
   - **Root Directory:** Click **"Edit"** → Change to `frontend`
   - **Build Command:** Leave blank (no build needed for static)
   - **Output Directory:** Leave blank

4. **Add Environment Variables:**
   - Click **"Environment Variables"**
   - Add: `REACT_APP_API_URL` = (Optional - our frontend auto-detects)
   - Click **"Deploy"**

5. **Get Frontend URL:**
   - After deployment completes, you'll get: `https://multi-agent-game-tester-frontend.vercel.app`

---

## Step 5: Link Backend & Frontend

1. **Update Backend with Frontend URL:**
   - Go to backend project in Vercel: `https://vercel.com/dashboard`
   - Click your **backend project**
   - Go to **Settings** → **Environment Variables**
   - Update `FRONTEND_URL` with your actual frontend URL:
     ```
     FRONTEND_URL=https://multi-agent-game-tester-frontend.vercel.app
     ```
   - Click **Save**

2. **Redeploy Backend (Important!):**
   - Go to **Deployments** tab
   - Click the latest deployment
   - Click **"Redeploy"**
   - Wait for deployment to complete

---

## Step 6: Final Testing

1. **Open Frontend:**
   ```
   https://multi-agent-game-tester-frontend.vercel.app
   ```

2. **Test the Workflow:**
   - Enter game URL (or use default: `https://play.ezygamers.com/`)
   - Click **"Generate Plan"** → Should generate 20 test cases
   - Click **"Execute Tests"** → Should execute top 10 and return report
   - Click **"View Latest Report"** → Should display JSON report with artifacts

3. **Verify No CORS Errors:**
   - Open browser DevTools (F12)
   - Check Console tab - should have no CORS errors
   - Check Network tab - API calls should show 200/success

---

## Troubleshooting

### CORS Errors
If you see CORS errors in the browser console:
1. Verify `FRONTEND_URL` environment variable on backend is correct
2. Redeploy the backend after updating environment variable
3. Clear browser cache (Ctrl+Shift+Delete)

### Backend Not Responding
1. Check backend deployment logs in Vercel dashboard
2. Verify all dependencies are in `requirements.txt`
3. Check that `main.py` is at project root

### Import Errors (Python Package Issues)
If backend fails to import modules:
1. Ensure `requirements.txt` includes all dependencies:
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   python-dotenv==1.0.0
   pydantic==2.5.0
   langchain==0.1.10
   ```
2. Check that `src/` package structure is correct with `__init__.py` files
3. Redeploy backend

---

## URLs After Deployment

- **Frontend:** `https://multi-agent-game-tester-frontend.vercel.app`
- **Backend API:** `https://multi-agent-game-tester-backend.vercel.app`
- **GitHub Repository:** `https://github.com/YOUR_USERNAME/multi-agent-game-tester`

---

## Demo Video Script

For your demo video, follow this flow:

1. **Show Frontend Loading** (5 sec)
   - Open deployed frontend URL
   - Show the clean UI

2. **Generate Plan** (10 sec)
   - Click "Generate Plan"
   - Show planning progress
   - Display 20 generated test cases

3. **Execute Tests** (15 sec)
   - Click "Execute Tests"
   - Show top 10 tests being executed
   - Mention: "Would execute 10 tests in production"

4. **View Report** (20 sec)
   - Click "View Latest Report"
   - Show JSON report structure:
     - Test execution summary
     - Pass/fail statistics
     - Individual test results
     - Artifacts (screenshots, DOM, console logs)

5. **Highlight Key Features** (10 sec)
   - Show verdicts and recommendations
   - Explain cross-agent validation
   - Demo reproducibility scores

**Total demo length:** ~60 seconds

---

## Quick Recap Checklist

- [ ] Git initialized and `.gitignore` configured
- [ ] Code pushed to GitHub
- [ ] Backend deployed on Vercel with `FRONTEND_URL` set
- [ ] Frontend deployed on Vercel
- [ ] Backend environment variable updated with actual frontend URL
- [ ] Backend redeployed after env var update
- [ ] Frontend loads and API calls succeed (check browser console)
- [ ] Demo video recorded and saved
- [ ] GitHub repository link ready for submission
- [ ] Demo video link ready for submission

---

## Questions?

Refer to:
- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Docs](https://docs.github.com/)
