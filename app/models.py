# app/models.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship # <-- Add Relationship

# === The Workflow Model (with a new Relationship attribute) ===
# This needs to be defined before the Task model that references it
class Workflow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    
    # This is the "many" side of the relationship.
    # It tells SQLModel that a Workflow can have a list of Task objects.
    # `back_populates` links it to the `workflow` attribute in the Task model.
    tasks: List["Task"] = Relationship(back_populates="workflow")


# === The NEW Task Model ===
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    task_type: str # e.g., "send_email", "post_to_slack"
    
    # This is our Foreign Key. It links this Task to a Workflow.
    # `workflow.id` refers to the `id` column in the `workflow` table.
    workflow_id: Optional[int] = Field(default=None, foreign_key="workflow.id")
    
    # This is the "one" side of the relationship.
    # It creates the actual link to the Workflow object in our Python code.
    workflow: Optional[Workflow] = Relationship(back_populates="tasks")