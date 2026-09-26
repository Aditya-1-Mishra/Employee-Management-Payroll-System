from pydantic import BaseModel
from typing import Optional


class DesignationCreate(BaseModel):
    name: str
    description: Optional[str] = None


class DesignationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DesignationResponse(BaseModel):
    designation_id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
