from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str

