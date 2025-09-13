# app/routers/workflows.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Workflow
from app.schemas import WorkflowCreate, WorkflowRead

# Create an APIRouter
# We can define a prefix and tags to be applied to all routes in this router.
router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"],
)

# Endpoint to create a new workflow
@router.post("/", response_model=WorkflowRead)
def create_workflow(
    *, session: Session = Depends(get_session), workflow: WorkflowCreate
):
    """
    Create a new workflow.
    """
    # Create a database model instance from the API schema
    db_workflow = Workflow.from_orm(workflow)
    session.add(db_workflow)
    session.commit()
    session.refresh(db_workflow)
    return db_workflow

# Endpoint to list all workflows
@router.get("/", response_model=List[WorkflowRead])
def read_workflows(*, session: Session = Depends(get_session)):
    """
    Retrieve all workflows.
    """
    workflows = session.exec(select(Workflow)).all()
    return workflows