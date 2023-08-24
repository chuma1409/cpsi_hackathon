from fastapi import FastAPI, HTTPException
import sqlite3
import json
import numpy as np
import face_recognition
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
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
    face_encoding: list[float] 

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
    patient_id = result[1]
    datef = datetime.now()
    cursor.execute("INSERT INTO visits (patient_id, reason_for_visit, visit_date) VALUES (?, ?, ?)",
                   (patient_id,"consultation" , datef))
    cursor.close()
    conn.close()

    if result is None: 
        raise HTTPException(status_code=404, detail="Patient not found")
    
    saved_encoding = json.loads(result[0])
    results = compare_face_encodings(face_encoding, [saved_encoding])

    return {"verification_results": results[0]}

@app.get("/get_number_of_bookings")
def get_number_of_bookings():
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()

    # Get the current date without the time
    current_date = datetime.date.today()

    # Convert the current date to a string in the format 'YYYY-MM-DD'
    current_date_str = current_date.strftime('%Y-%m-%d')

    # Execute the SQL query to count the bookings before today's date
    cursor.execute("SELECT COUNT(*) FROM visits WHERE strftime('%Y-%m-%d', visit_date) = ?", (current_date,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {"number_of_bookings": result[0]}

def addbooking(patient_id, reason_for_visit, date_time):
    
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

@app.get("/get_bookings")
def get_bookings():
    conn = sqlite3.connect("healthdb.db")
    cursor = conn.cursor()

    # Get the current date without the time
    current_date = datetime.now().date()

    # Convert the current date to a string in the format 'YYYY-MM-DD'
    current_date_str = current_date.strftime('%Y-%m-%d')

    # Execute the SQL query to get the bookings for today
    cursor.execute("SELECT patient_id, reason_for_visit, visit_date FROM visits WHERE strftime('%Y-%m-%d', visit_date) = ? ORDER BY visit_date", (current_date_str,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    collection_bookings = []
    consultation_bookings = []
    collection_interval = 10  # Interval for collection bookings in minutes
    other_interval = 30  # Initial interval for other bookings in minutes

    for row in result:
        patient_id = row[0]
        conn = sqlite3.connect("healthdb.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT name, last_name FROM patient WHERE id = ?", (patient_id,))
        res = cursor.fetchone()

        booking = {
            "name": res[0],
            "surname": res[1],
            "reason_for_visit": row[1],
            "consultation_time": None
        }

        if row[1] == "Collection":
            booking["consultation_time"] = (datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes=collection_interval)).strftime('%Y-%m-%d %H:%M:%S')
            collection_interval += 10  # Increase interval for collection bookings
            collection_bookings.append(booking)
        else:
            booking["consultation_time"] = (datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes=other_interval)).strftime('%Y-%m-%d %H:%M:%S')
            other_interval += 30  # Increase interval for other bookings
            consultation_bookings.append(booking)

    return {"collection_bookings": collection_bookings, "consultation_bookings": consultation_bookings}

