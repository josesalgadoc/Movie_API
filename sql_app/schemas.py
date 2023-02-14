#Python 
from typing import Optional
from uuid import UUID

#Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr


#----------------------------------------------
##Users
class UserBase(BaseModel):
    email: EmailStr = Field(...)
    is_active: Optional[bool] = None
class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )


#----------------------------------------------
##Movies
class MovieDatabase(BaseModel):
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
    
class MovieCreate(MovieDatabase):
    pass
class Movie(MovieDatabase):
    id: Optional[int] = None
    owner_id: int

class User(UserBase):
    pass
    # user_id: UUID = Field(...)
class UserShow(User, UserCreate):
    class Config:
        orm_mode = True