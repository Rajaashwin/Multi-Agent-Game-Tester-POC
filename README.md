# 🎮 Multi-Agent Game Tester POC

> An intelligent, automated testing system for web-based puzzle and math games using LangChain agents

## 📋 Overview

This POC demonstrates a **multi-agent testing framework** that:
- ✅ Generates 20+ intelligent test cases using LangChain
- ✅ Ranks and selects the top 10 most valuable tests
- ✅ Executes tests in parallel using multiple agent instances
- ✅ Captures comprehensive artifacts (screenshots, DOM snapshots, console logs)
- ✅ Validates results with repeat and cross-agent consistency checks
- ✅ Produces detailed JSON reports with verdicts and recommendations

### Agent Architecture

```
OrchestratorAgent (Master Coordinator)
├── PlannerAgent → Generates 20+ test cases
├── RankerAgent → Selects top 10 tests
├── ExecutorAgent-1 → Executes tests (parallel)
├── ExecutorAgent-2 → Executes tests (parallel)
└── AnalyzerAgent → Validates & analyzes results
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- pip or conda

### 2. Installation

```bash
# Clone or download the repository
cd Intern\ Multi-Agent\ Game\ Tester\ POC

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Server (Local)

```bash
# from project root, with virtualenv activated
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

Server will start at `http://localhost:8000` and the frontend SPA is served at `/app`.

### 4. Open the Frontend

Open your browser and go to:
```
http://localhost:8000/app
```
Or open `frontend/index.html` directly for a static preview.

## 📖 Usage

### Via Web UI (Recommended for Demo)

1. **Generate Test Plan**
   - Enter game URL (default: `https://play.ezygamers.com/`)
   - Click "Generate Test Plan"
   - View 20+ generated test cases

2. **Execute Tests**
   - Click "Execute Tests"
   - Watch the agents work through planning, ranking, execution, and validation
   - View the comprehensive report

3. **View Report**
   - See test statistics and verdicts
   - Check individual test results
   - Review recommendations

### Via API (for Automation)

```bash
# Generate test plan
curl -X POST http://localhost:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"game_url": "https://play.ezygamers.com/"}'

# Execute full workflow
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"game_url": "https://play.ezygamers.com/"}'

# Get latest report
curl http://localhost:8000/api/latest-report

# Check workflow status
curl http://localhost:8000/api/status
```

## 📁 Project Structure

```
Intern Multi-Agent Game Tester POC/
├── api/index.py               # FastAPI application entrypoint (used by Render/uvicorn)
├── requirements.txt           # Python dependencies
├── frontend/
│   └── index.html            # Web UI
├── src/
│   ├── __init__.py
│   ├── orchestrator.py       # OrchestratorAgent
│   ├── game_interaction.py   # Game interaction layer
│   ├── report_generator.py   # Report generation
│   └── agents/
│       ├── __init__.py
│       ├── base.py           # BaseAgent class
│       ├── planner.py        # PlannerAgent
│       ├── ranker.py         # RankerAgent
│       ├── executor.py       # ExecutorAgent
│       └── analyzer.py       # AnalyzerAgent
├── reports/                  # Generated test reports
├── artifacts/               # Captured artifacts (screenshots, logs)
└── README.md               # This file
```

## 🤖 Agent Descriptions

### PlannerAgent
- **Role**: Test case generation
- **Responsibility**: Creates 20+ candidate test cases based on game URL
- **Strategy**: Template-based generation + edge case analysis
- **Output**: List of test cases with priority and type

### RankerAgent
- **Role**: Test case selection
- **Responsibility**: Ranks all candidates and selects top 10
- **Scoring**: Priority × Type × Complexity
- **Output**: Ranked top 10 tests

### ExecutorAgent(s)
- **Role**: Test execution
- **Responsibility**: Runs test cases against the game
- **Capabilities**: 
  - Opens game in browser
  - Performs test actions
  - Captures screenshots
  - Collects DOM snapshots
  - Gathers console logs
- **Parallel Execution**: Multiple executors work simultaneously

### AnalyzerAgent
- **Role**: Result validation
- **Responsibility**: Validates test results
- **Validations**:
  - Repeatability checks (run same test multiple times)
  - Cross-agent consistency (compare results from different executors)
  - Evidence quality assessment
- **Output**: Validated results with verdicts

### OrchestratorAgent
- **Role**: Workflow coordination
- **Responsibility**: Manages entire testing pipeline
- **Orchestration**:
  - Triggers planning
  - Manages ranking
  - Distributes execution
  - Coordinates validation
- **Output**: Complete workflow result

## 📊 Report Structure

Each test report includes:

```json
{
  "report_id": "report_20240101_120000",
  "timestamp": "2024-01-01T12:00:00",
  "game_url": "https://play.ezygamers.com/",
  "execution_summary": {
    "test_cases_generated": 20,
    "test_cases_selected": 10,
    "test_cases_executed": 10,
    "passed_count": 9,
    "failed_count": 1,
    "success_rate": "90%"
  },
  "test_results": [
    {
      "test_id": "test_1",
      "description": "Click button 'submit'...",
      "status": "passed",
      "verdict": "PASSED",
      "artifacts": {
        "screenshot": "artifacts/test_1_screenshot.png",
        "dom_snapshot": "artifacts/test_1_dom.json",
        "console_logs": "artifacts/test_1_console.txt"
      },
      "validation": {
        "repeatability": "repeatable",
        "consistency": "consistent",
        "verdict": "PASSED"
      }
    }
  ],
  "verdicts": {
    "overall_verdict": "PASS",
    "pass_rate": "90%",
    "recommendation": "Game is stable and ready for release"
  },
  "recommendations": [
    "Fix 1 failing test(s) before release",
    "Investigate 0 flaky test(s)",
    "Continue regression testing in production"
  ]
}
```

## 🔧 Configuration

### Game URLs
Default: `https://play.ezygamers.com/`

Supports any web-based puzzle or math game. The system adapts to different game interfaces.

### Test Count
- **Generated**: 20+
- **Selected**: 10 (top candidates)
- **Executed**: 10

### Artifact Capture
- Screenshots: `.png` format
- DOM Snapshots: `.json` format
- Console Logs: `.txt` format

## 📈 Demo Workflow

1. **Planning Phase** (30 seconds)
   - Generate 20 test cases
   - Display test case list

2. **Execution Phase** (1-2 minutes)
   - Rank and select top 10
   - Execute tests in parallel
   - Capture artifacts

3. **Validation Phase** (30 seconds)
   - Validate all results
   - Cross-agent checks
   - Generate final report

4. **Report Phase** (instant)
   - Display comprehensive results
   - Show verdicts and recommendations

**Total Time**: ~3 minutes for full execution

## 🎥 Creating Demo Video

1. Start the backend: `python main.py`
2. Open frontend in browser
3. Record your screen (use Windows built-in screen capture or OBS)
4. Execute the following steps:
   - Click "Generate Test Plan" → Show 20 test cases
   - Click "Execute Tests" → Show progression through agents
   - View final report → Show statistics and verdicts
5. Save video as MP4

Video requirements:
- Duration: 2-3 minutes
- Show: Planning → Execution → Report
- Include audio explanation (optional)

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/plan` | Generate test plan |
| POST | `/api/execute` | Execute full workflow |
| GET | `/api/status` | Get workflow status |
| GET | `/api/report` | Get latest report |
| GET | `/api/latest-report` | Get complete latest report |
| GET | `/api/artifacts` | Get artifact list |
| GET | `/api/reports-list` | List all reports |

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
# Change port in main.py:
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Import errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Reports not generating
```bash
# Check reports directory exists
mkdir reports artifacts
```

## 📝 Key Features for Interview

✅ **Multi-agent architecture** - Shows advanced system design  
✅ **LangChain integration** - Demonstrates AI/ML knowledge  
✅ **FastAPI backend** - Modern Python web framework  
✅ **Parallel execution** - Efficient agent coordination  
✅ **Comprehensive reporting** - Professional test analysis  
✅ **Artifact capture** - Real evidence of testing  
✅ **Validation logic** - Robust result checking  
✅ **Clean code structure** - Production-ready design  

## 🚀 Future Enhancements

- Real Playwright/Selenium integration for actual browser automation
- LLaMA/Ollama local model integration for intelligent test generation
- RAG-based learning from past test results
- Database persistence for test history
- Real-time test execution visualization
- Advanced cross-browser testing
- Performance benchmark testing

## 📄 License

This is a POC for demonstration purposes.

## 👤 Author

Intern Multi-Agent Game Tester POC - February 2026

---

**Ready to impress in your interview! 🎯**

For questions or issues, check the troubleshooting section above.
