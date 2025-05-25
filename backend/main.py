from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
import joblib
import json
import os
from database import SessionLocal, engine
import models
from schemas import DoctorResponse, SymptomResponse, SymptomCreate
import schemas
from disease_specialties import get_relevant_specialties
import numpy as np
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths relative to the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_disease_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
SYMPTOMS_PATH = os.path.join(BASE_DIR, "models", "symptoms.json")

# Load the model and encoders with lower memory usage
try:
    print("Loading model files...")
    
    # Load symptoms first as it's the smallest
    with open(SYMPTOMS_PATH, 'r') as f:
        symptoms_data = json.load(f)
        SYMPTOMS = symptoms_data['symptoms']
    print(f"Loaded {len(SYMPTOMS)} symptoms")
    
    # Load label encoder next
    print("Loading label encoder...")
    label_encoder = joblib.load(ENCODER_PATH)
    print("Label encoder loaded successfully")
    
    # Load model with memory mapping
    print("Loading disease prediction model (this may take a moment)...")
    model = joblib.load(MODEL_PATH, mmap_mode='r')
    print("Model loaded successfully!")
    
except Exception as e:
    print(f"Error loading model and encoders: {str(e)}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for files in: {BASE_DIR}")
    print(f"Model path: {MODEL_PATH}")
    print(f"Encoder path: {ENCODER_PATH}")
    print(f"Symptoms path: {SYMPTOMS_PATH}")
    raise

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Disease Prediction API"}

@app.post("/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with plain password
    db_user = models.User(
        username=user.username,
        email=user.email,
        gender=user.gender,
        password=user.password  # Store password as-is
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.LoginResponse)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        # Log the login attempt (without password)
        print(f"Login attempt for username: {user_credentials.username}, admin login: {user_credentials.is_admin_login}")
        
        # Find the user
        user = db.query(models.User).filter(
            models.User.username == user_credentials.username
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
            
        # Check password
        if user.password != user_credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Check admin access if requested
        if user_credentials.is_admin_login and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: Admin access required"
            )
            
        # Log successful login
        print(f"Successful login for user: {user.username}, admin: {user.is_admin}")
            
        return {
            "status": "success",
            "username": user.username,
            "is_admin": user.is_admin
        }
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        # Log the error
        print(f"Unexpected login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.get("/api/symptoms")
async def get_symptoms():
    return {"symptoms": SYMPTOMS}

@app.post("/api/predict", response_model=schemas.PredictionResponse)
async def predict_disease(symptoms: schemas.SymptomsInput, db: Session = Depends(get_db)):
    try:
        print(f"Received prediction request with symptoms: {symptoms.symptoms}")
        
        # Create feature vector with named features
        feature_vector = pd.DataFrame(np.zeros((1, len(SYMPTOMS))), columns=SYMPTOMS)
        for symptom in symptoms.symptoms:
            if symptom in SYMPTOMS:
                feature_vector[symptom] = 1
            else:
                print(f"Warning: Unknown symptom '{symptom}'")
        
        print("Feature vector created")
        print(f"Non-zero features: {feature_vector.loc[0, feature_vector.iloc[0] > 0].index.tolist()}")

        # Make prediction
        print("Making prediction...")
        prediction = model.predict(feature_vector)
        probabilities = model.predict_proba(feature_vector)
        max_prob = np.max(probabilities)
        
        # Get predicted disease name
        disease = label_encoder.inverse_transform(prediction)[0]
        print(f"Predicted disease: {disease} with confidence {max_prob:.2f}")
        
        # Get relevant specialties for the predicted disease
        relevant_specialties = get_relevant_specialties(disease)
        print(f"Relevant specialties: {relevant_specialties}")
        
        recommended_doctors = []
        seen_doctors = set()
        
        # For emergency conditions, prioritize Emergency Medicine and related specialties
        is_emergency = any(specialty in ['Emergency Medicine', 'Critical Care', 'Toxicologist'] 
                         for specialty in relevant_specialties)
        
        # First, try to get doctors for each specialty in order of relevance
        for specialty in relevant_specialties:
            if len(recommended_doctors) >= 6:
                break
                
            specialty_doctors = (
                db.query(models.Doctor)
                .filter(func.lower(models.Doctor.specialization) == specialty.lower())
                .order_by(models.Doctor.rating.desc())
                .all()
            )
            
            # Add up to 2 doctors from each specialty
            count = 0
            for doctor in specialty_doctors:
                if doctor.id not in seen_doctors and count < 2:
                    recommended_doctors.append(doctor)
                    seen_doctors.add(doctor.id)
                    count += 1
                    
                if len(recommended_doctors) >= 6:
                    break
        
        # If we still need more doctors, add highly rated doctors from related specialties
        if len(recommended_doctors) < 6:
            # Get all doctors from related specialties that we haven't added yet
            related_doctors = (
                db.query(models.Doctor)
                .filter(
                    or_(*[
                        func.lower(models.Doctor.specialization) == specialty.lower()
                        for specialty in relevant_specialties
                    ])
                )
                .order_by(models.Doctor.rating.desc())
                .all()
            )
            
            for doctor in related_doctors:
                if doctor.id not in seen_doctors and len(recommended_doctors) < 6:
                    recommended_doctors.append(doctor)
                    seen_doctors.add(doctor.id)
        
        # If we still don't have enough specialists, add highly rated general practitioners
        if len(recommended_doctors) < 4:
            general_doctors = (
                db.query(models.Doctor)
                .filter(
                    or_(
                        func.lower(models.Doctor.specialization) == 'internal medicine',
                        func.lower(models.Doctor.specialization) == 'family medicine',
                        func.lower(models.Doctor.specialization) == 'general practice'
                    )
                )
                .order_by(models.Doctor.rating.desc())
                .limit(6 - len(recommended_doctors))
                .all()
            )
            
            for doctor in general_doctors:
                if doctor.id not in seen_doctors and len(recommended_doctors) < 6:
                    recommended_doctors.append(doctor)
                    seen_doctors.add(doctor.id)
        
        print(f"Found {len(recommended_doctors)} recommended doctors")
        
        return {
            "disease": disease,
            "confidence": float(max_prob),
            "recommended_doctors": recommended_doctors
        }
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

# Admin endpoints
@app.get("/api/admin/doctors")
async def get_all_doctors(db: Session = Depends(get_db)):
    try:
        doctors = db.query(models.Doctor).all()
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/users")
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    try:
        total_users = db.query(models.User).count()
        total_doctors = db.query(models.Doctor).count()
        
        return {
            "totalUsers": total_users,
            "totalDoctors": total_doctors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/doctors")
async def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    try:
        db_doctor = models.Doctor(**doctor.dict())
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, doctor: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    try:
        db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
            
        for key, value in doctor.dict(exclude_unset=True).items():
            setattr(db_doctor, key, value)
            
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
            
        db.delete(doctor)
        db.commit()
        return {"message": "Doctor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages", response_model=schemas.MessageResponse)
async def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    try:
        db_message = models.Message(**message.dict())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/messages", response_model=List[schemas.MessageResponse])
async def get_all_messages(db: Session = Depends(get_db)):
    try:
        messages = db.query(models.Message).order_by(models.Message.created_at.desc()).all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/messages/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    try:
        message = db.query(models.Message).filter(models.Message.id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
            
        db.delete(message)
        db.commit()
        return {"message": "Message deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/appointments", response_model=schemas.AppointmentResponse)
async def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        print(f"Creating appointment for doctor ID: {appointment.doctorId}")
        
        # Check if doctor exists
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Create appointment
        db_appointment = models.Appointment(
            doctor_id=appointment.doctorId,
            message=appointment.message,
            status='pending'
        )
        
        try:
            db.add(db_appointment)
            db.commit()
            db.refresh(db_appointment)
            print(f"Appointment created successfully with ID: {db_appointment.id}")
            return db_appointment
        except Exception as db_error:
            db.rollback()
            print(f"Database error: {str(db_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(db_error)}"
            )
            
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error in create_appointment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/api/admin/appointments", response_model=List[schemas.AppointmentResponse])
async def get_all_appointments(db: Session = Depends(get_db)):
    try:
        appointments = db.query(models.Appointment).order_by(models.Appointment.created_at.desc()).all()
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/appointments/{appointment_id}")
async def update_appointment_status(
    appointment_id: int,
    status: str = Query(..., description="New status for the appointment"),
    db: Session = Depends(get_db)
):
    try:
        appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
            
        if status not in ['pending', 'approved', 'rejected']:
            raise HTTPException(status_code=400, detail="Invalid status")
            
        appointment.status = status
        db.commit()
        db.refresh(appointment)
        return {"message": "Appointment status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SymptomBase(BaseModel):
    name: str
    description: Optional[str] = None

class SymptomCreate(SymptomBase):
    pass

class SymptomResponse(SymptomBase):
    id: int
    specialties: List[str] = []

    class Config:
        orm_mode = True

@app.get("/symptoms/", response_model=List[SymptomResponse])
def get_symptoms(db: Session = Depends(get_db)):
    return db.query(models.Symptom).all()

@app.get("/symptoms/{symptom_id}", response_model=SymptomResponse)
def get_symptom(symptom_id: int, db: Session = Depends(get_db)):
    symptom = db.query(models.Symptom).filter(models.Symptom.id == symptom_id).first()
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom

@app.get("/doctors/by-symptom/{symptom_id}", response_model=List[DoctorResponse])
def get_doctors_by_symptom(symptom_id: int, db: Session = Depends(get_db)):
    # Get the symptom and its specialties
    symptom = db.query(models.Symptom).filter(models.Symptom.id == symptom_id).first()
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    
    # Get the specialties for this symptom from the mapping table
    specialty_query = db.query(symptom_specialty.c.specialty).filter(
        symptom_specialty.c.symptom_id == symptom_id
    )
    specialties = [row[0] for row in specialty_query.all()]
    
    # Find doctors matching any of these specialties
    doctors = db.query(models.Doctor).filter(
        models.Doctor.specialization.in_(specialties)
    ).order_by(models.Doctor.rating.desc()).all()
    
    return doctors

@app.get("/doctors/search/", response_model=List[DoctorResponse])
def search_doctors_by_symptom(query: str, db: Session = Depends(get_db)):
    # Search for symptoms matching the query
    symptoms = db.query(models.Symptom).filter(
        models.Symptom.name.ilike(f"%{query}%")
    ).all()
    
    if not symptoms:
        return []
    
    # Get all specialties from matching symptoms
    specialty_sets = []
    for symptom in symptoms:
        specialty_query = db.query(symptom_specialty.c.specialty).filter(
            symptom_specialty.c.symptom_id == symptom.id
        )
        specialty_sets.append([row[0] for row in specialty_query.all()])
    
    # Flatten the specialty sets
    specialties = list(set([s for subset in specialty_sets for s in subset]))
    
    # Find doctors matching any of these specialties
    doctors = db.query(models.Doctor).filter(
        models.Doctor.specialization.in_(specialties)
    ).order_by(models.Doctor.rating.desc()).all()
    
    return doctors
