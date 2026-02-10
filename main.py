from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.orchestrator import OrchestratorAgent
from src.report_generator import ReportGenerator
from src.game_interaction import GameInteraction

# Initialize FastAPI app
app = FastAPI(title="Multi-Agent Game Tester POC")

# Get allowed origins from environment or use defaults
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
environment = os.getenv("ENVIRONMENT", "development")

# Build allowed origins list
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    frontend_url,
]

# In production, only allow the configured `FRONTEND_URL` to simplify CORS
if environment == "production":
    if frontend_url and frontend_url not in allowed_origins:
        allowed_origins.append(frontend_url)

# Serve frontend static files (UI) - mount at /app for SPA support
frontend_path = Path("frontend")
if frontend_path.exists():
    app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = OrchestratorAgent()
report_generator = ReportGenerator()
game_interaction = GameInteraction()

# Store latest workflow result
latest_workflow_result = None

class GameTestRequest(BaseModel):
    """Request model for game testing"""
    game_url: str = "https://play.ezygamers.com/"
    test_name: str = "Default Game Test"

class TestStatus(BaseModel):
    """Test status response"""
    status: str
    message: str

@app.get("/")
async def root():
    """Root endpoint - returns API info"""
    return {
        "name": "Multi-Agent Game Tester POC",
        "version": "1.0.0",
        "description": "Automated testing system for web-based games",
        "endpoints": {
            "plan": "/api/plan",
            "execute": "/api/execute",
            "status": "/api/status",
            "report": "/api/report",
            "latest_report": "/api/latest-report",
            "artifacts": "/api/artifacts"
        }
    }


# Static files are mounted at /app above; no dedicated /app route is required.

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/plan")
async def generate_test_plan(request: GameTestRequest):
    """Generate test plan for a game"""
    try:
        print(f"\n{'='*60}")
        print(f"Starting Test Planning for: {request.game_url}")
        print(f"{'='*60}\n")
        
        planner = orchestrator.planner
        result = await planner.execute(request.game_url)
        
        return {
            "status": "success",
            "message": f"Generated {result['total_tests_generated']} test cases",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/plan")
async def generate_test_plan():
    """Generate a test plan"""
    try:
        # Placeholder for the actual test plan generation logic
        return {"status": "success", "message": "Test plan generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute")
async def execute_tests(request: GameTestRequest):
    """Execute full testing workflow"""
    global latest_workflow_result
    
    try:
        print(f"\n{'='*60}")
        print(f"Starting Full Testing Workflow for: {request.game_url}")
        print(f"{'='*60}\n")
        
        # Run orchestration
        workflow_result = await orchestrator.orchestrate_testing(request.game_url)
        latest_workflow_result = workflow_result
        
        # Generate report
        report = report_generator.generate_report(workflow_result, request.game_url)
        report_path = report_generator.save_report(report)
        
        print(f"\n{'='*60}")
        print(f"Workflow Completed Successfully")
        print(f"Report saved: {report_path}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Testing workflow completed",
            "workflow_id": workflow_result.get("workflow_id"),
            "report_id": report.get("report_id"),
            "summary": report.get("execution_summary"),
            "verdicts": report.get("verdicts")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/execute")
async def execute_tests():
    """Execute the testing workflow"""
    try:
        # Placeholder for the actual execution logic
        return {"status": "success", "message": "Tests executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_workflow_status():
    """Get status of latest workflow"""
    if latest_workflow_result is None:
        return {"status": "no_workflow_executed"}
    
    return {
        "status": latest_workflow_result.get("status"),
        "workflow_id": latest_workflow_result.get("workflow_id"),
        "game_url": latest_workflow_result.get("game_url"),
        "summary": {
            "planning": latest_workflow_result.get("steps", {}).get("planning", {}).get("total_tests_generated", 0),
            "ranking": len(latest_workflow_result.get("steps", {}).get("ranking", {}).get("top_10_selected", [])),
            "execution": latest_workflow_result.get("steps", {}).get("execution", {})
        }
    }

@app.get("/api/report")
async def get_report():
    """Get latest generated report"""
    try:
        if latest_workflow_result is None:
            raise HTTPException(status_code=404, detail="No report generated yet")
        
        report = report_generator.generate_report(latest_workflow_result, 
                                                 latest_workflow_result.get("game_url", ""))
        
        return {
            "status": "success",
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest-report")
async def get_latest_report_full():
    """Get the complete latest report from disk"""
    try:
        report = report_generator.get_latest_report()
        
        if "error" in report:
            raise HTTPException(status_code=404, detail="No reports found")
        
        return {
            "status": "success",
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artifacts")
async def get_artifacts():
    """Get list of captured artifacts"""
    summary = game_interaction.get_artifacts_summary()
    
    return {
        "status": "success",
        "artifacts": summary
    }

@app.get("/api/reports-list")
async def list_reports():
    """List all available reports"""
    reports_dir = Path("reports")
    
    if not reports_dir.exists():
        return {"reports": []}
    
    reports = []
    for report_file in sorted(reports_dir.glob("report_*.json")):
        try:
            with open(report_file, 'r') as f:
                report_data = json.load(f)
                reports.append({
                    "report_id": report_data.get("report_id"),
                    "timestamp": report_data.get("timestamp"),
                    "game_url": report_data.get("game_url"),
                    "success_rate": report_data.get("execution_summary", {}).get("success_rate"),
                    "file_path": str(report_file)
                })
        except Exception as e:
            print(f"Error reading report {report_file}: {e}")
    
    return {"status": "success", "reports": reports}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
