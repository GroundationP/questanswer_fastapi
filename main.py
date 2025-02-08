from fastapi import FastAPI, HTTPException, File, UploadFile, Header, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from base64 import b64decode
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import io
import csv
import random

app = FastAPI()
security = HTTPBasic()
users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}
admin = {
    "admin": "4dm1N"
}


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in users or not password in users[username]:
        raise HTTPException(
            status_code=403,
            detail="Incorrect user name or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
    
    
def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in admin or not password in admin[username]:
        raise HTTPException(
            status_code=403,
            detail="Incorrect admin name or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return {"message": f"Hello {username}"}
    
@app.get("/admin")
def get_current_admin(username: str = Depends(get_current_admin)):
    return {"message": f"Hello {username}"}
    
# Load the CSV file
csv_file_path = "/Users/terence/A_NOTEBOOKS/Datasciencetest/API/FASTAPI/fastapi_exam_ARAUJOVIEIRADEANDRADE/questions.csv"
q_data = pd.read_csv(csv_file_path).fillna("NA")

@app.get("/verify")
def read_root():
    return {"message": "L'API est fonctionnelle."}

@app.get("/upload_csv")
def get_data():
    #print("Uploading CSV file")
    # Convert a sample of the DataFrame to JSON
    question_db = q_data.to_dict(orient="records")
    return question_db
    

@app.get('/upload_csv/{test_type:str}/{categories:str}')
def get_test(test_type, categories):
    try:
        use = list(filter(lambda x: (x['use']==test_type and x['subject']==categories), get_data()))
        use.append({"number_of_questions": len(use)})
        return use
    except IndexError:
        return {}
    
@app.post("/generate_quiz/{test_type:str}/{categories:str}/{number_of_questions:int}")  
def generate_quiz(test_type, categories, number_of_questions, username: str = Depends(get_current_user)):
    Question_db = get_data()
    if test_type not in ['Test de positionnement', 'Test de validation', 'Total Bootcamp', "multiple_choice"]:
        raise HTTPException(status_code=400, detail=f"Unknown test_type: {test_type}")  
    elif categories not in ['BDD', 'Systèmes distribués', 'Streaming de données', 'Docker', 'Classification', 'Sytèmes distribués', 'Data Science', 'Machine Learning', 'Automation']:
        raise HTTPException(status_code=400, detail=f"Unknown category: {categories}")
    for q in range(number_of_questions):
            New_Quest = random.choice(get_data())
            New_Quest["use"] = test_type
            New_Quest["subject"] = categories
            Question_db.append(New_Quest)
    return Question_db
    
@app.post("/create_question/{question:str}/{subject:str}/{correct:str}/{use:str}/{responseA:str}/{responseB:str}/{responseC:str}/{responseD:str}/{remark:str}")
def create_question(
    question: str,
    subject: str,
    correct: str,
    use: str,
    responseA: str,
    responseB: str,
    responseC: str,
    responseD: str,
    remark: str,
    username: str = Depends(get_current_admin)
    ):
    Question_db = get_data()
    new_question = {
        "question": question,
        "subject": subject,
        "use": use,
        "correct": correct,
        "responseA": responseA,
        "responseB": responseB,
        "responseC": responseC,
        "responseD": responseD,
        "remark": remark
    }
    Question_db.append(new_question)
    return {"message": "Question créée avec succès."}
