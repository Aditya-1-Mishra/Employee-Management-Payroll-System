from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: str | None = None


class RoleResponse(BaseModel):
    role_id: int
    name: str

    class Config:
        from_attributes = True
