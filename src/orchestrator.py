from .agents.base import BaseAgent
from .agents.planner import PlannerAgent
from .agents.ranker import RankerAgent
from .agents.executor import ExecutorAgent
from .agents.analyzer import AnalyzerAgent
from typing import Dict, List, Any
import asyncio

class OrchestratorAgent(BaseAgent):
    """Master agent that coordinates all other agents"""
    
    def __init__(self):
        super().__init__("orchestrator_1", "OrchestratorAgent")
        self.planner = PlannerAgent()
        self.ranker = RankerAgent()
        self.executors = [ExecutorAgent(f"executor_{i}") for i in range(1, 3)]
        self.analyzer = AnalyzerAgent()
    
    async def orchestrate_testing(self, game_url: str) -> Dict[str, Any]:
        """Coordinate entire testing workflow"""
        self.log(f"Starting orchestration for {game_url}")
        
        workflow_results = {
            "status": "running",
            "workflow_id": "workflow_1",
            "game_url": game_url,
            "steps": {}
        }
        
        try:
            # Step 1: Planning
            self.log("Step 1: Generating test cases...")
            planning_result = await self.planner.execute(game_url)
            workflow_results["steps"]["planning"] = planning_result
            test_cases = planning_result.get("test_cases", [])
            self.log(f"Generated {len(test_cases)} test cases")
            
            # Step 2: Ranking
            self.log("Step 2: Ranking test cases...")
            ranking_result = await self.ranker.execute(test_cases)
            workflow_results["steps"]["ranking"] = ranking_result
            top_10 = ranking_result.get("top_10_selected", [])
            self.log(f"Selected top {len(top_10)} tests")
            
            # Step 3: Execution
            self.log("Step 3: Executing tests in parallel...")
            execution_results = []
            
            # Distribute tests among executors
            tests_per_executor = len(top_10) // len(self.executors)
            executor_tasks = []
            
            for idx, executor in enumerate(self.executors):
                start = idx * tests_per_executor
                end = start + tests_per_executor if idx < len(self.executors) - 1 else len(top_10)
                executor_tests = top_10[start:end]
                
                if executor_tests:
                    executor_tasks.append(
                        executor.execute_multiple(executor_tests, game_url)
                    )
            
            # Run executors in parallel
            if executor_tasks:
                executor_outputs = await asyncio.gather(*executor_tasks)
                for output in executor_outputs:
                    execution_results.extend(output.get("execution_results", []))
            
            workflow_results["steps"]["execution"] = {
                "status": "success",
                "total_executed": len(execution_results),
                "passed": len([r for r in execution_results if r["status"] == "passed"]),
                "failed": len([r for r in execution_results if r["status"] == "failed"])
            }
            self.log(f"Executed {len(execution_results)} tests")
            
            # Step 4: Validation & Analysis
            self.log("Step 4: Validating and analyzing results...")
            analysis_result = await self.analyzer.execute(execution_results)
            workflow_results["steps"]["analysis"] = analysis_result
            self.log("Analysis complete")
            
            workflow_results["status"] = "completed"
            self.log("Orchestration workflow completed successfully")
            
        except Exception as e:
            self.log(f"Error during orchestration: {str(e)}")
            workflow_results["status"] = "failed"
            workflow_results["error"] = str(e)
        
        return workflow_results

    async def execute(self, game_url: str, *args, **kwargs) -> Dict[str, Any]:
        """Implement BaseAgent.execute - entry point for orchestration."""
        return await self.orchestrate_testing(game_url)
