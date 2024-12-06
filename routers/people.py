from fastapi import APIRouter, Depends, HTTPException
import db.models as models
from db.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
import requests
import oauth2
from schemas import PeopleSearch, PersonUpdate, PersonResponse, APIBinding
from db.people import create_new_person, validate_and_search, update_person_db, delete_person_db
import os
from db.people import fetch_random_person, fetch_person_nationality

router = APIRouter(
    prefix="/people",
    # tags=["People"]
)

BASE_URL = os.getenv("BASE_API_URL")

@router.get("/get_random_person", tags=['External API call & operations with DB'])
async def get_random_person():
    """
    ### Get random user from external API.
    """

    return fetch_random_person()


@router.get("/get_random_person_and_save", tags=['External API call & operations with DB'])
async def get_random_person_and_save(db: Session = Depends(get_db)):
    """
    ### Get random user (person in DB) from external API & save in DB, not all fields are saved in DB
    """


    response = fetch_random_person()
    new_person = create_new_person(response, db)

    return new_person


@router.get("/get_people_from_db", tags=['External API call & operations with DB'])
async def get_people_from_db(db: Session = Depends(get_db)):
    """
    ### Get all users(people) saved in DB 
    """

    people = db.query(models.Person).all()
    return people


@router.post("/get_people_from_db_search", tags=["External API call & operations with DB"])
async def get_people_from_db_search(params: PeopleSearch, db: Session = Depends(get_db)):
    """
        ### Perform seach in DB, indicating the values for fields indicated below:
    """

    try:
        people = validate_and_search(params, db)
        return people
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


@router.post("/API_bundle", tags=["Getting data both from DB and External API"])
async def get_person_nationality(params: APIBinding, db: Session = Depends(get_db)):
    """
        ### The endpoint combines the result for the call to external and local DB, you provide the Nat. and get the result from external API and local DB. 
    """

    try:
        people = db.query(models.Person).filter(models.Person.nationality == params.nationality).all()

        response = fetch_person_nationality(params.nationality)

        return {"DataFromLocalDB": people, "DataFromAPICall": response}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB error: " + str(e))

@router.put("/update_person", response_model=PersonResponse, tags=["Requires authentication"])
async def update_person(params: PersonUpdate, db: Session = Depends(get_db), user: dict = Depends(oauth2.get_current_users)):
    """
        ## You need to create an account and login to perform this operation. To create an account navigate to Users and Authentication endpoints below
        ### Update user(person in DB) by providing the id and the fields you want to change. 
    """

    try:
        updated_person = update_person_db(params, db)
        return updated_person
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/delete_person_by_id", tags=["Requires authentication"])
async def delete_person_by_id(id: int, db: Session = Depends(get_db), user: dict = Depends(oauth2.get_current_users)):
    """
        ## You need to create an account and login to perform this operation. To create an account navigate to Users and Authentication endpoints below
        ### Delete user(person in DB) by ID.
    """
    
    try:
        return delete_person_db(id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB error: " + str(e))