'''
UserBase → Shared fields (username, email)

UserCreate → Used for registration (adds password)

UserOut → Response model for sending user data (includes id + uses orm_mode)

Token → Structure for JWT auth response
'''

from pydantic import BaseModel, EmailStr, field_validator,Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(...,min_length=3, max_length=20)
    email: EmailStr
    is_admin: bool = False


class UserCreate(UserBase):
    password: str = Field(...,min_length=6, max_length=32)

    @field_validator("password")
    def validate_password(cls,v):
        if  " " in v:
            raise ValueError("Password can not contain spaces")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v
    
    @field_validator("username")
    def validate_username(cls,v):
        if not v.isalnum():
            raise ValueError("Username must contain only letters and numbers")
        return v



class UserOut(UserBase):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True   # Pydantic v2: enables reading ORM objects


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
