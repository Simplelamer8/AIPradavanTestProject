import db.models as models
from sqlalchemy import and_
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import requests
import os
from schemas import APIBinding

BASE_URL = os.getenv("BASE_API_URL")


def fetch_random_person():
    response = requests.get(BASE_URL)
    return response.json()

def fetch_person_nationality(nationality: str):
    url = f"{BASE_URL}/?nat={nationality}"
    response = requests.get(url)
    return response.json()

def create_new_person(response, db):

    results = response['results'][0]
    gender = results['gender']
    name = results['name']
    title = name['title']
    first_name = name['first']
    last_name = name['last']
    location = results['location']
    city = location['city']
    country = location['country']
    email = results['email']
    nationality = results['nat']
    dict_person = {'gender': gender, 'title': title, 'first_name': first_name, 'last_name': last_name, 'city': city, 'country': country, 'email': email, 'nationality': nationality}
    
    # print("new_person: ", dict_person)
    new_person = models.Person(**dict_person)
    res = db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person

def validate(params):
    if params.gender:
        params.gender = params.gender.lower()
    if params.nationality:
        params.nationality = params.nationality.upper()
        if len(params.nationality) != 2:
            raise ValueError("Nationality field must have the length of 2")
    
def validate_and_search(params, db):
    try:
        validate(params)
    except ValueError as e:
        raise e
    
    params = params.model_dump()

    filter_condition = [getattr(models.Person, key) == params[key] for key in params.keys() if params[key] is not None]

    people = db.query(models.Person).filter(and_(*filter_condition)).all()
    return people

def update_person_db(params, db):
    try:
        validate(params)
    except ValueError as e:
        raise e
    
    person = db.query(models.Person).filter(models.Person.id == params.id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    params = params.model_dump()
    params = {key: value for key, value in params.items() if value is not None}

    print(params)
    for key in params:
        setattr(person, key, params[key])
    
    db.commit()
    db.refresh(person)
    
    return person

def delete_person_db(id, db):
    person = db.query(models.Person).filter(models.Person.id == id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        db.delete(person)
        db.commit()
        return {"message": f"Person with id {id} deleted succesfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB error: " + str(e))