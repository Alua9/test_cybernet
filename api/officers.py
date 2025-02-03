from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from db.models import Officer, Department
from schemas.officers import OfficerCreateRequest, OfficerCreateResponse, OfficersListResponse, OfficerInfo, \
    OfficerDetailResponse, OfficerUpdateRequest, OfficerUpdateResponse, OfficerDeleteResponse
from utils import logged_in

router = APIRouter(
    prefix="/officers",
    tags=["officers"],
    dependencies=[Depends(logged_in)]
)


@router.get("/")
async def get_officers_list(
        session: Annotated[AsyncSession, Depends(get_session)],
        department_id: int | None = None
) -> OfficersListResponse:
    query = select(Officer)
    if department_id:
        query = query.filter(Officer.department_id == department_id)

    db_officers = (
        await session.execute(query)
    ).scalars()

    if not db_officers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Officers not found'
        )

    data = []
    for officer in db_officers:
        data.append(
            OfficerInfo(
                id=officer.id,
                first_name=officer.first_name,
                last_name=officer.last_name,
                email=officer.email,
                department_id=officer.department_id
            )
        )

    return OfficersListResponse(
        total=len(data),
        data=data
    )


@router.post("/create/")
async def create_officer(
        officer: OfficerCreateRequest,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> OfficerCreateResponse:
    db_department = (
        await session.execute(
            select(Department).filter(Department.id == officer.department_id)
        )
    ).scalar()

    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    db_officer = Officer(
        first_name=officer.first_name,
        last_name=officer.last_name,
        email=officer.email,
        department_id=officer.department_id
    )

    session.add(db_officer)

    try:
        await session.commit()
        await session.refresh(db_officer)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Officer with this email already exists."
        )

    return OfficerCreateResponse(
        id=db_officer.id,
        first_name=db_officer.first_name,
        last_name=db_officer.last_name,
        email=db_officer.email,
        department_id=db_officer.department_id
    )


@router.get("/{officer_id}/")
async def get_officer(
        officer_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> OfficerDetailResponse:
    db_officer = (
        await session.execute(
            select(Officer).filter(Officer.id == officer_id)
        )
    ).scalar()

    if not db_officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Officer not found'
        )

    return OfficerDetailResponse(
        id=db_officer.id,
        first_name=db_officer.first_name,
        last_name=db_officer.last_name,
        email=db_officer.email,
        department_id=db_officer.department_id
    )


@router.put("/{officer_id}/update/")
async def update_department(
        officer_id: int,
        officer: OfficerUpdateRequest,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> OfficerUpdateResponse:
    db_officer = (
        await session.execute(
            select(Officer).filter(Officer.id == officer_id)
        )
    ).scalar()

    if not db_officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Officer not found'
        )

    if officer.first_name:
        db_officer.first_name = officer.first_name
    if officer.last_name:
        db_officer.last_name = officer.last_name
    if officer.email:
        db_officer.email = officer.email
    if officer.department_id:
        db_officer.department_id = officer.department_id

    try:
        await session.commit()
        await session.refresh(db_officer)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Officer with this email already exists."
        )

    return OfficerUpdateResponse(
        id=db_officer.id,
        first_name=db_officer.first_name,
        last_name=db_officer.last_name,
        email=db_officer.email,
        department_id=db_officer.department_id
    )


@router.delete("/{officer_id}/delete/")
async def delete_officer(
        officer_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
)-> OfficerDeleteResponse:
    db_officer = (
        await session.execute(
            select(Officer).filter(Officer.id == officer_id)
        )
    ).scalar()

    if not db_officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Officer not found'
        )

    await session.delete(db_officer)
    await session.commit()
    return OfficerDeleteResponse(
        message="Officer Successfully Deleted"
    )
