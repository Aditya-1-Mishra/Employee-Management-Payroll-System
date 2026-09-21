from sqlalchemy import Column, Integer, String, Date,ForeignKey 
from sqlalchemy.orm import relationship

from app.core.database import Base

class Employee(Base):
    __tablename__= 'employees'

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    email = Column(String(100), unique=True,nullable=False)
    phone = Column(String(15),unique=True,nullable=True)
    dob = Column(Date,nullable=True)
    password = Column(String(100),nullable=False)
    status = Column(String(10),nullable=False,default='active')
    gender = Column(String(10),nullable=True)

    role_id = Column(Integer,ForeignKey('roles.role_id'),nullable=False)
    department_id = Column(Integer,ForeignKey('departments.department_id'),nullable=False)
    designation_id = Column(Integer,ForeignKey('designations.designation_id'),nullable=False)
    manager_id = Column(Integer,ForeignKey('employees.employee_id'),nullable=True)

    '''back_populates is used to define one sided realtionship between two tables. Where backref is used only in one variable but it automatically creates a new variable in the other table.'''
    role = relationship('Role', backref='employees')
    department = relationship('Department', backref='employees')
    designation = relationship('Designation', backref='employees')
    manager = relationship('Employee',remote_side=[employee_id], backref='subordinates') 
    

