from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


lecturers = {
    1: {
        "name": "Wesonga",
        "course": "IT",
        "salary": 99000
    },
    2: {
        "name": "Gavuna",
        "course": "Medicine",
        "salary": 100000
    },
    3: {
        "name": "Kabuye",
        "course": "Engineering",
        "salary": 110000
    }
}

class Lecturer(BaseModel):
    name: str
    course: str
    salary: int


@app.get("/")
def index():
    return {
        "message": "Server running"
    }

@app.get("/lecturers")
def get_lecturers():
    return {
        "message": "Query success",
        "data": lecturers
    }
    
    
    
@app.get("/get-by-id/{lecturer_id}")
def get_lecturer(lecturer_id: int):
    if lecturer_id in lecturers:
        return {
            "message": "Query success",
            "data": lecturers[lecturer_id]
        }
    return {
        "message": "lecturer not found"
    }
    

@app.post("/create-lecturer/{lecturer_id}")
def create_lecturer(lecturer_id: int, lecturer: Lecturer):
    if lecturer_id in lecturers:
        return {
            "message": "Lecturer already exists"
        }
    lecturers[lecturer_id] = lecturer
    return {
        "message" : "Lecturer created successfully",
        "data": lecturer
    }