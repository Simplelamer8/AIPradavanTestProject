### deployed project link: https://aipradavantestproject.onrender.com/docs#/
### To test the deployed version, it might take you from 1 to 10-15 minutes for the application to function again.

# How to run the app on local?
### 1) Clone the repository:
git clone <repository_url>  
cd <project_name>

### 2) Set up virtual environment:

python -m venv .venv

On Windows:  
.venv\Scripts\activate

On macOS/Linux:  
source .venv/bin/activate


### 3) Install dependencies:  
pip install -r requirements.txt

### 4) The project uses deployed PostgreSQL database
### 5) Create enviroment variables by adding .env file to the root of the project directory and add the following variables:  
DB_URL=postgresql://aipradavan_user:9ZQKLhpy5ju7Xu4pO4T15XYAt2cxyoQ9@dpg-ct9cekpu0jms73cp78jg-a.frankfurt-postgres.render.com/aipradavan  
BASE_API_URL=https://randomuser.me/api/  
SECRET_KEY = HLrZakkjVqsSyE8KADgASD4fUZhnlFBWKlfgsJTpG4je9B8iLOLgk2i3k3xbOvkpJck=  
ALGORITHM=HS256  
  
### 6) Run the application:  
uvicorn main:app --reload

### 7) Test the application:
#### Using docs: http://127.0.0.1:8000/docs
#### Base url: http://127.0.0.1:8000

### Endpoints:
#### GET Requests:  
http://127.0.0.1:8000/people/get_random_person  
The endpoint return random user from external API  

http://127.0.0.1:8000/people/get_random_person_and_save  
The endpoint requests random user and saves in DB, returns the saved data  

http://127.0.0.1:8000/people/get_people_from_db
Returns all of the people data saved in DB  

#### Post Requests:  
http://127.0.0.1:8000/people/get_people_from_db_search
Returns the data in People table based on the search field values you provide  

http://127.0.0.1:8000/people/API_bundle  
Returns the data of people from DB that has indicated Nationality and the result from the call to external API  


#### Update:
http://127.0.0.1:8000/people/update_person
Requires authentication, Include the user id and the field values to which you want to change data.  

#### Delete:  
http://127.0.0.1:8000/people/delete_person_by_id  
Deletes the person data using the id you provide  

### USERS  
#### Post:  
http://127.0.0.1:8000/users/  
Creates the user, include the following fields, e.g.:  
{  
  "email": "user@example.com",  
  "password": "string",  
  "repeat_password": "string"  
}  

#### Get:
http://127.0.0.1:8000/users/{id}  
Include the {id} value to get the data about the user account   


#### Login, POST method:  
http://127.0.0.1:8000/login  
Include the fields:  
{  
  "email": "user@example.com",  
  "password": "string",  
}  
To enter the account and get the JWT token  
