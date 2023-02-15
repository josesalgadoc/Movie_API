#Python 
from typing import Optional

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#----------------------------------------------
##Movies
class MovieBase(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=50
        )
    overview: str = Field(
        min_length=15, 
        max_length=100
        )
    year: int = Field(
        le=2022
        )
    rating: float = Field(
        ge=1, 
        le=10
        )
    category: str = Field(
        min_length=5, 
        max_length=15
        )
class MovieCreate(MovieBase):
    pass
class Movie(MovieBase):
    id: Optional[int] = None
    owner_id: int
    class Config:
        orm_mode = True

#----------------------------------------------
##Users
class UserBase(BaseModel):
    email: EmailStr = Field(...)
class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
class User(UserBase):
    id: int
    is_active: Optional[bool] = None
    class Config:
        orm_mode = True