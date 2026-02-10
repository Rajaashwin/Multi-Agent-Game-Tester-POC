from .base import BaseAgent
from typing import Dict, List, Any
import json

class PlannerAgent(BaseAgent):
    """Agent that generates test case candidates"""
    
    def __init__(self):
        super().__init__("planner_1", "PlannerAgent")
        self.test_templates = [
            "Click button '{button}' and verify result",
            "Enter value '{value}' in input field and submit",
            "Test keyboard shortcut '{key}'",
            "Verify error handling for invalid input '{input}'",
            "Test boundary condition with value '{value}'",
            "Attempt to click non-existent element '{element}'",
            "Test rapid clicking of button '{button}' {count} times",
            "Verify page loads correctly on first visit",
            "Test page refresh and state persistence",
            "Verify console has no critical errors",
            "Test with empty input fields",
            "Test with maximum allowed values",
            "Test with minimum allowed values",
            "Verify responsive design at different viewport sizes",
            "Test tab navigation through form fields",
        ]
    
    async def execute(self, game_url: str, game_analysis: str = None) -> Dict[str, Any]:
        """Generate 20+ test cases for the given game"""
        self.log(f"Generating test cases for {game_url}")
        
        test_cases = []
        
        # Generate test cases based on templates
        buttons = ["submit", "clear", "reset", "check", "verify", "calculate"]
        values = ["0", "1", "-1", "999999", "0.5", "invalid", ""]
        
        # Template-based tests
        for button in buttons[:3]:
            for template in self.test_templates[:7]:
                if "{button}" in template or "{count}" in template:
                    # Provide safe defaults for optional template placeholders
                    mapping = {
                        "button": button,
                        "count": 3,
                        "value": "1",
                        "element": "unknown",
                        "input": "",
                        "key": "Enter"
                    }
                    try:
                        description = template.format(**mapping)
                    except Exception:
                        description = template

                    test_case = {
                        "id": f"test_{len(test_cases) + 1}",
                        "description": description,
                        "priority": "high" if button in ["submit", "check"] else "medium",
                        "type": "ui_interaction",
                        "expected_result": f"Button '{button}' works correctly"
                    }
                    test_cases.append(test_case)
        
        # Value-based tests
        for value in values:
            test_case = {
                "id": f"test_{len(test_cases) + 1}",
                "description": f"Enter value '{value}' and verify handling",
                "priority": "high" if value in ["", "invalid"] else "medium",
                "type": "input_validation",
                "expected_result": f"Handle input '{value}' correctly"
            }
            test_cases.append(test_case)
        
        # Additional edge case tests
        edge_cases = [
            "Load game and verify initial state",
            "Check all visible buttons are clickable",
            "Verify no JavaScript errors on load",
            "Test page performance and load time",
            "Verify page accessibility",
        ]
        
        for description in edge_cases:
            if len(test_cases) < 20:
                test_case = {
                    "id": f"test_{len(test_cases) + 1}",
                    "description": description,
                    "priority": "medium",
                    "type": "functional",
                    "expected_result": "Test passes without errors"
                }
                test_cases.append(test_case)
        
        # Ensure we have 20+ tests
        while len(test_cases) < 20:
            test_case = {
                "id": f"test_{len(test_cases) + 1}",
                "description": f"Stress test iteration {len(test_cases) - 19}",
                "priority": "low",
                "type": "stress_test",
                "expected_result": "No crashes or memory leaks"
            }
            test_cases.append(test_case)
        
        return {
            "status": "success",
            "agent": self.name,
            "total_tests_generated": len(test_cases),
            "test_cases": test_cases[:20]
        }
