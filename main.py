#Python
from typing import List # Para especificar un campo opcional en el esquema BaseModel
from jwt_manager import create_token, validate_token
from uuid import UUID

#Pydantic
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Form, Path, Query, Request, HTTPException, Depends
from fastapi import status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

#Local Modules
from sql_app import crud
from sql_app.schemas import UserBase, Movie
from sql_app.database import Base, Engine, SessionLocal
from sql_app.models import Movie as MovieModel


app = FastAPI()
app.title = "First FastAPI"
# app.version = "0.0.1"
Base.metadata.create_all(bind=Engine)

# uvicorn main:app --reload --port 5000 --host 0.0.0.0
# Buscar en celular ipPC:port

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid Credentials!")

# Database

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un raro e único planeta llamado Pandora, habitado por ...",
        "year": "2009",
        "rating": 8.0,
        "category": "Accion"
    },
    {
        "id": 2,
        "title": "Ant-Man",
        "overview": "Scott Lang, un ladrón de casas, luego de salir de ...",
        "year": "2019",
        "rating": 8.5,
        "category": "Heroes"
    }
]

users = [
    {
        "email": "jose@gmail.com",
        "password": "joseperezpassword"

    },
    {
        "email": "juan@gmail.com",
        "password": "juanperezpassword"
    }
]


#-----------------Path Operations----------------------
## Home message
@app.get(
    path="/", 
    summary="Home message",
    tags = ["Home"]
    )
def message():
    return HTMLResponse("<h1>Welcome FastAPI</h1>")

#---------------------------------------
## Users
### Login user
@app.post(
    path="/login", 
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags = ["Users"]
    )
def login(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

### Show all users
@app.get(
        path="/users",
        response_model=List[UserBase],
        status_code=status.HTTP_200_OK,
        summary="Show a user",
        tags=["Users"]
)
def show_all_users():
    pass

#---------------------------------------
##Movie

### Show all movies
@app.get(
    path="/movies", 
    response_model=List[Movie], 
    status_code=200,
    dependencies=[Depends(JWTBearer())],
    tags = ["Movies"]
    )
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

## Show a movie
@app.get(
    path="/movies/{id}", 
    response_model=Movie,
    status_code=status.HTTP_200_OK,
    summary="Show a movie",
    tags = ["Movies"]
    )
def show_a_movie(
    id: int = Path(
        ge=1, 
        le=2000
        )
) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])
            
## Show a movie by category (Query Params)
@app.get(
    path="/movies/", 
    response_model=List[Movie],
    summary="Show a movie by category",
    tags = ["Movies"]
    )
def get_movies_by_category(
    category: str = Query(
        min_length=5, 
        max_length=15
        )
) -> List[Movie]:
    data = list(filter(lambda item: item["category"] == category, movies))
    return JSONResponse(content=data)

## Create movie
@app.post(
    path="/movies", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Create a movie",
    tags = ["Movies"]
    )
def create_movie(
    movie: Movie
) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"Message": "Movie registered successfully!"})

## Update movie
@app.put(
    path="/movies/{id}", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Update a movie",
    tags=["Movies"], 
    )
def update_movie(
    id: int, 
    movie: Movie
) -> dict:
    [movies[index].update(movie) for index, item in enumerate(movies) if item["id"] == id]
    return JSONResponse(status_code=200, content={"Message": "Movie updated successfully!"})

## Delete movie
@app.delete(
    path="/movies/{id}", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Delete a movie",
    tags=["Movies"], 
    )
def delete_movie(
    id: int, 
    movie: Movie
) -> dict:
    [movies.remove(item) for item in movies if item["id"] == id]
    return JSONResponse(status_code=200, content={"Message": "Movie deleted successfully!"})

