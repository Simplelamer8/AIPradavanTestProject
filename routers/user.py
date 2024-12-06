from fastapi import APIRouter, Depends, status, HTTPException
import db.models as models
from db.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse
from typing import Union
from utils import hash_password



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Union[UserResponse, dict])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if user.password != user.repeat_password:
            return {"status": "400", "data": "password and repeat_password fields are not the same!"}
        
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        dict_user = user.model_dump()
        dict_user.pop("repeat_password")
        new_user = models.User(**dict_user)
        res = db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        print(e)
        return {"status": "400", "data": "Some error happened while creating a new user..."}

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user