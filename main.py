
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from typing import List, Optional

import os


load_dotenv()

app = FastAPI()

# Connect to MongoDB Atlas
client = os.getenv("DATABASE_URL")
db = client.Library 


# Data models
class Student(BaseModel):
    name: str
    age: int
    address: dict 


# To store the data into the database
@app.post("/students", status_code=201, response_model=dict)
async def create_student(student: Student):
    result = db.students.insert_one(student.dict())
    return {"id": str(result.inserted_id)}



#retrive the student data from the database
@app.get("/students", response_model=List[Student])
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = age
    return list(db.students.find(query))



#retrive the data with id
@app.get("/students/{id}", response_model=Student)
async def get_student(id: str):
    student = db.students.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student with this respective id is not present into the database")
    return student



#update the student data
@app.patch("/students/{id}", response_model=dict)
async def update_student(id: str, student: Student):
    result = db.students.update_one({"_id": ObjectId(id)}, {"$set": student.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student data is updated into the database")
    return {"message": "Student updated successfully"}




#delete the student 
@app.delete("/students/{id}", response_model=dict)
async def delete_student(id: str):
    result = db.students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student data is deleted from the database")
    return {"message": "Student deleted successfully"}