#SQL Alchemy
from sqlalchemy.orm import Session

#Local Packages
from . import models, schemas

#----------------------------------------------
#Create
##Create a User
def create_user(db: Session, user: schemas.UserCreate):
    fake_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def create_user_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


#----------------------------------------------
# Read
##Read a User