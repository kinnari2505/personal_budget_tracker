'''
UserBase → Shared fields (username, email)

UserCreate → Used for registration (adds password)

UserOut → Response model for sending user data (includes id + uses orm_mode)

Token → Structure for JWT auth response
'''

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    username: str
    email: EmailStr
    # role: Optional[str] = 'user'

    class Config:
        from_attributes = True   # Pydantic v2: enables reading ORM objects


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
