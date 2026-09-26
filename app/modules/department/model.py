from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base

class Department(Base):
    __tablename__='departments'

    department_id = Column(Integer,primary_key=True,index=True)
    departmentName = Column(String(100),nullable=False,unique=True)
    description = Column(Text,nullable=True)

