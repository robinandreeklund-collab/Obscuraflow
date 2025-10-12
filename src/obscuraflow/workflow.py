"""
Workflow module for Obscuraflow
"""

from typing import List, Dict, Any, Optional
from .task import Task


class Workflow:
    """
    Represents a workflow composed of multiple tasks.
    
    A workflow manages the execution of tasks and their dependencies.
    """
    
    def __init__(self, name: str):
        """
        Initialize a Workflow.
        
        Args:
            name: Name of the workflow
        """
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.execution_order: List[str] = []
        self.status = "initialized"
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the workflow.
        
        Args:
            task: Task to add
        """
        if task.name in self.tasks:
            raise ValueError(f"Task '{task.name}' already exists in workflow")
        self.tasks[task.name] = task
    
    def remove_task(self, task_name: str) -> None:
        """
        Remove a task from the workflow.
        
        Args:
            task_name: Name of the task to remove
        """
        if task_name not in self.tasks:
            raise ValueError(f"Task '{task_name}' not found in workflow")
        del self.tasks[task_name]
    
    def get_task(self, task_name: str) -> Optional[Task]:
        """
        Get a task by name.
        
        Args:
            task_name: Name of the task
            
        Returns:
            Task object or None if not found
        """
        return self.tasks.get(task_name)
    
    def _resolve_dependencies(self) -> List[str]:
        """
        Resolve task dependencies and determine execution order.
        
        Returns:
            List of task names in execution order
        """
        visited = set()
        order = []
        
        def visit(task_name: str, path: set):
            if task_name in path:
                raise ValueError(f"Circular dependency detected: {task_name}")
            
            if task_name in visited:
                return
            
            task = self.tasks.get(task_name)
            if not task:
                raise ValueError(f"Task '{task_name}' not found")
            
            path.add(task_name)
            for dep in task.dependencies:
                visit(dep, path.copy())
            
            visited.add(task_name)
            order.append(task_name)
        
        for task_name in self.tasks:
            if task_name not in visited:
                visit(task_name, set())
        
        return order
    
    def execute(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Args:
            context: Initial context data for the workflow
            
        Returns:
            Dictionary of task results
        """
        if context is None:
            context = {}
        
        self.status = "running"
        self.execution_order = self._resolve_dependencies()
        results = {}
        
        try:
            for task_name in self.execution_order:
                task = self.tasks[task_name]
                
                # Prepare context with results from dependencies
                task_context = context.copy()
                for dep_name in task.dependencies:
                    task_context[dep_name] = results.get(dep_name)
                
                result = task.execute(task_context)
                results[task_name] = result
            
            self.status = "completed"
            return results
        except Exception as e:
            self.status = "failed"
            raise RuntimeError(f"Workflow '{self.name}' failed: {str(e)}") from e
    
    def __repr__(self) -> str:
        return f"Workflow(name='{self.name}', tasks={len(self.tasks)}, status='{self.status}')"
