"""
Executor module for Obscuraflow
"""

from typing import Dict, Any, Optional
from .workflow import Workflow


class Executor:
    """
    Executor for running workflows.
    
    The executor provides a simple interface for executing workflows
    and managing execution state.
    """
    
    def __init__(self, workflow: Workflow):
        """
        Initialize an Executor.
        
        Args:
            workflow: Workflow to execute
        """
        self.workflow = workflow
        self.results: Optional[Dict[str, Any]] = None
    
    def run(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the workflow.
        
        Args:
            context: Initial context data for the workflow
            
        Returns:
            Dictionary of task results
        """
        self.results = self.workflow.execute(context)
        return self.results
    
    def get_results(self) -> Optional[Dict[str, Any]]:
        """
        Get the results of the last execution.
        
        Returns:
            Dictionary of task results or None if not executed
        """
        return self.results
    
    def reset(self) -> None:
        """
        Reset the executor and workflow state.
        """
        self.results = None
        for task in self.workflow.tasks.values():
            task.status = "pending"
            task.result = None
        self.workflow.status = "initialized"
    
    def __repr__(self) -> str:
        return f"Executor(workflow='{self.workflow.name}')"
