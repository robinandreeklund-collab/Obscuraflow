# Obscuraflow

A lightweight workflow orchestration framework for Python.

## Overview

Obscuraflow is a simple yet powerful workflow orchestration framework that allows you to define, manage, and execute complex workflows with task dependencies.

## Features

- **Simple API**: Easy-to-use interface for defining workflows and tasks
- **Dependency Management**: Automatic resolution of task dependencies
- **Error Handling**: Built-in error handling and status tracking
- **Flexible Execution**: Execute workflows with custom context data

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from obscuraflow import Workflow, Task, Executor

# Define task functions
def fetch_data():
    return {"users": 100, "products": 50}

def process_data(fetch_data):
    return {
        "total_items": fetch_data["users"] + fetch_data["products"],
        "data": fetch_data
    }

# Create workflow
workflow = Workflow("data_pipeline")

# Add tasks
task1 = Task("fetch_data", fetch_data)
task2 = Task("process_data", process_data, dependencies=["fetch_data"])

workflow.add_task(task1)
workflow.add_task(task2)

# Execute
executor = Executor(workflow)
results = executor.run()
```

## Documentation

### Core Components

#### Task
Represents a single unit of work in a workflow.

```python
task = Task(
    name="my_task",
    function=my_function,
    dependencies=["other_task"]
)
```

#### Workflow
Manages a collection of tasks and their execution order.

```python
workflow = Workflow("my_workflow")
workflow.add_task(task)
results = workflow.execute()
```

#### Executor
Provides a simple interface for running workflows.

```python
executor = Executor(workflow)
results = executor.run()
```

## Examples

See the `examples/` directory for more detailed examples.

## Running Tests

```bash
python -m unittest discover tests
```

## License

MIT