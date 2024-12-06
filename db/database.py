from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://aipradavan_user:9ZQKLhpy5ju7Xu4pO4T15XYAt2cxyoQ9@dpg-ct9cekpu0jms73cp78jg-a.frankfurt-postgres.render.com/aipradavan"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()