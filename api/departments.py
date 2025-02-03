from fastapi import HTTPException, Depends, APIRouter, status
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from db.models import Department
from schemas.departments import DepartmentCreateRequest, DepartmentCreateResponse, DepartmentUpdateRequest, \
    DepartmentUpdateResponse, DepartmentDetailResponse, DepartmentsListResponse, DepartmentInfo, \
    DepartmentDeleteResponse
from utils import logged_in

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    dependencies=[Depends(logged_in)]
)


@router.get("/")
async def get_departments_list(
        session: Annotated[AsyncSession, Depends(get_session)]
)-> DepartmentsListResponse:
    # db_departments = session.query(Department).all()
    db_departments = (
        await session.execute(select(Department))
    ).scalars()

    if not db_departments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Departments not found'
        )
    data = []
    for department in db_departments:
        data.append(
            DepartmentInfo(
                id=department.id,
                name=department.name
            )
        )
    return DepartmentsListResponse(
        total=len(data),
        data=data
    )


@router.post("/create/")
async def create_department(
        department: DepartmentCreateRequest,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> DepartmentCreateResponse:
    db_department = Department(name=department.name)
    session.add(db_department)
    try:
        await session.commit()
        await session.refresh(db_department)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department already exists."
        )

    return DepartmentCreateResponse(
        id=db_department.id,
        name=db_department.name
    )


@router.get("/{department_id}/")
async def get_department(
        department_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> DepartmentDetailResponse:
    # db_department = session.query(Department).filter(Department.id == department_id).first()
    db_department = (
        await session.execute(
            select(Department).filter(Department.id == department_id)
        )
    ).scalar()

    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department not found'
        )
    return DepartmentDetailResponse(
        id=db_department.id,
        name=db_department.name
    )



@router.put("/{department_id}/update/")
async def update_department(
        department_id: int,
        department: DepartmentUpdateRequest,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> DepartmentUpdateResponse:
    # db_department = session.query(Department).filter(Department.id == department_id).first()
    db_department = (
        await session.execute(
            select(Department).filter(Department.id == department_id)
        )
    ).scalar()

    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department not found'
        )

    if department.name:
        db_department.name = department.name

    try:
        await session.commit()
        await session.refresh(db_department)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department already exists."
        )

    return DepartmentUpdateResponse(
        id=db_department.id,
        name=db_department.name
    )



@router.delete("/{department_id}/delete/")
async def delete_department(
        department_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> DepartmentDeleteResponse:
    # db_department = session.query(Department).filter(Department.id == department_id).first()
    db_department = (
        await session.execute(
            select(Department).filter(Department.id == department_id)
        )
    ).scalar()

    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department not found'
        )

    await session.delete(db_department)
    await session.commit()
    return DepartmentDeleteResponse(
        message="Department Successfully Deleted"
    )

