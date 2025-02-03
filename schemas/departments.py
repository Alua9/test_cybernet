from pydantic import BaseModel


class DepartmentCreateRequest(BaseModel):
    name: str

class DepartmentCreateResponse(BaseModel):
    id: int
    name: str

class DepartmentUpdateRequest(BaseModel):
    name: str | None = None

class DepartmentUpdateResponse(BaseModel):
    id: int
    name: str

class DepartmentInfo(BaseModel):
    id: int
    name: str

class DepartmentsListResponse(BaseModel):
    total: int
    data: list[DepartmentInfo]

class DepartmentDetailResponse(BaseModel):
    id: int
    name: str

class DepartmentDeleteResponse(BaseModel):
    message: str