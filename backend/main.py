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

# Import the disease explanation router
from disease_explanation import router as explanation_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the explanation router
app.include_router(explanation_router)

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
MODEL_PATH = os.path.join(BASE_DIR, "..", "new model", "app", "disease_model.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "..", "new model", "app", "model_metrics.pkl")
SYMPTOMS_PATH = os.path.join(BASE_DIR, "models", "symptoms.json")

# Global variables to store model data
model = None
label_encoder = None
model_symptoms = None
feature_vector_template = None

# Cache for disease predictions and feature importances
disease_features_cache = {}
prediction_cache = {}
CACHE_TIMEOUT = 300  # 5 minutes

# Load the model and encoders with lower memory usage
try:
    print("Loading model files...")
    
    # Load model bundle with optimized memory mapping
    print("Loading disease prediction model (this may take a moment)...")
    model_bundle = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
    
    # Extract components from the bundle
    if isinstance(model_bundle, dict):
        # Extract model, encoder and symptoms from the bundle
        model = model_bundle.get("model")
        label_encoder = model_bundle.get("encoder")  # Changed from "label_encoder" to "encoder"
        bundle_symptoms = model_bundle.get("symptoms")
        
        if bundle_symptoms:
            SYMPTOMS = bundle_symptoms
            print(f"Loaded {len(SYMPTOMS)} symptoms from model bundle")
        else:
            # Fall back to symptoms.json if bundle doesn't have symptoms
            with open(SYMPTOMS_PATH, 'r') as f:
                symptoms_data = json.load(f)
                SYMPTOMS = symptoms_data['symptoms']
            print(f"Loaded {len(SYMPTOMS)} symptoms from symptoms.json")
    else:
        model = model_bundle
        label_encoder = None
        
        # Load symptoms from file
        with open(SYMPTOMS_PATH, 'r') as f:
            symptoms_data = json.load(f)
            SYMPTOMS = symptoms_data['symptoms']
        print(f"Loaded {len(SYMPTOMS)} symptoms from symptoms.json")

    # If label_encoder is None, load it from create_label_encoder.py output
    if label_encoder is None:
        print("Model bundle missing encoder, loading from separate file...")
        encoder_path = os.path.join(BASE_DIR, "..", "new model", "app", "label_encoder.pkl")
        try:
            label_encoder = joblib.load(encoder_path)
            print(f"Successfully loaded label encoder with {len(label_encoder.classes_)} classes")
        except Exception as e:
            print(f"Error loading label encoder: {e}")
            # Create a simple label encoder
            from sklearn.preprocessing import LabelEncoder
            label_encoder = LabelEncoder()
            if hasattr(model, "classes_"):
                label_encoder.classes_ = model.classes_
                print(f"Created label encoder from model classes: {len(label_encoder.classes_)} classes")
            else:
                # Fallback to common disease names
                print("Using fallback disease classes")
                # Try to read from diseases_list.json
                try:
                    diseases_path = os.path.join(BASE_DIR, "..", "diseases_list.json")
                    with open(diseases_path, 'r') as f:
                        diseases_data = json.load(f)
                        diseases = [d["disease"] for d in diseases_data[:50]]  # Limit to first 50
                        label_encoder.classes_ = np.array(diseases)
                        print(f"Created label encoder with {len(diseases)} diseases from diseases_list.json")
                except Exception as e:
                    print(f"Error loading diseases: {e}")
                    # Hardcoded fallback
                    label_encoder.classes_ = np.array([
                        "Common Cold", "Pneumonia", "Diabetes", "Hypertension", 
                        "Arthritis", "Migraine", "Asthma", "Influenza",
                        "Hepatitis", "Dengue", "Tuberculosis", "Malaria",
                        "Typhoid", "Jaundice", "Chicken pox", "Measles"
                    ])
                    print(f"Created fallback label encoder with {len(label_encoder.classes_)} classes")
    
    # Pre-compute model features and template
    model_symptoms = SYMPTOMS if model.feature_names_in_ is None else model.feature_names_in_
    feature_vector_template = pd.DataFrame(np.zeros((1, len(model_symptoms))), columns=model_symptoms)
    
    # Pre-compute disease features for all diseases
    print("Pre-computing disease features...")
    for idx, disease in enumerate(label_encoder.classes_):
        # Convert disease to string if needed
        disease_str = str(disease) if not isinstance(disease, str) else disease
        
        # Get feature importances for this disease
        if hasattr(model, "feature_importances_"):
            # For single model with feature_importances_ attribute
            disease_features = model.feature_importances_
        elif hasattr(model, "estimators_") and len(model.estimators_) > idx:
            # For ensemble models with estimators
            disease_features = model.estimators_[idx].feature_importances_
        else:
            # Fallback to equal importance
            disease_features = np.ones(len(model_symptoms)) / len(model_symptoms)
        
        disease_features_cache[disease_str] = disease_features
    
    print(f"Initialized prediction system with {len(model_symptoms)} features")
    
except Exception as e:
    print(f"Error loading model and encoders: {str(e)}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for files in: {BASE_DIR}")
    print(f"Model path: {MODEL_PATH}")
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
        full_name=user.full_name,
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
            "is_admin": user.is_admin,
            "user_id": user.id,
            "full_name": user.full_name
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
        if not symptoms.symptoms:
            raise HTTPException(
                status_code=400,
                detail="Please provide at least one symptom"
            )
        
        # Sort symptoms for consistent cache key
        sorted_symptoms = sorted(symptoms.symptoms)
        cache_key = ','.join(sorted_symptoms)
        
        # Check cache first
        cached_result = prediction_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Create feature vector using the template (avoid copying large arrays)
        feature_vector = feature_vector_template.copy()
        valid_symptoms = []
        invalid_symptoms = []
        
        # Map symptoms to feature vector (optimized)
        for symptom in symptoms.symptoms:
            if symptom in model_symptoms:
                feature_vector.at[0, symptom] = 1
                valid_symptoms.append(symptom)
            else:
                invalid_symptoms.append(symptom)
        
        if not valid_symptoms:
            raise HTTPException(
                status_code=400,
                detail="No valid symptoms provided. Please check your symptom names."
            )

        # Get probabilities for all diseases using the model
        probabilities = model.predict_proba(feature_vector)[0]
        
        # Get predictions with confidence scores
        disease_probs = list(zip(label_encoder.classes_, probabilities))
        
        # Define common mental health symptoms (moved outside the loop)
        mental_health_symptoms = {
            'anxiety', 'depression', 'insomnia', 'fatigue', 'mood swings', 
            'irritability', 'stress', 'panic attacks', 'emotional', 'nervousness',
            'anxiety and nervousness', 'depressive or psychotic symptoms'
        }
        
        is_mental_health = any(s in mental_health_symptoms for s in valid_symptoms)
        
        # Filter and sort predictions (optimized)
        relevant_predictions = []
        for disease, prob in disease_probs:
            if prob < 0.15:  # Early skip for low probability
                continue
                
            try:
                # Ensure disease is a string for processing
                disease_str = str(disease) if not isinstance(disease, str) else disease
                
                # Get feature importances for this disease
                disease_features = disease_features_cache.get(disease_str)
                if disease_features is None:
                    # If not in cache, use default importances
                    disease_features = np.ones(len(model_symptoms)) / len(model_symptoms)
                
                # Get important symptoms with their importance scores
                symptom_importance = [(sym, imp) for sym, imp in zip(model_symptoms, disease_features) if imp > 0.01]
                
                # Calculate symptom matches (optimized)
                matching_symptoms = []
                total_importance = 0
                matched_importance = 0
                
                for sym, imp in symptom_importance:
                    total_importance += imp
                    if sym in valid_symptoms:
                        matching_symptoms.append({"symptom": sym, "importance": float(imp)})
                        matched_importance += imp
                
                if not matching_symptoms:
                    continue
                
                # Calculate scores
                symptom_coverage = matched_importance / total_importance if total_importance > 0 else 0
                matching_count = len(matching_symptoms)
                
                # Adjust confidence for mental health conditions
                adjusted_prob = prob
                if is_mental_health:
                    # Convert disease to string if it's not already
                    if any(mh in disease_str.lower() for mh in ['anxiety', 'depression', 'stress', 'disorder', 'mental']):
                        adjusted_prob *= 1.5
                    else:
                        adjusted_prob *= 0.5
                
                severity_score = matched_importance * adjusted_prob
                
                # Only include relevant predictions
                if ((adjusted_prob >= 0.15 and symptom_coverage >= 0.3) or
                    (matching_count >= 2 and adjusted_prob >= 0.4) or
                    (is_mental_health and 
                     any(mh in disease_str.lower() for mh in ['anxiety', 'depression', 'stress']) and 
                     adjusted_prob >= 0.2)):
                    
                    relevant_predictions.append({
                        "disease": disease_str,  # Ensure disease is a string
                        "confidence": float(adjusted_prob),
                        "matching_symptoms": matching_symptoms,
                        "symptom_coverage": float(symptom_coverage),
                        "severity_score": float(severity_score),
                        "matching_count": matching_count
                    })
            except Exception as e:
                print(f"Error processing disease {disease}: {str(e)}")
                continue
        
        # Sort predictions by severity score and confidence
        relevant_predictions.sort(key=lambda x: (x["severity_score"], x["confidence"]), reverse=True)
        
        # Take top 5 most relevant predictions
        top_predictions = relevant_predictions[:5]
        
        if not top_predictions:
            # Use pre-computed features for fallback
            best_matches = []
            for disease, prob in disease_probs:
                if prob < 0.1:  # Skip very low probability matches
                    continue
                    
                try:
                    disease_str = str(disease) if not isinstance(disease, str) else disease
                    disease_features = disease_features_cache.get(disease_str, np.ones(len(model_symptoms)) / len(model_symptoms))
                    matching_count = sum(1 for sym, imp in zip(model_symptoms, disease_features) 
                                      if imp > 0.01 and sym in valid_symptoms)
                    
                    if matching_count > 0:
                        best_matches.append((disease_str, prob, matching_count))
                except Exception as e:
                    continue
            
            if best_matches:
                best_matches.sort(key=lambda x: (x[2], x[1]), reverse=True)
                best_disease = best_matches[0]
                top_predictions = [{
                    "disease": best_disease[0],
                    "confidence": float(best_disease[1]),
                    "matching_symptoms": [{"symptom": s, "importance": 0.01} for s in valid_symptoms],
                    "symptom_coverage": float(best_disease[2]/len(valid_symptoms)),
                    "severity_score": float(best_disease[1] * 0.1),
                    "matching_count": best_disease[2]
                }]
            else:
                top_disease = max(disease_probs, key=lambda x: x[1])
                disease_str = str(top_disease[0]) if not isinstance(top_disease[0], str) else top_disease[0]
                top_predictions = [{
                    "disease": disease_str,
                    "confidence": float(top_disease[1]),
                    "matching_symptoms": [],
                    "symptom_coverage": 0.0,
                    "severity_score": float(top_disease[1] * 0.1),
                    "matching_count": 0
                }]

        # Get recommended doctors (optimized query)
        recommended_doctors = []
        seen_doctors = set()
        
        # Prepare specialty lists for all predictions at once
        all_specialties = set()
        for pred in top_predictions:
            try:
                all_specialties.update(get_relevant_specialties(pred["disease"]))
            except Exception as e:
                print(f"Error getting specialties for {pred['disease']}: {str(e)}")
                # Add default specialties
                all_specialties.update(['Internal Medicine', 'Family Medicine', 'General Practice'])
        
        if is_mental_health:
            all_specialties.update(['psychiatrist', 'psychologist', 'mental health specialist'])
        
        # Batch query for doctors
        specialty_doctors = (
            db.query(models.Doctor)
            .filter(func.lower(models.Doctor.specialization).in_([s.lower() for s in all_specialties]))
            .order_by(models.Doctor.rating.desc())
            .limit(8)
            .all()
        )
        
        # Process doctors
        for doctor in specialty_doctors:
            if doctor.id not in seen_doctors:
                doctor_dict = doctor.__dict__
                doctor_dict["specialty_relevance"] = 1.0
                recommended_doctors.append(doctor_dict)
                seen_doctors.add(doctor.id)
                
                if len(recommended_doctors) >= 8:
                    break
        
        # If we need more doctors, add general practitioners
        if len(recommended_doctors) < 4:
            additional_doctors = (
                db.query(models.Doctor)
                .filter(
                    or_(
                        func.lower(models.Doctor.specialization).in_([
                            'internal medicine',
                            'family medicine',
                            'general practice'
                        ])
                    )
                )
                .order_by(models.Doctor.rating.desc())
                .limit(8 - len(recommended_doctors))
                .all()
            )
            
            for doctor in additional_doctors:
                if doctor.id not in seen_doctors:
                    doctor_dict = doctor.__dict__
                    doctor_dict["specialty_relevance"] = 0.1
                    recommended_doctors.append(doctor_dict)
                    seen_doctors.add(doctor.id)
        
        # Prepare response
        response = {
            "predictions": top_predictions,
            "recommended_doctors": recommended_doctors,
            "input_summary": {
                "valid_symptoms": valid_symptoms,
                "invalid_symptoms": invalid_symptoms,
                "total_symptoms_provided": len(symptoms.symptoms),
                "valid_symptoms_count": len(valid_symptoms)
            }
        }
        
        # Cache the result
        prediction_cache[cache_key] = response
        
        return response
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in disease prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting disease: {str(e)}"
        )

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
            user_id=appointment.userId,
            message=appointment.message,
            status='pending'
        )
        
        try:
            db.add(db_appointment)
            db.commit()
            db.refresh(db_appointment)
            print(f"Appointment created successfully with ID: {db_appointment.id}")
            
            # Create response with doctor information
            appointment_response = {
                "id": db_appointment.id,
                "doctor_id": db_appointment.doctor_id,
                "message": db_appointment.message,
                "status": db_appointment.status,
                "created_at": db_appointment.created_at,
                "doctor": doctor
            }
            return appointment_response
            
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
        
        # Fetch doctor and user information for each appointment
        appointments_with_details = []
        for appointment in appointments:
            doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
            user = db.query(models.User).filter(models.User.id == appointment.user_id).first()
            
            if doctor and user:
                appointment_dict = {
                    "id": appointment.id,
                    "doctor_id": appointment.doctor_id,
                    "user_id": appointment.user_id,
                    "message": appointment.message,
                    "status": appointment.status,
                    "created_at": appointment.created_at,
                    "doctor": doctor,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.full_name,
                        "email": user.email
                    }
                }
                appointments_with_details.append(appointment_dict)
        
        return appointments_with_details
    except Exception as e:
        print(f"Error fetching admin appointments: {str(e)}")
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

@app.get("/api/users/{user_id}/appointments", response_model=List[schemas.AppointmentResponse])
async def get_user_appointments(user_id: int, db: Session = Depends(get_db)):
    try:
        # First verify the user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

        # Get all appointments for the user
        appointments = db.query(models.Appointment).filter(
            models.Appointment.user_id == user_id
        ).order_by(models.Appointment.created_at.desc()).all()
        
        # Fetch doctor and user information for each appointment
        appointments_with_details = []
        for appointment in appointments:
            try:
                doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
                if not doctor:
                    print(f"Warning: Doctor with ID {appointment.doctor_id} not found for appointment {appointment.id}")
                    continue
                
                appointment_dict = {
                    "id": appointment.id,
                    "doctor_id": appointment.doctor_id,
                    "user_id": user_id,
                    "message": appointment.message,
                    "status": appointment.status,
                    "created_at": appointment.created_at,
                    "doctor": doctor,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.full_name,
                        "email": user.email
                    }
                }
                appointments_with_details.append(appointment_dict)
            except Exception as detail_error:
                print(f"Error processing appointment {appointment.id}: {str(detail_error)}")
                continue
        
        return appointments_with_details
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error fetching appointments: {str(e)}")
        db.rollback()  # Explicitly rollback on error
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching appointments: {str(e)}"
        )

@app.get("/api/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
