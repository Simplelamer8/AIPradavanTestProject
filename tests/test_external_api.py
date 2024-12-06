import pytest
from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

BASE_API_URL = os.getenv("BASE_API_URL")

@pytest.mark.integration
def test_get_random_person():
    """
    Test the `/get_random_person` endpoint to verify it fetches data from the external API.
    """
    response = client.get("/people/get_random_person")
    assert response.status_code == 200, "Failed to fetch random person from external API"
    data = response.json()


    assert "results" in data, "Response does not contain 'results'"
    assert isinstance(data["results"], list), "'results' should be a list"
    assert len(data["results"]) > 0, "No results returned from API"


@pytest.mark.integration
def test_get_random_person_and_save():
    """
    Test the `/get_random_person_and_save` endpoint to verify it saves external API data to the database.
    """
    response = client.get("/people/get_random_person_and_save")
    assert response.status_code == 200, "Failed to fetch and save person from external API"
    data = response.json()

    assert "id" in data, "Saved person object does not contain an ID"
    assert "first_name" in data, "Saved person object does not contain a first_name"
    assert "last_name" in data, "Saved person object does not contain a last_name"
    assert "nationality" in data, "Saved person object does not contain a nationality"
    assert "gender" in data, "Saved person object does not contain a gender"
    


@pytest.mark.integration
def test_get_person_nationality():
    """
    Test the `/API_bundle` endpoint to verify integration of external API and DB data.
    """
    nationality = "US"
    response = client.post("/people/API_bundle", json={"nationality": nationality})
    assert response.status_code == 200, "Failed to fetch nationality data from API and DB"
    data = response.json()

    assert "DataFromLocalDB" in data, "Missing 'DataFromLocalDB' in response"
    assert "DataFromAPICall" in data, "Missing 'DataFromAPICall' in response"
    assert isinstance(data["DataFromAPICall"], dict), "'DataFromAPICall' should be a dictionary"
