# Python
from typing import List # Para especificar un campo opcional en el esquema BaseModel

# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Local Modules

from sql_app import crud, schemas
from dependencies import *

# SQL Alchemy
from sqlalchemy.orm import Session

router = APIRouter()

### Get all movies
@router.get(
    path="/movies", 
    response_model=List[schemas.Movie], 
    status_code=200,
    summary="Get all movies",
    # dependencies=[Depends(JWTBearer())],
    tags = ["Movies"]
    )
def get_movies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    movies = crud.MovieRequests(db).get_movies(skip=skip, limit=limit)
    
    if movies is None:
        raise HTTPException(status_code=404, detail="Dont exist movies")
    return jsonable_encoder(movies)

## Get a movie by user_id
@router.get(
    path="/movies/{user_id}", 
    response_model=schemas.Movie,
    status_code=status.HTTP_200_OK,
    summary="Get movie by User id",
    tags = ["Movies"]
    )
def get_movie_by_user(
    user_id: int = Path(
        ge=1, 
        le=200
    ),
    db: Session = Depends(get_db)
):
    movie = crud.MovieRequests(db).get_movie_by_user(user_id=user_id)
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

## Show a movie by category
@router.get(
    path="/movies/", 
    response_model=List[schemas.Movie],
    status_code=status.HTTP_200_OK,
    summary="Get movie by category",
    tags = ["Movies"]
    )
def get_movies_by_category(
    movie_category: str = Query(
        min_length=2, 
        max_length=15
        ),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    movies = crud.MovieRequests(db).get_movie_by_category(category=movie_category, skip=skip, limit=limit)
    
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail="Movie category not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

## Create movie
@router.post(
    path="/movies/{user_id}", 
    response_model=schemas.Movie, 
    status_code=status.HTTP_200_OK,
    summary="Create a movie for user",
    tags = ["Movies"]
    )
def create_movie_for_user(
    user_id: int,
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db)
):
    crud.MovieRequests(db).create_user_movie(movie=movie, user_id=user_id)
    return JSONResponse(status_code=201, content={"Message": "Movie registered successfully!"})

### Delete movie
@router.delete(
    path="/movies/delete/{movie_id}", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Delete a movie",
    tags=["Movies"], 
    )
def delete_movie(
    movie_id: int, 
    limit: int = 1,
    db: Session = Depends(get_db)
):
    crud.MovieRequests(db).delete_movie_by_movie_id(movie_id=movie_id, limit=limit)
    return JSONResponse(status_code=200, content={"Message": "Movie deleted successfully!"})

### Update movie
@router.put(
    path="/movies/update/{movie_id}", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Update a movie",
    tags=["Movies"], 
    )
def update_movie(
    movie_id: int, 
    movie: schemas.Movie,
    limit: int = 1, 
    db: Session = Depends(get_db)
):
    crud.MovieRequests(db).update_movie_by_movie_id(movie_id=movie_id, movie=movie, limit=limit)
    return JSONResponse(status_code=200, content={"Message": "Movie updated successfully!"})

