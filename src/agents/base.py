from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.created_at = datetime.now()
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute agent task"""
        pass
    
    def log(self, message: str):
        """Log agent activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.name} ({self.agent_id}): {message}")
