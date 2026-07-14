import os
import sqlite3
import json
from datetime import datetime

# Define database paths
DB_DIR = "database"
USERS_DB = os.path.join(DB_DIR, "users.db")
PATIENTS_DB = os.path.join(DB_DIR, "patients.db")

def init_dbs():
    """Initializes the SQLite databases and tables if they do not exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    
    # Initialize Users Database
    conn_u = sqlite3.connect(USERS_DB)
    cursor_u = conn_u.cursor()
    cursor_u.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            hospital TEXT,
            role TEXT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TEXT
        )
    """)
    conn_u.commit()
    conn_u.close()
    
    # Initialize Patients Database
    conn_p = sqlite3.connect(PATIENTS_DB)
    cursor_p = conn_p.cursor()
    
    # Patients Table
    cursor_p.execute("""
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            height REAL,
            weight REAL,
            created_at TEXT
        )
    """)
    
    # Predictions Table
    cursor_p.execute("""
        CREATE TABLE IF NOT EXISTS Predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            prediction_date TEXT,
            model_name TEXT,
            probability REAL,
            risk_level TEXT,
            kidney_health_score REAL,
            inputs TEXT, -- JSON format of clinical parameters
            ai_summary TEXT,
            FOREIGN KEY(patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
        )
    """)
    
    # Reports Table
    cursor_p.execute("""
        CREATE TABLE IF NOT EXISTS Reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            prediction_id INTEGER,
            report_path TEXT,
            created_at TEXT,
            FOREIGN KEY(patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY(prediction_id) REFERENCES Predictions(id) ON DELETE CASCADE
        )
    """)
    
    # Alerts Table
    cursor_p.execute("""
        CREATE TABLE IF NOT EXISTS Alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            prediction_id INTEGER,
            risk_level TEXT,
            alert_message TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT,
            FOREIGN KEY(patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY(prediction_id) REFERENCES Predictions(id) ON DELETE CASCADE
        )
    """)
    
    # ChatHistory Table
    cursor_p.execute("""
        CREATE TABLE IF NOT EXISTS ChatHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT, -- 'user' or 'assistant'
            message TEXT,
            timestamp TEXT
        )
    """)
    
    conn_p.commit()
    
    # Check if empty and seed
    cursor_p.execute("SELECT COUNT(*) FROM Patients")
    if cursor_p.fetchone()[0] == 0:
        seed_data_if_empty(cursor_p)
        conn_p.commit()
        
    conn_p.close()

def seed_data_if_empty(cursor_p):
    """Seeds the database with high-fidelity sample kidney clinical data."""
    # Seed Patients
    patients = [
        ("P-1001", "John Doe", 62, "Male", 175.0, 82.0, "2026-07-10T10:00:00"),
        ("P-1002", "Alice Smith", 45, "Female", 162.0, 58.0, "2026-07-11T11:30:00"),
        ("P-1003", "Robert Johnson", 58, "Male", 180.0, 95.0, "2026-07-12T09:15:00"),
        ("P-1004", "Emily Davis", 70, "Female", 155.0, 65.0, "2026-07-13T14:45:00"),
        ("P-1005", "Michael Wilson", 34, "Male", 172.0, 70.0, "2026-07-14T08:00:00")
    ]
    cursor_p.executemany("INSERT INTO Patients VALUES (?, ?, ?, ?, ?, ?, ?)", patients)
    
    # Seed Predictions
    predictions = [
        (1, "P-1001", "2026-07-10T10:15:00", "Random Forest", 0.85, "High Risk", 15.0,
         json.dumps({
             "age": 62, "gender": 1, "height": 175.0, "weight": 82.0,
             "blood_pressure": 155.0, "blood_glucose": 145.0, "serum_creatinine": 3.2,
             "blood_urea": 75.0, "albumin": 3, "hemoglobin": 10.2, "sodium": 132.0, "potassium": 5.2,
             "hypertension": 1, "diabetes": 1, "smoking": 1, "alcohol": 0, "family_history": 1
         }),
         "Clinical signs of severe renal impairment detected. Elevated creatinine (3.2 mg/dL) and high-grade albuminuria (Grade 3+) point to advanced nephron dysfunction. Urgent nephrology consultation is required."),
         
        (2, "P-1002", "2026-07-11T11:45:00", "XGBoost", 0.12, "Low Risk", 88.0,
         json.dumps({
             "age": 45, "gender": 0, "height": 162.0, "weight": 58.0,
             "blood_pressure": 118.0, "blood_glucose": 92.0, "serum_creatinine": 0.8,
             "blood_urea": 25.0, "albumin": 0, "hemoglobin": 13.8, "sodium": 140.0, "potassium": 4.1,
             "hypertension": 0, "diabetes": 0, "smoking": 0, "alcohol": 0, "family_history": 0
         }),
         "Renal markers are within optimal ranges. Serum creatinine (0.8 mg/dL) and lack of protein in urine suggest normal glomerular filtration rate. Continue routine health checkups."),
         
        (3, "P-1003", "2026-07-12T09:30:00", "SVM", 0.54, "Moderate Risk", 46.0,
         json.dumps({
             "age": 58, "gender": 1, "height": 180.0, "weight": 95.0,
             "blood_pressure": 138.0, "blood_glucose": 115.0, "serum_creatinine": 1.8,
             "blood_urea": 52.0, "albumin": 1, "hemoglobin": 12.1, "sodium": 136.0, "potassium": 4.7,
             "hypertension": 1, "diabetes": 0, "smoking": 0, "alcohol": 1, "family_history": 0
         }),
         "Mild renal impairment indicated. Elevated creatinine (1.8 mg/dL) and microalbuminuria (Grade 1+) suggest early-stage kidney disease. Focus on managing blood pressure and lifestyle modifications."),
         
        (4, "P-1004", "2026-07-13T15:00:00", "MLP", 0.76, "High Risk", 24.0,
         json.dumps({
             "age": 70, "gender": 0, "height": 155.0, "weight": 65.0,
             "blood_pressure": 148.0, "blood_glucose": 180.0, "serum_creatinine": 2.7,
             "blood_urea": 68.0, "albumin": 2, "hemoglobin": 11.0, "sodium": 134.0, "potassium": 4.9,
             "hypertension": 1, "diabetes": 1, "smoking": 0, "alcohol": 0, "family_history": 1
         }),
         "Significant kidney risk detected. Serum creatinine (2.7 mg/dL) is high, accompanied by grade 2+ albuminuria. Underlying hypertension and diabetes are accelerating kidney damage. Urgent referral suggested."),
         
        (5, "P-1005", "2026-07-14T08:15:00", "Logistic Regression", 0.05, "Low Risk", 95.0,
         json.dumps({
             "age": 34, "gender": 1, "height": 172.0, "weight": 70.0,
             "blood_pressure": 112.0, "blood_glucose": 88.0, "serum_creatinine": 0.7,
             "blood_urea": 22.0, "albumin": 0, "hemoglobin": 14.5, "sodium": 141.0, "potassium": 4.0,
             "hypertension": 0, "diabetes": 0, "smoking": 0, "alcohol": 0, "family_history": 0
         }),
         "Renal function is excellent. High kidney health score of 95/100. No key clinical risk factors identified.")
    ]
    
    for pred in predictions:
        cursor_p.execute("""
            INSERT INTO Predictions (id, patient_id, prediction_date, model_name, probability, risk_level, kidney_health_score, inputs, ai_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, pred)
        
    # Seed Alerts
    alerts = [
        (1, "P-1001", 1, "High Risk", "CRITICAL ALERT: Patient P-1001 John Doe is flagged as High Risk (85.0% probability) for kidney failure. High Creatinine (3.2) & Albuminuria.", "Active", "2026-07-10T10:15:00"),
        (2, "P-1004", 4, "High Risk", "CRITICAL ALERT: Patient P-1004 Emily Davis is flagged as High Risk (76.0% probability) for kidney failure. High Creatinine (2.7) & Albuminuria.", "Active", "2026-07-13T15:00:00")
    ]
    cursor_p.executemany("INSERT INTO Alerts VALUES (?, ?, ?, ?, ?, ?, ?)", alerts)

# Users Table Helper Functions
def add_user(fullname, email, phone, hospital, role, username, hashed_password):
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Users (fullname, email, phone, hospital, role, username, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (fullname, email, phone, hospital, role, username, hashed_password, datetime.now().isoformat()))
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            return False, "Email already registered."
        elif "username" in str(e):
            return False, "Username already exists."
        return False, f"Registration failed: {str(e)}"
    finally:
        conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "fullname": user[1],
            "email": user[2],
            "phone": user[3],
            "hospital": user[4],
            "role": user[5],
            "username": user[6],
            "password": user[7],
            "created_at": user[8]
        }
    return None

def update_user_password(username, new_hashed_password):
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (new_hashed_password, username))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

# Patients Table Helper Functions
def save_patient(patient_id, name, age, gender, height, weight):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        # If exists, we can update or keep. Let's insert or replace
        cursor.execute("""
            INSERT INTO Patients (patient_id, name, age, gender, height, weight, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(patient_id) DO UPDATE SET
                name=excluded.name,
                age=excluded.age,
                gender=excluded.gender,
                height=excluded.height,
                weight=excluded.weight
        """, (patient_id, name, age, gender, height, weight, datetime.now().isoformat()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving patient: {e}")
        return False
    finally:
        conn.close()

def get_patient(patient_id):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients WHERE patient_id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "patient_id": row[0],
            "name": row[1],
            "age": row[2],
            "gender": row[3],
            "height": row[4],
            "weight": row[5],
            "created_at": row[6]
        }
    return None

def delete_patient(patient_id):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        # SQLite CASCADE deletes related predictions, alerts, etc., if foreign keys are enabled.
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("DELETE FROM Patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting patient: {e}")
        return False
    finally:
        conn.close()

# Predictions Table Helper Functions
def add_prediction(patient_id, model_name, probability, risk_level, score, inputs_dict, ai_summary):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Predictions (patient_id, prediction_date, model_name, probability, risk_level, kidney_health_score, inputs, ai_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, datetime.now().isoformat(), model_name, probability, risk_level, score, json.dumps(inputs_dict), ai_summary))
        pred_id = cursor.lastrowid
        conn.commit()
        return pred_id
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return None
    finally:
        conn.close()

def get_predictions_for_patient(patient_id):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Predictions WHERE patient_id = ? ORDER BY prediction_date DESC", (patient_id,))
    rows = cursor.fetchall()
    conn.close()
    predictions = []
    for r in rows:
        predictions.append({
            "id": r[0],
            "patient_id": r[1],
            "prediction_date": r[2],
            "model_name": r[3],
            "probability": r[4],
            "risk_level": r[5],
            "kidney_health_score": r[6],
            "inputs": json.loads(r[7]),
            "ai_summary": r[8]
        })
    return predictions

def get_all_predictions():
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pr.id, pr.patient_id, pr.prediction_date, pr.model_name, pr.probability, pr.risk_level, 
               pr.kidney_health_score, pr.inputs, pr.ai_summary, pa.name, pa.age, pa.gender
        FROM Predictions pr
        JOIN Patients pa ON pr.patient_id = pa.patient_id
        ORDER BY pr.prediction_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    predictions = []
    for r in rows:
        predictions.append({
            "id": r[0],
            "patient_id": r[1],
            "prediction_date": r[2],
            "model_name": r[3],
            "probability": r[4],
            "risk_level": r[5],
            "kidney_health_score": r[6],
            "inputs": json.loads(r[7]),
            "ai_summary": r[8],
            "patient_name": r[9],
            "patient_age": r[10],
            "patient_gender": r[11]
        })
    return predictions

def delete_prediction(pred_id):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Predictions WHERE id = ?", (pred_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        return False
    finally:
        conn.close()

# Alerts Table Helper Functions
def add_alert(patient_id, prediction_id, risk_level, alert_message):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Alerts (patient_id, prediction_id, risk_level, alert_message, status, created_at)
            VALUES (?, ?, ?, ?, 'Active', ?)
        """, (patient_id, prediction_id, risk_level, alert_message, datetime.now().isoformat()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving alert: {e}")
        return False
    finally:
        conn.close()

def get_active_alerts():
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT al.id, al.patient_id, al.prediction_id, al.risk_level, al.alert_message, al.status, al.created_at, pa.name
        FROM Alerts al
        JOIN Patients pa ON al.patient_id = pa.patient_id
        WHERE al.status = 'Active'
        ORDER BY al.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    alerts = []
    for r in rows:
        alerts.append({
            "id": r[0],
            "patient_id": r[1],
            "prediction_id": r[2],
            "risk_level": r[3],
            "alert_message": r[4],
            "status": r[5],
            "created_at": r[6],
            "patient_name": r[7]
        })
    return alerts

def resolve_alert(alert_id):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE Alerts SET status = 'Resolved' WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()

# Reports Table Helper Functions
def add_report(patient_id, prediction_id, report_path):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Reports (patient_id, prediction_id, report_path, created_at)
            VALUES (?, ?, ?, ?)
        """, (patient_id, prediction_id, report_path, datetime.now().isoformat()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving report log: {e}")
        return False
    finally:
        conn.close()

def get_reports_for_patient(patient_id):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reports WHERE patient_id = ? ORDER BY created_at DESC", (patient_id,))
    rows = cursor.fetchall()
    conn.close()
    reports = []
    for r in rows:
        reports.append({
            "id": r[0],
            "patient_id": r[1],
            "prediction_id": r[2],
            "report_path": r[3],
            "created_at": r[4]
        })
    return reports

# Chat History Helper Functions
def add_chat_msg(username, role, message):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ChatHistory (username, role, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, (username, role, message, datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        print(f"Error saving chat log: {e}")
    finally:
        conn.close()

def get_chat_history(username):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT role, message, timestamp FROM ChatHistory WHERE username = ? ORDER BY timestamp ASC", (username,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "message": r[1], "timestamp": r[2]} for r in rows]

def clear_chat_history(username):
    conn = sqlite3.connect(PATIENTS_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ChatHistory WHERE username = ?", (username,))
    conn.commit()
    conn.close()
