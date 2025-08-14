from pydantic import BaseModel, EmailStr


class UserGet(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdateName(BaseModel):
    name: str
