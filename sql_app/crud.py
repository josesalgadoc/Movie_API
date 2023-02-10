#SQL Alchemy
from sqlalchemy.orm import Session

#Local Packages
from . import models, schemas

#Create

##Create a User
def create_user(db: Session, user: schemas.UserCreate):
    fake_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def create_movie(db: Session, movie: schemas.Movie, user_id: int):
    db_movie = models.Movie(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

# Read

##Read a User