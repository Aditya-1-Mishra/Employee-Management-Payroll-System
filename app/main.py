from fastapi import FastAPI
from app.modules.employee.route import router as employee_router
from app.modules.department.route import router as department_router
from app.core.database import Base, engine

## execute this command to create all tables in the database
# Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(employee_router)
app.include_router(department_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Employee Management and Payroll System API!"}
