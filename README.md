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

### 4) The project uses PostgreSQL as database, You need to create DB for the project with name "AIPradavan"
### 5) Create enviroment variables by adding .env file to the root of the project directory and add the following variables:  
DB_URL=Link to your local DB  
BASE_API_URL=https://randomuser.me/api/  
SECRET_KEY = HLrZakkjVqsSyE8KADgASD4fUZhnlFBWKlfgsJTpG4je9B8iLOLgk2i3k3xbOvkpJck=  
ALGORITHM=HS256  
  
### 6) Run the application:  
uvicorn main:app --reload

### 7) Test the application:
#### Using docs: http://127.0.0.1:8000/docs
#### Base url: http://127.0.0.1:8000
