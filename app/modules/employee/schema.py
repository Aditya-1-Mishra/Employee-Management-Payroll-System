from  pydantic import BaseModel, Field
from typing import Optional
from datetime import date 
import string
import secrets
'''to generate a random password in case assigned authority do not have any passowrd in mind for the employee.'''
def generate_password():
    characters = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(secrets.choice(characters) for _ in range(12))


class EmployeeCreate(BaseModel):
    name: str = Field(..., description="Employee name")
    email: str = Field(..., description="Employee email")
    phone: Optional[str] = Field(None, description="Employee phone number")
    designation: str = Field(..., description="Employee designation")
    department: str = Field(..., description="Employee department")
    hire_date: Optional[date] = Field(None, description="Employee hire date")
    password: str = Field(description="Employee password",default_factory=generate_password)
    gender: Optional[str] = Field(None, description="Employee gender")
    role: str = Field(..., description="Employee role")
    manager_id: Optional[int] = Field(None, description="Employee manager ID")
    dob: Optional[date] = Field(None, description="Employee date of birth")

# same field as per the EmployeeCreate class but all fields are optional for update operation.
class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Employee name")
    email: Optional[str] = Field(None, description="Employee email")
    phone: Optional[str] = Field(None, description="Employee phone number")
    designation: Optional[str] = Field(None, description="Employee designation")
    department: Optional[str] = Field(None, description="Employee department")
    hire_date: Optional[date] = Field(None, description="Employee hire date")
    password: Optional[str] = Field(None, description="Employee password")
    gender: Optional[str] = Field(None, description="Employee gender")
    role: Optional[str] = Field(None, description="Employee role")
    manager_id: Optional[int] = Field(None, description="Employee manager ID")
    dob: Optional[date] = Field(None, description="Employee date of birth")

class EmployeeResponse(BaseModel):
    employee_id: int = Field(..., description="Employee ID")
    name: str = Field(..., description="Employee name")
    email: str = Field(..., description="Employee email")
    phone: Optional[str] = Field(None, description="Employee phone number")
    designation: str = Field(..., description="Employee designation")
    department: str = Field(..., description="Employee department")
    hire_date: Optional[date] = Field(None, description="Employee hire date")
    gender: Optional[str] = Field(None, description="Employee gender")
    role: str = Field(..., description="Employee role")
    manager_id: Optional[int] = Field(None, description="Employee manager ID")
    dob: Optional[date] = Field(None, description="Employee date of birth")

    class Config:
        from_attributes = True 
