#System
import os

#SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Manipular todas las tablas de datos

## Nombre bd
sqlite_name_db = "movie_db.sqlite"

## Leer el directorio actual de este archivo
base_dir = os.path.dirname(os.path.realpath(__file__)) 

## Creando url de la base de datos
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(base_dir, sqlite_name_db)}" # Las tres barras es el como se conecta a una base de datos sqlite

## Motor de la base de datos
Engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

## Crear sesión para conectarse a la db
SessionLocal = sessionmaker(bind=Engine)

## Instancia para manipular tabla de datos
Base = declarative_base()