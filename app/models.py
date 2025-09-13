# app/models.py

from typing import Optional
from sqlmodel import Field, SQLModel

# This is our main table model. It defines the columns in the 'workflow' table.
class Workflow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)