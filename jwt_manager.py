from jwt import encode, decode

def create_token(data: dict):
    token: str = encode(payload=data, key="secrete_key", algorithm="HS256") #payload--> Contenido que convertiré al token
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="secrete_key", algorithms=['HS256'])
    return data

'''## Buena práctica para ra que la clave no sea facil en descifrar

pip install python-dotenv
from jwt import encode
from dotenv import load_dotenv
import os

load_dotenv()


defcreate_token(data: dict) -> str:
    token: str = encode(payload=data,
                        key=os.getenv('SECRET_KEY'),
                        algorithm="HS256"
                        )
    return token'''