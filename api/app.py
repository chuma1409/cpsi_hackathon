from fastapi import FastAPI, HTTPException
import sqlite3
import json
import numpy as np
import face_recognition
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
    cursor.execute("SELECT encoding FROM patient WHERE id_number = ?", (id_number,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None: 
        raise HTTPException(status_code=404, detail="Patient not found")
    
    saved_encoding = json.loads(result[0])
    results = compare_face_encodings(face_encoding, [saved_encoding])

    return {"verification_results": results[0]}
