# Python
from typing import List

# FastApi
from fastapi import APIRouter, Depends, status
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