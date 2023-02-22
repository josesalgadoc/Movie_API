# Local Modules
from sql_app import database


# Dependency database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()