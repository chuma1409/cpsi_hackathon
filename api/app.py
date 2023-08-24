from fastapi import FastAPI, HTTPException
import sqlite3
import json
import numpy as np
import face_recognition
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import datetime
app = FastAPI()
origins = [
    "*",  # Update this with your actual frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
conn = sqlite3.connect("healthdb.db")
cursor = conn.cursor()

class PatientVerificationRequest(BaseModel):
    id_number: str
g    face_encoding: list[float] 

class DoctorVerificationRequest(BaseModel):
    name: str
    password: str

@app.get("/get_user_by_id/{id_number}")
def get_user_by_id(id_number: str):
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_number, name, last_name, encoding FROM patient WHERE id_number = ?", (id_number,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {
        "id_number": result[0],
        "name": result[1],
        "last_name": result[2]
    }
    return user_data

def compare_face_encodings(new_encoding, saved_encodings):
    new_encoding_np = np.array(new_encoding)
    saved_encodings_np = np.array(saved_encodings)
    
    results = face_recognition.compare_faces(saved_encodings_np, new_encoding_np)
    
    # Convert NumPy boolean values to Python booleans
    results_python = [bool(result) for result in results]
    
    return results_python

@app.post("/verify_face")
def verify_face(request: PatientVerificationRequest):
    id_number = request.id_number
    face_encoding = request.face_encoding
    
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT encoding,id FROM patient WHERE id_number = ?", (id_number,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None: 
        raise HTTPException(status_code=404, detail="Patient not found")
    
    saved_encoding = json.loads(result[0])
    results = compare_face_encodings(face_encoding, [saved_encoding])
    patient_id = result[1]
    # if results[0]:
    #     datef = datetime.datetime.now()
    #     addbooking(patient_id, request.reason_for_visit, datef)
    return {"verification_results": results[0]}

@app.get("/get_number_of_bookings")
def get_number_of_bookings():
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visits WHERE visit_date < date('now')")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"number_of_bookings": result[0]}

def addbooking(patient_id, reason_for_visit, date_time):
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visits (patient_id, reason_for_visit, visit_date) VALUES (?, ?, ?)",
                   (patient_id, reason_for_visit, date_time))
    conn.commit()
    cursor.close()
    conn.close()
    
@app.post("/doctor")
def get_doctor(login: DoctorVerificationRequest):
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()
    password = login.password
    name = login.name
    cursor.execute("SELECT id_number, name, last_name, password FROM doctor WHERE name = ?", (name,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail="invalid credentials")

    if result[3] != password:
        raise HTTPException(status_code=404, detail="invalid credentials")
    doctor_data = {
        "id_number": result[0],
        "name": result[1],
        "last_name": result[2]
    }
    return doctor_data

