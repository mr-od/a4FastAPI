from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from fastapi import Form


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: Optional[str] = Field(None)
    # is_admin: Optional[bool] = Field(None)
    is_admin: Optional[bool] = False


class CreateUserSchema(UserBaseSchema):
    password: str = Field(..., min_length=8)

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)


class UpdateUserSchema(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    phone: Optional[str]


class UserSchema(UpdateUserSchema):
    id: int
    is_active: bool = True
    created: datetime
    updated: datetime
    is_admin: bool
    is_admin: bool

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
