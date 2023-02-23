# Pydantic
from pydantic import EmailStr

# FastAPI
from fastapi import HTTPException

# SQL Alchemy
from sqlalchemy.orm import Session

# Local Packages
from . import models, schemas

#----------------------------------------------
## Users
class UserRequests():
    def __init__(self, db: Session):
        self.db = db

    ### Get user by email
    def get_user_by_email(self, email: EmailStr):
        return self.db.query(models.User).filter(models.User.email == email).first()

    ### Get all users
    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.User).offset(skip).limit(limit).all()

    ### Get user by id
    def get_user_by_id(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    ### Create a User
    def create_user(self, user: schemas.UserCreate):
        db_user = self.get_user_by_email(email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        fake_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, password=fake_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    ### Delete user
    def delete_user(self, email: EmailStr):
        db_user = self.get_user_by_email(email=email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.db.delete(db_user)
        self.db.commit()
        return

#----------------------------------------------
## Movies
class MovieRequests():
    def __init__(self, db: Session):
        self.db = db

    ### Get movie by user
    def get_movie_by_user(self, user_id: int):
        return self.db.query(models.Movie).filter(models.Movie.owner_id == user_id).all()
    
    ### Get all movies
    def get_movies(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Movie).offset(skip).limit(limit).all()
    
    ### Get movie by category
    def get_movie_by_category(self, category: str, skip: int = 0, limit: int = 100):
        return self.db.query(models.Movie).filter(models.Movie.category == category).offset(skip).limit(limit).all()
    
    ### Get movie by movie_id
    def get_movie_by_movie_id(self, movie_id: int, limit: int):
        return self.db.query(models.Movie).filter(models.Movie.id == movie_id).limit(limit).first()

    ### Create a Movie
    def create_user_movie(self, movie: schemas.MovieCreate, user_id: int):
        db_movie = models.Movie(**movie.dict(), owner_id=user_id)
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie
    
    ### Delete a Movie by movie_id
    def delete_movie_by_movie_id(self, movie_id: int, limit: int):
        db_movie = self.get_movie_by_movie_id(movie_id=movie_id, limit=limit)
        if db_movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        self.db.delete(db_movie)
        self.db.commit()
        return

    ### Update Movie by movie_id
    def update_movie_by_movie_id(self, movie_id: int, movie: schemas.Movie, limit: int):
        db_movie = self.get_movie_by_movie_id(movie_id=movie_id, limit=limit)
        if db_movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
    
        db_movie.title = movie.title
        db_movie.overview = movie.overview
        db_movie.year = movie.year
        db_movie.rating = movie.rating
        db_movie.category = movie.category

        self.db.commit()
        return

