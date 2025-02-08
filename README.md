# Question answer management - fastapi
Example of FastAPI usage to handle multiple choice questions

In this exercise, we will simulate the implementation of an API designed to handle French questions collected via the web or a smartphone. The API includes a basic authentication system, where the username and password are mandatory. On the user side, they are able to query the database, to generate and retrieve the number of selected questions by test and category type. To achieve this, three main endpoints have been implemented (User/Admin authentication, loading questions and add new questions).

#  To setup environment 
python3 -m venv env_fastapi
cd env_fastapi/bin
source activate env_fastapi
pip install -r requirements.txt

# To call API
fastapi dev main.py

# Example of GET query (open a new terminal)
curl -X 'GET' \
  'http://127.0.0.1:8000/upload_csv' \
  -H 'accept: application/json'
