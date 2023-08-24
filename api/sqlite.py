import sqlite3
import json
import face_recognition
import numpy as np
conn = sqlite3.connect("api/healthdb.db")
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE patient (
#     id INTEGER PRIMARY KEY,
#     id_number TEXT NOT NULL UNIQUE,
#     name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     encoding TEXT NOT NULL
# )
# ''')

# cursor.execute('''
# CREATE TABLE visits (
#     id INTEGER PRIMARY KEY,
#     patient_id INTEGER NOT NULL,
#     reason_for_visit TEXT NOT NULL,
#     visit_date TIMESTAMP NOT NULL,
#     FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
# )
# ''')
# delete the doctor table
cursor.execute('''DROP TABLE visits''')
cursor.execute('''CREATE TABLE visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    reason_for_visit TEXT,
    visit_date DATETIME
);''')


conn.commit()
conn.close()

def insert_patient(conn, id_number, name, last_name, encoding):
    encoded_array_as_json = json.dumps(encoding.tolist()) 
    conn.execute("INSERT INTO patient (id_number, name, last_name, encoding) VALUES (?, ?, ?, ?)",
                 (id_number, name, last_name, encoded_array_as_json))
    conn.commit()

def insert_doctor(conn, id_number, name, last_name, password):
    conn.execute("INSERT INTO doctor (id_number, name, last_name, password) VALUES (?, ?, ?, ?)",
                 (id_number, name, last_name, password))
    conn.commit()
    
# insert_doctor(conn, "0105085616123", "musa", "rambuda", "1234")
# insert_doctor(conn, "0105085616044", "charles", "rambuda", "1234")
# ondwela_image = face_recognition.load_image_file("api/ondwela.jpg")
# encoding_array = face_recognition.face_encodings(ondwela_image)[0] 
# insert_patient(conn, "0105085616123", "ondwela", "rambuda", encoding_array)

# chuma_image = face_recognition.load_image_file("api/chuma.jpg")
# encoding_array = face_recognition.face_encodings(chuma_image)[0] 
# insert_patient(conn, "0105085616124", "chuma", "rambuda", encoding_array)

# conn.close()

