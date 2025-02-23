from typing import Optional

from pydantic import BaseModel, EmailStr, condecimal


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = True
    is_superuser: bool = False
    amount: condecimal(max_digits=10, decimal_places=2)


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class UpdateAmount(BaseModel):
    user_id: int
    new_amount: condecimal(max_digits=10, decimal_places=2)
