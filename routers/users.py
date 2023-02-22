# Python
from typing import List
#Pydantic
from pydantic import EmailStr
# FastApi
from fastapi import APIRouter, Depends, Form,HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
# Local Modules
from sql_app import crud, schemas
from dependencies import *
#SQL Alchemy
from sqlalchemy.orm import Session

router = APIRouter()

### Get all users
@router.get(
        path="/users",
        response_model=List[schemas.User],
        status_code=status.HTTP_200_OK,
        summary="Get all users",
        tags=["Users"]
    )
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = crud.UserRequests(db).get_users(skip=skip, limit=limit)
    return JSONResponse(status_code=200, content=jsonable_encoder(users))

### Get a user by id
@router.get(
        path="/users/{user_id}",
        response_model=schemas.User, 
        status_code=status.HTTP_200_OK,
        summary="Get User by id",
        tags=["Users"]
    )
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = crud.UserRequests(db).get_user_by_id(user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't have a movie")
    return jsonable_encoder(user)

### Create a user
@router.post(
        path="/users",
        response_model=schemas.User,
        status_code=status.HTTP_201_CREATED,
        summary="Create a user",
        tags=["Users"]
    )
def create_a_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    user = crud.UserRequests(db).create_user(user=user)
    return jsonable_encoder(user)

### Login
@router.post(
    path="/login", 
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags = ["Users"]
    )
def login(
    email: EmailStr = Form(...),
    password: str = Form(...),
    # db: Session = Depends(get_db)
):
    pass
    # for user in users:
    #     if user["email"] == email and user["password"] == password:
    #         return user
    # return JSONResponse(content={email :"Email or password incorrect!"})

### Delete user by email
@router.delete(
        path="/users/delete",
        response_model=dict,
        status_code=status.HTTP_200_OK, 
        summary="Delete a user by email", 
        tags=["Users"]
)
def delete_user_by_email(
    email: EmailStr,
    db: Session = Depends(get_db)
):
    crud.UserRequests(db).delete_user(email=email)
    return JSONResponse(status_code=200, content={"Message": "User deteled successfully!"})

