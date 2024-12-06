from fastapi import FastAPI, Depends, HTTPException
import db.models as models
from db.database import engine, SessionLocal
from routers import user, auth, people
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.database import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Test Project for AIPradavan"
)

app.include_router(people.router)
app.include_router(user.router)
app.include_router(auth.router)