#Local Modules
from .database import Base

#SQL Alchemy
from sqlalchemy import Boolean, Column, ForeignKey, Float, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    movies = relationship("Movie", back_populates="owner")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True) 
    overview = Column(String, index=True)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="movies")

