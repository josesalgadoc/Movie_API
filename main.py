#Python
from typing import List # Para especificar un campo opcional en el esquema BaseModel
# from jwt_manager import create_token, validate_token
# from uuid import UUID

#Pydantic
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Depends, Form, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.security import HTTPBearer

#SQL Alchemy
from sqlalchemy.orm import Session

#Local Modules
from sql_app import crud, database, schemas


database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.title = "First FastAPI"
# app.version = "0.0.1"

# uvicorn main:app --reload --port 5000 --host 0.0.0.0
# Buscar en celular ipPC:port

'''class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid Credentials!")'''

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

# Dependency database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags = ["Users"]
    )
def login(
    email: EmailStr = Form(...),
    password: str = Form(...),
    # db: Session = Depends(get_db())
):
    pass
    # for user in users:
    #     if user["email"] == email and user["password"] == password:
    #         return user
    # return JSONResponse(content={email :"Email or password incorrect!"})
        

### Create a user
@app.post(
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
    # users.append(user)
    db_user = crud.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db=db, user=user)
    return jsonable_encoder(user)

### Get all users
@app.get(
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
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return JSONResponse(status_code=200, content=jsonable_encoder(users))

### Get a user by id
@app.get(
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
    user = crud.get_user_by_id(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't have a movie")
    return jsonable_encoder(user)

#---------------------------------------
##Movie

## Create movie
@app.post(
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
    crud.create_user_movie(db=db, movie=movie, user_id=user_id)
    # movies.append(movie)
    return JSONResponse(status_code=201, content={"Message": "Movie registered successfully!"})

### Get all movies
@app.get(
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
    movies = crud.get_movies(db=db, skip=skip, limit=limit)
    
    if movies is None:
        raise HTTPException(status_code=404, detail="Dont exist movies")
    return jsonable_encoder(movies)

### Get a movie by user
@app.get(
    path="/movies/{user_id}", 
    response_model=schemas.Movie,
    status_code=status.HTTP_200_OK,
    summary="Get movie by User",
    tags = ["Movies"]
    )
def get_movie_by_user(
    user_id: int = Path(
        ge=1, 
        le=200
    ),
    db: Session = Depends(get_db)
):
    movie = crud.get_movie_by_user(db=db, user_id=user_id)
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))
            
### Show a movie by category
@app.get(
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
    movies = crud.get_movie_by_category(db=db, category=movie_category, skip=skip, limit=limit)
    
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail="Movie category not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

### Update movie
@app.put(
    path="/movies/update/{id}", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Update a movie",
    tags=["Movies"], 
    )
def update_movie(
    id: int, 
    movie: schemas.Movie,
    # db: Session = Depends(get_db)
):
    [movies[index].update(movie) for index, item in enumerate(movies) if item["id"] == id]
    return JSONResponse(status_code=200, content={"Message": "Movie updated successfully!"})

### Delete movie
@app.delete(
    path="/movies/delete/{id}", 
    response_model=dict, 
    status_code=status.HTTP_200_OK,
    summary="Delete a movie",
    tags=["Movies"], 
    )
def delete_movie(
    movie_id: int, 
    limit: int = 1,
    # movie: schemas.Movie,
    db: Session = Depends(get_db)
):
    # [movies.remove(item) for item in movies if item["id"] == id]
    db_movie = crud.get_movie_by_movie_id(db=db, movie_id=movie_id, limit=limit)

    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200, content={"Message": "Movie deleted successfully!"})


