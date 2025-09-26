# celery_worker.py

from celery import Celery
from sqlmodel import Session, select

# We need to import our database engine and models
from app.database import engine
from app.models import Workflow
from app.core.task_executor import execute_task # Import our new executor

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# This is our NEW, intelligent task.
@celery_app.task
def run_workflow_task(workflow_id: int):
    """
    The main Celery task that retrieves and executes all tasks for a given workflow.
    """
    print(f"🚀 Starting execution for workflow_id: {workflow_id}")

    # The worker needs its own database session.
    with Session(engine) as session:
        # Fetch the workflow and its tasks using our relationship magic
        workflow = session.get(Workflow, workflow_id)
        
        if not workflow:
            print(f"❌ Workflow with id {workflow_id} not found.")
            return
            
        print(f"Found workflow: '{workflow.name}' with {len(workflow.tasks)} tasks.")
        
        # This context dictionary can be used to pass data from one task to the next.
        # For now, it's empty.
        execution_context = {}
        
        # Execute tasks in the order they were created (or add an order field later)
        # We sort by ID as a simple way to ensure order for now.
        sorted_tasks = sorted(workflow.tasks, key=lambda t: t.id)
        
        for task in sorted_tasks:
            print(f"--- Running task: {task.name} (Type: {task.task_type}) ---")
            result = execute_task(task, execution_context)
            
            # Here you could update the context with the result of the task
            # e.g., execution_context[f"task_{task.id}_result"] = result
            
            print(f"--- Finished task: {task.name} with status: {result.get('status')} ---")

    print(f"✅ Workflow execution finished for workflow_id: {workflow_id}")
    return f"Workflow {workflow_id} completed successfully."