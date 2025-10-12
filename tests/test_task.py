"""
Tests for the Task module
"""

import unittest
from obscuraflow.task import Task


class TestTask(unittest.TestCase):
    """Test cases for the Task class"""
    
    def test_task_creation(self):
        """Test basic task creation"""
        def sample_function():
            return "result"
        
        task = Task("test_task", sample_function)
        self.assertEqual(task.name, "test_task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.dependencies, [])
    
    def test_task_execution(self):
        """Test task execution"""
        def sample_function():
            return 42
        
        task = Task("test_task", sample_function)
        result = task.execute()
        
        self.assertEqual(result, 42)
        self.assertEqual(task.status, "completed")
        self.assertEqual(task.result, 42)
    
    def test_task_with_context(self):
        """Test task execution with context"""
        def sample_function(value):
            return value * 2
        
        task = Task("test_task", sample_function)
        result = task.execute({"value": 5})
        
        self.assertEqual(result, 10)
        self.assertEqual(task.status, "completed")
    
    def test_task_with_dependencies(self):
        """Test task with dependencies"""
        def sample_function():
            return "result"
        
        task = Task("test_task", sample_function, dependencies=["dep1", "dep2"])
        self.assertEqual(task.dependencies, ["dep1", "dep2"])
    
    def test_task_failure(self):
        """Test task execution failure"""
        def failing_function():
            raise ValueError("Test error")
        
        task = Task("failing_task", failing_function)
        
        with self.assertRaises(RuntimeError):
            task.execute()
        
        self.assertEqual(task.status, "failed")


if __name__ == "__main__":
    unittest.main()
