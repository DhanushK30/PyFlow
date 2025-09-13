# app/schemas.py

from typing import Optional, List # <-- Add List
from sqlmodel import SQLModel

# === Task Schemas ===
class TaskCreate(SQLModel):
    name: str
    description: Optional[str] = None
    task_type: str

class TaskRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    task_type: str

# === Workflow Schemas (Updated) ===
class WorkflowCreate(SQLModel):
    name: str
    description: Optional[str] = None

class WorkflowRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None

# This is a NEW schema for reading a Workflow *with* its list of tasks.
# It's called "nesting" schemas.
class WorkflowReadWithTasks(WorkflowRead):
    tasks: List[TaskRead] = []