
#FastAPI
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get(
    path="/", 
    summary="Home message",
    tags = ["Home"]
    )
def home_message():
    return HTMLResponse("<h1>Movie API</h1>")