#Pydantic
from pydantic import EmailStr
#FastAPI
from fastapi import HTTPException
#SQL Alchemy
from sqlalchemy.orm import Session
#Local Packages
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

### Create a Movie
def create_user_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

### Get all movies
def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

### Get movie by user
def get_movie_by_user(db: Session, user_id: int):
    return db.query(models.Movie).filter(models.Movie.owner_id == user_id).all()

### Get movie by category
def get_movie_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).filter(models.Movie.category == category).offset(skip).limit(limit).all()

### Get movie by movie_id
def get_movie_by_movie_id(db: Session, movie_id: int, limit: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).limit(limit).first()

# ### Update movie
# def update_movie(db: Session, movie_id: int, limit: int, movie: schemas.Movie):
#     db_movie = get_movie_by_movie_id(db=db, movie_id=movie_id, limit=limit)

#     db_movie.title = movie.title
#     db_movie.overview = movie.overview
#     db_movie.year = movie.year
#     db_movie.rating = movie.rating
#     db_movie.category = movie.category

#     db.commit()
#     return