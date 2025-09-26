# app/routers/workflows.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status 
from celery_worker import run_workflow_task 
from sqlmodel import Session, select

from app.database import get_session
from app.models import Workflow, Task # <-- Import Task
from app.schemas import ( # <-- Import new schemas
    WorkflowCreate, 
    WorkflowRead, 
    WorkflowReadWithTasks, 
    TaskCreate,
    TaskRead
)

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"],
)

# --- Workflow Endpoints ---

@router.post("/", response_model=WorkflowRead)
def create_workflow(*, session: Session = Depends(get_session), workflow: WorkflowCreate):
    db_workflow = Workflow.from_orm(workflow)
    session.add(db_workflow)
    session.commit()
    session.refresh(db_workflow)
    return db_workflow

@router.get("/", response_model=List[WorkflowRead])
def read_workflows(*, session: Session = Depends(get_session)):
    workflows = session.exec(select(Workflow)).all()
    return workflows

# NEW: Get a single workflow by its ID
@router.get("/{workflow_id}", response_model=WorkflowReadWithTasks)
def read_workflow(*, session: Session = Depends(get_session), workflow_id: int):
    """
    Retrieve a single workflow by its ID, including its tasks.
    """
    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

# --- Task Endpoints ---

# NEW: Add a task to a specific workflow
@router.post("/{workflow_id}/tasks/", response_model=TaskRead)
def create_task_for_workflow(
    *,
    session: Session = Depends(get_session),
    workflow_id: int,
    task: TaskCreate
):
    """
    Create a new task and associate it with an existing workflow.
    """
    # First, check if the workflow exists
    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Create the task, linking it via the workflow_id
    db_task = Task.from_orm(task, update={'workflow_id': workflow_id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.post("/{workflow_id}/run", status_code=status.HTTP_202_ACCEPTED)
def run_workflow(
    *,
    session: Session = Depends(get_session),
    workflow_id: int
):
    """
    Trigger a workflow to run in the background.
    """
    # First, check if the workflow exists
    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Send the task to the Celery worker
    # .delay() is the magic that sends it to the Redis queue.
    task_result = run_workflow_task.delay(workflow.id)
    
    # Return immediately to the user
    return {"message": "Workflow run has been triggered.", "task_id": task_result.id}