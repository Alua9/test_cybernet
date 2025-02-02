from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import Officer
from schemas.officers import OfficerBase

router = APIRouter()

@router.get("/departments/{department_id}/officers/{officer_id}")
async def read_officer(officer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.query(Officer).filter(Officer.id == officer_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Officer is not found')
    return result


# @app.get("/departments/{department_id}/officers/{officer_id}")
# async def read_officer(officer_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.query(Officer).filter(Officer.id == officer_id).all()
#     if not result:
#         raise HTTPException(status_code=404, detail='Officer is not found')
#     return result




@router.post("/departments/{department_id}/officers/create/")
async def create_officer(department_id: int, officer: OfficerBase, db: Annotated[Session, Depends(get_db)]):
    db_officer = Officer(first_name=officer.first_name, last_name=officer.last_name, email=officer.email, department_id=department_id)
    db.add(db_officer)
    db.commit()

