Render deployment steps (quick)

1) Create a Render account (https://render.com) and connect your GitHub/Git provider.

2) Import the repository or create a new Web Service with the following settings:
   - Environment: `Python`
   - Branch: `master`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.index:app --host 0.0.0.0 --port $PORT`
   - Python Version: `3.12` (matches `runtime.txt`)
   - Plan: `Free` (or choose another)

3) Add environment variables on Render (Dashboard -> Environment):
   - `FRONTEND_URL` = your frontend URL (e.g., `https://<your-frontend>.onrender.com`)
   - `ENVIRONMENT` = `production`

4) (Optional) Use the provided `render.yaml` in the repo to import the service configuration.
   - If you use `render.yaml`, replace the `repo` field with your repo URL before importing.

5) Redeploy / trigger a manual deploy. After the build completes, open the Service URL.

6) Update frontend configuration (if needed):
   - Ensure the frontend `API_URL` points to the Render service domain (e.g., `https://multi-agent-game-tester-api.onrender.com`).

Local test commands (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.index:app --reload
# open http://localhost:8000/app
```

Notes:
- This keeps your repo small and demonstrates a production-like deployment in your submission.
- If you want, I can also prepare a short README section for the project README.md with these steps.
