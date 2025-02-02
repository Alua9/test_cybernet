from fastapi import HTTPException, Depends, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
from models import Department
from schemas.departments import DepartmentBase


# 1. GET /departments/ - list of all departments
# 2. POST /departments/create/ - create a new department
# 3. GET /departments/{department_id}/ - get a department info
# 4. PUT /departments/{department_id}/update/ - update department info
# 5. DELETE /departments/{department_id}/delete/ - delete department

router = APIRouter()


@router.get("/departments/")
async def read_department(db: Annotated[Session, Depends(get_db)]):
    result = db.query(Department).all()
    if not result:
        raise HTTPException(status_code=404, detail='Departments are not found')
    return result


@router.post("/departments/create/")
async def create_department(department: DepartmentBase, db: Annotated[Session, Depends(get_db)]):
    db_department = Department(name=department.name)#using sqlalchemy to write orm statement that link us a peace of data in database
    db.add(db_department)
    db.commit()


@router.get("/department/{department_id}")
async def read_department(department_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.query(Department).filter(Department.id == department_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Department is not found')
    return result

# @router.put("/departments/{department_id}/update/")
# async def update_department(department: DepartmentBase, db: Annotated[Session, Depends(get_db)]):
#     db_deparment =  Department(name=department.name)
#     db.add(db_officer)
#     db.commit()