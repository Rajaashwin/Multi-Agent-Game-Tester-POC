# Deployment Guide: GitHub & Render

This guide walks you through deploying the Multi-Agent Game Tester POC on **GitHub** and **Render** (recommended). The repo is configured to run the backend with `uvicorn` and serve the frontend static files from the same service at `/app`.

## Prerequisites

1. Git installed on your machine
2. GitHub account
3. Render account (free tier available at https://render.com)
4. GitHub CLI (optional but recommended) or standard Git flow

---

## Step 1: Project Preparation (Already Done ✓)

The following have been configured:
- ✅ `.gitignore` - excludes `venv/`, `.env`, `__pycache__/`, etc.
- ✅ `.env.example` - template for environment variables
- ✅ `render.yaml` - Render service manifest (optional)
- ✅ `main.py` / `api/index.py` - configured to mount `frontend/` at `/app` and use `FRONTEND_URL` for CORS
- ✅ `frontend/index.html` - frontend uses same-origin API URL when served from the Render service

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

## Step 3: Deploy Backend & Frontend on Render (recommended)

1. **Create a Render account:** https://render.com and connect your GitHub account.

2. **Import the repository or create a new Web Service:**
   - Choose **Web Service (Static/Server)** and point to this repository and `master` branch.
   - If using `render.yaml`, import the manifest or let Render detect settings.

3. **Build & Start commands:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.index:app --host 0.0.0.0 --port $PORT`

4. **Environment variables:**
   - `FRONTEND_URL` = `https://<your-render-service>.onrender.com` (the public URL Render gives you)
   - `ENVIRONMENT` = `production`

5. **Deploy:** Trigger a deploy; after build completes open `<your-render-service>/app` to see the UI.

6. **Verify health:**
   ```bash
   curl https://<your-render-service>/health
   # should return {"status":"healthy"}
   ```

---

## Step 4: Local testing

1. Create and activate a virtualenv, install deps, and run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.index:app --reload
# open http://localhost:8000/app
```

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

1. **Open Frontend (Render):**
   - `https://<your-render-service>/app`

2. **Test the Workflow:**
   - Enter game URL (or use default: `https://play.ezygamers.com/`)
   - Click **"Generate Plan"** → Should generate test cases
   - Click **"Execute Tests"** → Should execute and return a report
   - Click **"View Latest Report"** → Should display JSON report with artifacts

3. **Verify No CORS Errors:**
   - Open browser DevTools (F12)
   - Check Console tab for errors and Network tab for successful API calls

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

- **Frontend + Backend (Render):** `https://<your-render-service>` (frontend available at `/app`)
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
