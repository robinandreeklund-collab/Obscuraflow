"""
Simple example demonstrating Obscuraflow usage
"""

from obscuraflow import Workflow, Task, Executor


def fetch_data():
    """Simulate fetching data"""
    print("Fetching data...")
    return {"users": 100, "products": 50}


def process_data(fetch_data):
    """Process the fetched data"""
    print(f"Processing data: {fetch_data}")
    return {
        "total_items": fetch_data["users"] + fetch_data["products"],
        "data": fetch_data
    }


def save_results(process_data):
    """Save the processed results"""
    print(f"Saving results: {process_data}")
    return f"Saved {process_data['total_items']} items successfully"


def main():
    # Create a workflow
    workflow = Workflow("data_pipeline")
    
    # Define tasks
    task1 = Task("fetch_data", fetch_data)
    task2 = Task("process_data", process_data, dependencies=["fetch_data"])
    task3 = Task("save_results", save_results, dependencies=["process_data"])
    
    # Add tasks to workflow
    workflow.add_task(task1)
    workflow.add_task(task2)
    workflow.add_task(task3)
    
    # Create executor and run
    executor = Executor(workflow)
    results = executor.run()
    
    # Print results
    print("\n=== Workflow Results ===")
    for task_name, result in results.items():
        print(f"{task_name}: {result}")


if __name__ == "__main__":
    main()
