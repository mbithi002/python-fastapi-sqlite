# requirements----commands
# py -m pip install fastapi
# py -m pip install uvicon
# command to run the application: uvicon myapi:app --reload
# replace the myapi with your file name and the app with your vairable name
# now hack


# below we import the fastapi library and instantiate the object
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

# we assign the object to a variable app
app = FastAPI()

# mock data, later data will come from a database

students = {
    1: {
        "name": "John",
        "age": 20,
        "grade": 90
    },
    2: {
        "name": "Jane",
        "age": 21,
        "grade": 85
    }
}

class Student(BaseModel):
    name: str
    age: int
    grade: int

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[int] = None

# our application endpoints
# first define the endpoint method and then the method follows

# GET methods
@app.get("/")
def index():
    return {
        "message": "Hello, World!"
    }
    
@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    if student_id in students:
        return {
            "student": students[student_id]
        }
        
@app.get("/get-by-name/{student_id}")
def get_student_by_name(*, student_id: int, name: Optional[str], test: int):
        for student_id in students:
            if students[student_id]["name"] == name:
                return {
                    "data": students[student_id]
                }
        return {
            "data": "not found"
        }
        

# POST methods
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student: Student):
    if student_id in students:
        return {
            "Error": "Student with the same ID already exists"
        }
    students[student_id] = student
    return {
        "student": student,
        "message": "Student created successfully"
    }
    

# update endpoint
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {
            "Error": f"Student with ID {student_id} does not exist"
        }
    
    # Update only the fields that are provided in the request
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.grade is not None:
        students[student_id]["grade"] = student.grade
    
    return {
        "updated_student": students[student_id],
        "message": "Student updated successfully"
    }
    
# delete endpoint
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {
            "Error" : f"Student with the ID {student_id} does not exist"
        }
    del students[student_id]
    return {
        "message": "Student deleted successfully",
        "data": students
    }
    
@app.get("/students")
def get_students():
    return {
        "students": students
    }