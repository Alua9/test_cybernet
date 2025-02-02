from pydantic import BaseModel


class OfficerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
