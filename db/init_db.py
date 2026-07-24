from db.database import engine, Base
from db.models import User
from db.database import Base, engine
from db.models import *

def init_db():
    Base.metadata.create_all(bind=engine)
    print("ALL TABLES CREATED")

if __name__ == "__main__":
    init_db()


