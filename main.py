from fastapi import FastAPI
import db.models as models
from db.database import engine
from routers import user, auth, people


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Test Project for AIPradavan"
)

app.include_router(people.router)
app.include_router(user.router)
app.include_router(auth.router)