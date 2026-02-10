from .base import BaseAgent
from typing import Dict, List, Any

class RankerAgent(BaseAgent):
    """Agent that ranks and selects best test cases"""
    
    def __init__(self):
        super().__init__("ranker_1", "RankerAgent")
    
    async def execute(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rank test cases and select top 10"""
        self.log(f"Ranking {len(test_cases)} test cases")
        
        # Simple scoring system
        scored_cases = []
        
        for test in test_cases:
            score = 0
            
            # Priority scoring
            if test.get("priority") == "high":
                score += 100
            elif test.get("priority") == "medium":
                score += 50
            else:
                score += 25
            
            # Type scoring
            if test.get("type") in ["functional", "input_validation"]:
                score += 30
            elif test.get("type") == "ui_interaction":
                score += 20
            else:
                score += 10
            
            # Complexity scoring
            description = test.get("description", "").lower()
            if any(word in description for word in ["error", "invalid", "boundary", "edge"]):
                score += 20
            
            scored_cases.append({
                **test,
                "score": score
            })
        
        # Sort by score descending and take top 10
        ranked = sorted(scored_cases, key=lambda x: x["score"], reverse=True)
        top_10 = ranked[:10]
        
        self.log(f"Selected top 10 tests with scores: {[t['score'] for t in top_10]}")
        
        return {
            "status": "success",
            "agent": self.name,
            "total_ranked": len(test_cases),
            "top_10_selected": top_10,
            "ranking_strategy": "Priority + Type + Complexity scoring"
        }
