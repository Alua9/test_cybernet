from pydantic import BaseModel


class OfficerCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int


class OfficerCreateResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int


class OfficerInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int

class OfficersListResponse(BaseModel):
    total: int
    data: list[OfficerInfo]

class OfficerDetailResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int


class OfficerUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    department_id: int | None = None

class OfficerUpdateResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int


class OfficerDeleteResponse(BaseModel):
    message: str
