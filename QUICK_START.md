# 🚀 Quick Start Guide - Windows

## Step 1: Install Python (If Not Already Installed)

1. Download Python 3.9+ from https://www.python.org/
2. During installation, **CHECK** "Add Python to PATH"
3. Click Install

## Step 2: Start the Application

### Option A: Easy Way (Recommended for Demo)
```bash
# Double-click run.bat in the project folder
run.bat
```

The batch file will:
- Create a virtual environment
- Install all dependencies
- Start the server

### Option B: Manual Way
```bash
# Open Command Prompt in the project folder

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

## Step 3: Open in Browser

After the server starts, go to:

```
http://localhost:8000/docs
```

Or open `frontend/index.html` directly in your browser.

## Step 4: Run Demo

### In Web Interface:

1. **Generate Test Plan**
   - URL will be pre-filled: `https://play.ezygamers.com/`
   - Click "🚀 Generate Test Plan"
   - Wait ~5 seconds
   - See 20 test cases generated

2. **Execute Tests**
   - Click "▶️ Execute Tests"
   - Watch the progress
   - Takes ~2-3 minutes
   - View comprehensive report

3. **Record Demo Video**
   - Use Windows Snip & Sketch or OBS to record
   - Show the entire flow above
   - Save as video.mp4

## Step 5: Troubleshooting

### "Python not found"
- Make sure Python is in PATH
- Restart Command Prompt

### "Port 8000 in use"
- Close other applications using port 8000
- Or edit `main.py` and change port to 8001

### "Module not found"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

## File Locations

```
Your Project Folder:
├── run.bat                     <- Double-click to start
├── main.py                     <- Backend code
├── frontend/
│   └── index.html             <- Open this in browser
├── reports/                   <- Test reports saved here
│   └── report_20260210_sample.json  <- Example report
├── artifacts/                 <- Test artifacts saved here
└── README.md                  <- Full documentation
```

## What to Show in Demo

✅ **Planning Phase** (30 sec)
- Click "Generate Test Plan"
- Show 20 test cases listed

✅ **Execution Phase** (2 min)
- Click "Execute Tests"
- Show loading indicator
- Tests running in background

✅ **Report Phase** (instant)
- See test statistics
- View pass/fail verdicts
- Check recommendations

## Tips for Demo

1. **Open dual screens/windows** to show:
   - Command prompt (backend running)
   - Browser (frontend)

2. **Speak clearly** - Explain what each step does

3. **Highlight key features**:
   - "20 tests generated automatically"
   - "Parallel execution with multiple agents"
   - "Comprehensive report with verdicts"

4. **Keep it simple** - Don't go into technical details

## Next: GitHub Upload

1. Create account on GitHub.com
2. Create new repository
3. Click "Upload files"
4. Select all files from your folder
5. Commit changes
6. Share the repository link

That's it! 🎉

---

For more details, see README.md
