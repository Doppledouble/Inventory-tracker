from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

url_object = URL.create(
    "postgresql",
    username="postgres",
    password="Nephilian_10",  # plain (unescaped) text
    host="localhost",
    database="inventory_db",
)

engine = create_engine(url_object)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base  = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()