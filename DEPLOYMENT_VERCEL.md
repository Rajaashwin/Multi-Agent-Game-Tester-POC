# Deployment Guide: GitHub + Vercel

This guide walks you through deploying the Multi-Agent Game Tester POC to GitHub and Vercel.

## Step 1: Push to GitHub

### Prerequisites
- GitHub account (create one at https://github.com/signup if you don't have one)
- Git installed on your machine (https://git-scm.com/download/win for Windows)

### Option A: Using GitHub CLI (Fastest)
If you have GitHub CLI installed:
```powershell
cd 'F:\Intern Multi-Agent Game Tester POC'
gh auth login
gh repo create multi-agent-game-tester --public --source=. --remote=origin
git push -u origin main
```

### Option B: Using Web UI (Manual)
1. Go to https://github.com/new
2. Create a new repository named `multi-agent-game-tester`
3. Set it to **Public**
4. Click "Create repository"
5. In PowerShell, run:
```powershell
cd 'F:\Intern Multi-Agent Game Tester POC'
git remote add origin https://github.com/YOUR_USERNAME/multi-agent-game-tester.git
git branch -M main
git push -u origin main
```
(Replace `YOUR_USERNAME` with your actual GitHub username)

### Verify GitHub Push
- Go to https://github.com/YOUR_USERNAME/multi-agent-game-tester
- You should see all your code files

---

## Step 2: Deploy Backend to Vercel

### Prerequisites
- Vercel account (sign up at https://vercel.com with GitHub account)
- GitHub repository pushed (Step 1 complete)

### Steps
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Click "Import" next to your `multi-agent-game-tester` repository
4. **Project Settings:**
   - Framework Preset: `Other` (FastAPI doesn't need a preset)
   - Root Directory: `./` (or leave empty)
   - Build Command: Leave empty or `pip install -r requirements.txt`
   - Output Directory: Leave empty
5. Click "Environment Variables" and add:
   - Name: `FRONTEND_URL`
   - Value: (leave empty for now, you'll update it after frontend deploys)
   - Name: `ENVIRONMENT`
   - Value: `production`
6. Click "Deploy"
7. Wait for deployment to complete (~2-3 minutes)
8. Copy your backend URL (e.g., `https://your-project-name.vercel.app`)

---

## Step 3: Deploy Frontend to Vercel

### Steps
1. In Vercel Dashboard, click "Add New..." → "Project" again
2. Import the same `multi-agent-game-tester` repository again
3. **Project Settings:**
   - Framework Preset: `Other`
   - Root Directory: `frontend` ← **IMPORTANT: Set this to `frontend`**
   - Build Command: Leave empty (static HTML)
   - Output Directory: `.` (current directory)
4. Click "Environment Variables" and add:
   - Name: `BACKEND_URL`
   - Value: `https://your-project-name.vercel.app` (the backend URL from Step 2)
5. Click "Deploy"
6. Wait for frontend deployment (~1-2 minutes)
7. Copy your frontend URL (e.g., `https://your-frontend-name.vercel.app`)

---

## Step 4: Link Frontend & Backend

### Update Backend with Frontend URL
1. Go to your **Backend** project in Vercel Dashboard
2. Go to "Settings" → "Environment Variables"
3. Update `FRONTEND_URL`:
   - Name: `FRONTEND_URL`
   - Value: `https://your-frontend-name.vercel.app` (from Step 3)
4. Go to "Deployments" and click "Redeploy" on the latest deployment
5. Wait for redeployment complete

### Update Frontend with Backend URL
1. Go to your **Frontend** project in Vercel Dashboard
2. Go to "Settings" → "Environment Variables"
3. Verify `BACKEND_URL` is set to your backend URL
4. If needed, update and redeploy

---

## Step 5: Test the Deployment

1. Open your fronted URL: `https://your-frontend-name.vercel.app`
2. You should see the Game Tester UI
3. Click "Generate Plan" → should generate 20 test cases
4. Click "Execute Tests" → should run workflow and display report
5. If API calls fail (CORS errors in browser console), ensure:
   - Backend `FRONTEND_URL` is correctly set to your frontend domain
   - Frontend API calls point to your backend URL

---

## Troubleshooting

### CORS Errors
- Ensure backend environment variable `FRONTEND_URL` matches your frontend domain
- Check [`main.py`](main.py) to verify CORS configuration includes production Vercel domains

### 404 on API Calls
- Verify backend is deployed and responding at `https://your-backend.vercel.app/health`
- Check Vercel logs: Backend Project → "Deployments" → Click latest → "Logs"

### Frontend Won't Load
- Ensure `root` directory is set to `frontend` in Vercel project settings
- Check that `frontend/index.html` exists in your repository

### Port Issues Locally
- If testing locally, ensure `.env` file has:
  ```
  FRONTEND_URL=http://localhost:3000
  ENVIRONMENT=development
  ```

---

## Local Testing Before Deployment

To test locally before deploying:

```powershell
cd 'F:\Intern Multi-Agent Game Tester POC'
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then open: `http://localhost:8000/app`

---

## Files Modified for Deployment

- `main.py` - Added environment variable support for CORS
- `vercel.json` - Configuration for Vercel Python hosting
- `.env.example` - Example environment variables
- `.gitignore` - Excludes `.env` and secrets

---

## Need Help?

- GitHub Issues: https://github.com/YOUR_USERNAME/multi-agent-game-tester/issues
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/
