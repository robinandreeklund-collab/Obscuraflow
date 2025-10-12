"""
Tests for the Executor module
"""

import unittest
from obscuraflow.executor import Executor
from obscuraflow.workflow import Workflow
from obscuraflow.task import Task


class TestExecutor(unittest.TestCase):
    """Test cases for the Executor class"""
    
    def test_executor_creation(self):
        """Test basic executor creation"""
        workflow = Workflow("test_workflow")
        executor = Executor(workflow)
        
        self.assertEqual(executor.workflow.name, "test_workflow")
        self.assertIsNone(executor.results)
    
    def test_executor_run(self):
        """Test executor run"""
        workflow = Workflow("test_workflow")
        
        def task_func():
            return 42
        
        task = Task("task1", task_func)
        workflow.add_task(task)
        
        executor = Executor(workflow)
        results = executor.run()
        
        self.assertEqual(results["task1"], 42)
        self.assertEqual(executor.get_results()["task1"], 42)
    
    def test_executor_reset(self):
        """Test executor reset"""
        workflow = Workflow("test_workflow")
        
        def task_func():
            return 42
        
        task = Task("task1", task_func)
        workflow.add_task(task)
        
        executor = Executor(workflow)
        executor.run()
        executor.reset()
        
        self.assertIsNone(executor.results)
        self.assertEqual(workflow.status, "initialized")
        self.assertEqual(task.status, "pending")


if __name__ == "__main__":
    unittest.main()
