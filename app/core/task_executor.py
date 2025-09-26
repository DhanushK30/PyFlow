# app/core/task_executor.py

import time
from app.models import Task

def _execute_log_message(task: Task, context: dict):
    """
    A simple task type that just prints a message.
    The 'context' can be used to pass data between tasks in the future.
    """
    print(f"✅ EXECUTING (LOG_MESSAGE): '{task.name}' - Description: {task.description}")
    time.sleep(1) # Simulate work
    return {"status": "success", "message": f"Logged message for task {task.id}"}

def _execute_send_slack_message(task: Task, context: dict):
    """

    Dummy function for sending a slack message.
    """
    print(f"🔔 EXECUTING (SLACK_MESSAGE): Sending message for task '{task.name}'")
    time.sleep(2) # Simulate API call
    return {"status": "success", "message": f"Slack message sent for task {task.id}"}

# This is our registry of task types.
# The key is the `task_type` string from our database model.
# The value is the function that executes it.
TASK_TYPE_REGISTRY = {
    "log_message": _execute_log_message,
    "send_slack_message": _execute_send_slack_message,
}

def execute_task(task: Task, context: dict = None):
    """

    Looks up the task type in the registry and executes the corresponding function.
    """
    if context is None:
        context = {}
        
    executor_func = TASK_TYPE_REGISTRY.get(task.task_type)
    
    if not executor_func:
        print(f"❌ ERROR: No executor found for task type '{task.task_type}'")
        return {"status": "error", "message": f"Unknown task type: {task.task_type}"}
        
    return executor_func(task, context)