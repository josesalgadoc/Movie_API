# Python
# from jwt_manager import create_token, validate_token

# FastAPI
from fastapi import FastAPI
# from fastapi.security import HTTPBearer

# Local Modules
from sql_app import database
from routers import home, movies, users
from middlewares import error_handler

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.title = "MovieAPI"
# app.version = "0.0.1"
# uvicorn main:app --reload --port 5000 --host 0.0.0.0
# Buscar en celular ipPC:port

# Middleware
app.add_middleware(error_handler.ErrorHandler)

# Routers
app.include_router(home.router)
app.include_router(users.router)
app.include_router(movies.router)

'''class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid Credentials!")'''

