from fastapi import FastAPI , Path
from typing import Optional
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


app = FastAPI()
 
students = {
    1 :{
        "name":"Niko",
        "age" : 12,
        "address" : "Banepa"
    },
    2 :{
        "name": "BTS",
        "age" : 7,
        "address" : "Korea"
    }
}

class NewStudent(BaseModel):
    name: str
    age = int
    address = str

class UpdateStudent(BaseModel):
    name : Optional(str) = None
    age : Optional(int) =None
    address : Optional(str) = None


@app.get("/")     #<------path parameter#    
def index():
    return {"Name":"first name"}  

@app.get("/student/{id_student}")  
def students_data(id_student : int =  Path(description="This is the student ID box.",gt=0,lt=3)):
    return students[id_student]


@app.get("/get-by-name/{student_id}")
def student_name(student_id :int , name : str = None):
    for students_id in students:
        if students[students_id]["name"] == name:
            return students[students_id]
    return {"name": "not found"}

#add new student
@app.post("/add-student/{student_id}") 
def create_student(student_id : int , student_data = NewStudent ):
    if student_id in students:
        return {"Error" : "Id already present"}

    students[student_id] = student_data 
    return students[student_id] 

#update student 
@app.put("/update-student/{student_id}")
def update_student(student_id : int , student_data = UpdateStudent ):
    if student_id not in students:
        return {"error":"No student with that id is found"}
    if students[student_id].name != None:
        students[student_id].name = student_data.name
    if students[student_id].age != None:
        students[student_id].age = student_data.age
    if students[student_id].address != None:
        students[student_id].address = student_data.address

    return students[student_id]

#delete student
@app.delete("/delete-student/{student_id}")
def deteleStudent(student_id : int):
    if student_id not in students:
        return {"error" : "No student with that id is found"}
    
    
    del students[student_id]
    return {"Message" : "Student Delete Successfully."} 