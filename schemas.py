from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    repeat_password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class PeopleSearch(BaseModel):
    id: Optional[int] = None
    gender: Optional[str] = None
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    email: Optional[EmailStr] = None
    nationality: Optional[str] = None

class PersonUpdate(BaseModel):
    id: int
    gender: Optional[str] = None
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    email: Optional[EmailStr] = None
    nationality: Optional[str] = None

class PersonResponse(BaseModel):
    id: int
    gender: str
    title: str
    first_name: str
    last_name: str
    city: str
    country: str
    email: EmailStr
    nationality: str


class APIBinding(BaseModel):
    nationality: str