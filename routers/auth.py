from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import UserLogin, Token
import db.models as models
import utils
import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
        ### In order to do calls to endpoints that require authentication, you need to use "Authorize" button located above the endpoints section of the page (it is small White&Green button with lock image at the right hand side of the screen).
        ### This is just test end point
    """
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    result = utils.verify(userCredentials.password, user.password)

    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #Creating and returning token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}