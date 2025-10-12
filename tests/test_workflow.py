"""
Tests for the Workflow module
"""

import unittest
from obscuraflow.workflow import Workflow
from obscuraflow.task import Task


class TestWorkflow(unittest.TestCase):
    """Test cases for the Workflow class"""
    
    def test_workflow_creation(self):
        """Test basic workflow creation"""
        workflow = Workflow("test_workflow")
        self.assertEqual(workflow.name, "test_workflow")
        self.assertEqual(workflow.status, "initialized")
        self.assertEqual(len(workflow.tasks), 0)
    
    def test_add_task(self):
        """Test adding tasks to workflow"""
        workflow = Workflow("test_workflow")
        
        def sample_function():
            return "result"
        
        task = Task("task1", sample_function)
        workflow.add_task(task)
        
        self.assertEqual(len(workflow.tasks), 1)
        self.assertIn("task1", workflow.tasks)
    
    def test_duplicate_task(self):
        """Test adding duplicate task raises error"""
        workflow = Workflow("test_workflow")
        
        def sample_function():
            return "result"
        
        task1 = Task("task1", sample_function)
        task2 = Task("task1", sample_function)
        
        workflow.add_task(task1)
        with self.assertRaises(ValueError):
            workflow.add_task(task2)
    
    def test_remove_task(self):
        """Test removing tasks from workflow"""
        workflow = Workflow("test_workflow")
        
        def sample_function():
            return "result"
        
        task = Task("task1", sample_function)
        workflow.add_task(task)
        workflow.remove_task("task1")
        
        self.assertEqual(len(workflow.tasks), 0)
    
    def test_get_task(self):
        """Test getting task from workflow"""
        workflow = Workflow("test_workflow")
        
        def sample_function():
            return "result"
        
        task = Task("task1", sample_function)
        workflow.add_task(task)
        
        retrieved_task = workflow.get_task("task1")
        self.assertEqual(retrieved_task.name, "task1")
    
    def test_workflow_execution(self):
        """Test basic workflow execution"""
        workflow = Workflow("test_workflow")
        
        def task1_func():
            return 10
        
        def task2_func():
            return 20
        
        task1 = Task("task1", task1_func)
        task2 = Task("task2", task2_func)
        
        workflow.add_task(task1)
        workflow.add_task(task2)
        
        results = workflow.execute()
        
        self.assertEqual(results["task1"], 10)
        self.assertEqual(results["task2"], 20)
        self.assertEqual(workflow.status, "completed")
    
    def test_workflow_with_dependencies(self):
        """Test workflow execution with dependencies"""
        workflow = Workflow("test_workflow")
        
        def task1_func():
            return 10
        
        def task2_func(task1):
            return task1 * 2
        
        task1 = Task("task1", task1_func)
        task2 = Task("task2", task2_func, dependencies=["task1"])
        
        workflow.add_task(task1)
        workflow.add_task(task2)
        
        results = workflow.execute()
        
        self.assertEqual(results["task1"], 10)
        self.assertEqual(results["task2"], 20)
    
    def test_circular_dependency(self):
        """Test that circular dependencies are detected"""
        workflow = Workflow("test_workflow")
        
        def sample_function():
            return "result"
        
        task1 = Task("task1", sample_function, dependencies=["task2"])
        task2 = Task("task2", sample_function, dependencies=["task1"])
        
        workflow.add_task(task1)
        workflow.add_task(task2)
        
        with self.assertRaises(ValueError):
            workflow.execute()


if __name__ == "__main__":
    unittest.main()
