# celery_worker.py

import time
from celery import Celery

# Initialize Celery
# The first argument is the name of the current module.
# The `broker` argument specifies the URL of our message broker (Redis).
# The `backend` argument is used to store task results, which we'll also use Redis for.
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# This is our first "task".
# The @celery_app.task decorator registers this function as a Celery task.
@celery_app.task
def run_workflow_task(workflow_id: int):
    """
    A dummy task that simulates running a workflow.
    In the future, this will fetch tasks from the DB and execute them.
    """
    print(f"Received request to run workflow_id: {workflow_id}")
    
    # Simulate a long-running process
    total_steps = 5
    for i in range(total_steps):
        time.sleep(1) # Simulate doing work, like calling an API
        print(f"Workflow {workflow_id}: Executing step {i+1}/{total_steps}...")
    
    print(f"Workflow {workflow_id} finished successfully.")
    return f"Workflow {workflow_id} completed!"