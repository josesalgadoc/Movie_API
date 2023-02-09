#Python
from typing import Optional, List # Para especificar un campo opcional en el esquema BaseModel
from jwt_manager import create_token, validate_token

#Pydantic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

#SQL
from sql_app.config.database import Base, Engine, SessionLocal
from sql_app.models.movie import Movie


app = FastAPI()
app.title = "First FastAPI"
# app.version = "0.0.1"
Base.metadata.create_all(bind=Engine)

# uvicorn main:app --reload --port 5000 --host 0.0.0.0
# Buscar en celular ipPC:port

# Models
class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(
        min_length=5,
        max_length=15
        )
    overview: str = Field(
        min_length=15, 
        max_length=50
        )
    year: int = Field(
        le=2022
        )
    rating: float = Field(
        ge=1, 
        le=10
        )
    category: str = Field(
        min_length=5, 
        max_length=15
        )

    #Examples

    class Config:
        schema_extra = {
            "example" : {
                "id": 1,
                "title": "My Movie",
                "overview": "Movie Description",
                "year": 2022,
                "rating": 9.0,
                "category": "Accion"
            }
        }

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

## Home message
@app.get(
    path="/", 
    tags = ["home"]
    )
def message():
    return HTMLResponse("<h1>Welcome FastAPI</h1>")

## Login user
@app.post(
    path="/login", 
    tags = ["auth"]
    )
def login(
    user: User
):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

## Show all movies
@app.get(
    path="/movies", 
    tags = ["movies"], 
    response_model=List[Movie], 
    status_code=200,
    dependencies=[Depends(JWTBearer())]
    )
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

## Show a movie
@app.get(
    path="/movies/{id}", 
    tags = ["movies"], 
    response_model=Movie
    )
def filter_movies(
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
    tags = ["movies"], 
    response_model=List[Movie]
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
    tags = ["movies"],
    response_model=dict, 
    status_code=201
    )
def create_movie(
    movie: Movie
) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"Message": "Movie registered successfully!"})

## Update movie
@app.put(
    path="/movies/{id}", 
    tags = ["movies"], 
    response_model=dict, 
    status_code=200
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
    tags = ["movies"], 
    response_model=dict, 
    status_code=200
    )
def delete_movie(
    id: int, 
    movie: Movie
) -> dict:
    [movies.remove(item) for item in movies if item["id"] == id]
    return JSONResponse(status_code=200, content={"Message": "Movie deleted successfully!"})

