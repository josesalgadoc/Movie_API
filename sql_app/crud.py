#Pydantic
from pydantic import EmailStr

#SQL Alchemy
from sqlalchemy.orm import Session

#Local Packages
from . import models, schemas

#----------------------------------------------
## Users

### Create a User
def create_user(db: Session, user: schemas.UserCreate):
    fake_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

### Get all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

### Get user by id
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

### Get user by email
def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


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
def get_movie_by_movie_id(db: Session, movie_id: int, limit: int = 1):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).limit(limit).first()

### Update movie
# def update_movie(db: Session, user_id: int, limit: int = 1):
#     return db.query(models.Movie)
