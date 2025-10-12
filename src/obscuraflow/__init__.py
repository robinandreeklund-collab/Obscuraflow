"""
Obscuraflow - A workflow orchestration framework
"""

__version__ = "0.1.0"
__author__ = "Robin Andreeklund"

from .workflow import Workflow
from .task import Task
from .executor import Executor

__all__ = ["Workflow", "Task", "Executor"]
