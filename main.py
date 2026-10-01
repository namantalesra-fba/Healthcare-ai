from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database import get_connection
from backend.nlp_processor import extract_symptoms
from backend.predictor import DiseasePredictor


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Healthcare AI",
    description="Local AI-powered healthcare screening and appointment system",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ML PREDICTOR
# ============================================================

predictor = DiseasePredictor()


# ============================================================
# REQUEST MODELS
# ============================================================

class SymptomRequest(BaseModel):
    text: str


class AppointmentRequest(BaseModel):
    slot_id: int
    doctor_id: int
    patient_name: str
    patient_contact: str
    disease_predicted: str
    symptoms: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Healthcare AI backend is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# AI SYMPTOM PREDICTION
# ============================================================

@app.post("/predict")
def predict_symptoms(request: SymptomRequest):

    user_text = request.text

    symptoms = extract_symptoms(user_text)

    if not symptoms:
        return {
            "success": False,
            "message": "No recognizable symptoms were detected.",
            "symptoms": [],
        }

    result = predictor.predict(symptoms)

    return {
        "success": True,
        "input": user_text,
        "symptoms": symptoms,
        "prediction": result,
    }


# ============================================================
# GET DOCTORS
# ============================================================

@app.get("/doctors")
def get_doctors(
    specialization: Optional[str] = None
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if specialization:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    specialization,
                    hospital,
                    contact,
                    fee
                FROM doctors
                WHERE LOWER(specialization) = LOWER(?)
                """,
                (specialization,),
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    specialization,
                    hospital,
                    contact,
                    fee
                FROM doctors
                """
            )

        doctors = cursor.fetchall()

        return {
            "success": True,
            "doctors": [
                dict(doctor)
                for doctor in doctors
            ],
        }

    finally:

        connection.close()


# ============================================================
# GET AVAILABLE SLOTS
# ============================================================

@app.get("/doctors/{doctor_id}/slots")
def get_doctor_slots(
    doctor_id: int
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # Check doctor
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                name,
                specialization,
                hospital,
                contact,
                fee
            FROM doctors
            WHERE id = ?
            """,
            (doctor_id,),
        )

        doctor = cursor.fetchone()

        if not doctor:

            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        # ----------------------------------------------------
        # Available slots
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                doctor_id,
                date,
                start_time,
                end_time,
                is_booked
            FROM slots
            WHERE doctor_id = ?
            AND is_booked = 0
            ORDER BY date, start_time
            """,
            (doctor_id,),
        )

        slots = cursor.fetchall()

        return {
            "success": True,
            "doctor": dict(doctor),
            "slots": [
                dict(slot)
                for slot in slots
            ],
        }

    finally:

        connection.close()


# ============================================================
# BOOK APPOINTMENT
# ============================================================

@app.post("/appointments")
def book_appointment(
    request: AppointmentRequest
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # Check doctor
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM doctors
            WHERE id = ?
            """,
            (request.doctor_id,),
        )

        doctor = cursor.fetchone()

        if not doctor:

            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        # ----------------------------------------------------
        # Check slot
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM slots
            WHERE id = ?
            AND doctor_id = ?
            """,
            (
                request.slot_id,
                request.doctor_id,
            ),
        )

        slot = cursor.fetchone()

        if not slot:

            raise HTTPException(
                status_code=404,
                detail="Appointment slot not found"
            )

        # ----------------------------------------------------
        # Check whether slot is already booked
        # ----------------------------------------------------

        if slot["is_booked"] == 1:

            raise HTTPException(
                status_code=409,
                detail="This appointment slot is already booked"
            )

        # ----------------------------------------------------
        # Create timestamp
        # ----------------------------------------------------

        created_at = datetime.now().isoformat(
            timespec="seconds"
        )

        # ----------------------------------------------------
        # Insert appointment
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO appointments
            (
                slot_id,
                doctor_id,
                patient_name,
                patient_contact,
                disease_predicted,
                symptoms,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request.slot_id,
                request.doctor_id,
                request.patient_name,
                request.patient_contact,
                request.disease_predicted,
                request.symptoms,
                created_at,
            ),
        )

        appointment_id = cursor.lastrowid

        # ----------------------------------------------------
        # Mark slot as booked
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE slots
            SET is_booked = 1
            WHERE id = ?
            """,
            (request.slot_id,),
        )

        # ----------------------------------------------------
        # Commit transaction
        # ----------------------------------------------------

        connection.commit()

        # ----------------------------------------------------
        # Return confirmation
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Appointment booked successfully",
            "appointment": {
                "id": appointment_id,
                "patient_name": request.patient_name,
                "patient_contact": request.patient_contact,
                "disease_predicted": request.disease_predicted,
                "symptoms": request.symptoms,
                "created_at": created_at,
                "doctor": dict(doctor),
                "slot": dict(slot),
            },
        }

    except HTTPException:

        connection.rollback()

        raise

    except Exception as error:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Could not book appointment: {error}"
        )

    finally:

        connection.close()