from typing import Optional
from pydantic import BaseModel, Field

class DepartmentCreate(BaseModel):
    departmentName : str = Field(...,description="Department Name")
    description : Optional[str]=None

class DepartmentUpdate(BaseModel):
    departmentName : Optional[str] = Field(None,description="New Name of current depaertment")
    description : Optional[str] = None
class DepartmentResponse(BaseModel):
    department_id:int = Field(...)
    departmentName : str = Field(...)
    description : Optional[str] = None

    class Config:
        from_attributes=True

