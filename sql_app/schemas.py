#Python 
from typing import Optional
from uuid import UUID

#Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr


#Schemas
class UserBase(BaseModel):
    email: EmailStr = Field(...)

class UserCreate(UserBase):
    user_id: UUID = Field(...)
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(
        min_length=5,
        max_length=15
        )
    overview: str = Field(
        min_length=15, 
        max_length=50
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
    
    #Examples
    class Config:
        schema_extra = {
            "example" : {
                "id": 1,
                "title": "My Movie",
                "overview": "Movie Description",
                "year": 2022,
                "rating": 9.0,
                "category": "Accion"
            }
        }