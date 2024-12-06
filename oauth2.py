from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import get_db
import db.models as models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")#The tokenUrl parameter tells the OAuth2PasswordBearer logic where the token can be gotten from. This is primarily used for the openapi.json and the automatic docs. They will show API endpoints with the little lock, and when entering your user/password it will send a POST request with those user/password credentials to the tokenUrl endpoint to collect a bearer token.

# JOSE -> JS object signing and encryption

SECRET_KEY = "HLrZakkjVqsSyE8KADgASD4fUZhnlFBWKlfgsJTpG4je9B8iLOLgk2i3k3xbOvkpJck="
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    # print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload["user_id"])
        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id = id)
    except:
        raise credentials_exception
    
    return token_data


# def get_current_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user", headers={"WWW-Authenticate": "Bearer"})
#     user_data = verify_access_token(token, credentials_exception)
#     user = db.query(models.User).filter(models.User.id == user_data.id).first()

#     return user

def get_current_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials", headers={"WWW-Authenticate": "Bearer"}) # headers serve as a metadata about the error, it indicates why error happened.
    user_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == user_data.id).first()
    print(type(user))

    return user