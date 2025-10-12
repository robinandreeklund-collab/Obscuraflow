"""
Task module for Obscuraflow
"""

from typing import Any, Callable, Optional, Dict


class Task:
    """
    Represents a single task in a workflow.
    
    A task encapsulates a function to be executed along with its configuration.
    """
    
    def __init__(
        self,
        name: str,
        function: Callable,
        dependencies: Optional[list] = None,
        **kwargs
    ):
        """
        Initialize a Task.
        
        Args:
            name: Name of the task
            function: Function to execute
            dependencies: List of task names this task depends on
            **kwargs: Additional task configuration
        """
        self.name = name
        self.function = function
        self.dependencies = dependencies or []
        self.config = kwargs
        self.result = None
        self.status = "pending"
    
    def execute(self, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute the task.
        
        Args:
            context: Context data passed to the task function
            
        Returns:
            Result of the task execution
        """
        try:
            self.status = "running"
            if context is None:
                context = {}
            
            self.result = self.function(**context)
            self.status = "completed"
            return self.result
        except Exception as e:
            self.status = "failed"
            raise RuntimeError(f"Task '{self.name}' failed: {str(e)}") from e
    
    def __repr__(self) -> str:
        return f"Task(name='{self.name}', status='{self.status}')"
