from pydantic import BaseModel, EmailStr, constr, Field
from datetime import datetime
from typing import Optional, Literal, List

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    full_name: constr(min_length=2, max_length=255)

class UserCreate(UserBase):
    password: constr(min_length=6, max_length=100)
    gender: Literal['male', 'female', 'other']
    is_admin: bool = False

class UserLogin(BaseModel):
    username: str
    password: str
    is_admin_login: bool = False

class UserResponse(UserBase):
    id: int
    gender: str
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    status: str
    username: str
    is_admin: bool
    user_id: int
    full_name: str

class SymptomsInput(BaseModel):
    symptoms: List[str]

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    hospital: str
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True

class MatchingSymptom(BaseModel):
    symptom: str
    importance: float

class DiseasePrediction(BaseModel):
    disease: str
    confidence: float
    matching_symptoms: List[MatchingSymptom]
    symptom_coverage: float
    severity_score: float
    matching_count: int

class InputSummary(BaseModel):
    valid_symptoms: List[str]
    invalid_symptoms: List[str]
    total_symptoms_provided: int
    valid_symptoms_count: int

class PredictionResponse(BaseModel):
    predictions: List[DiseasePrediction]
    recommended_doctors: List[DoctorResponse]
    input_summary: InputSummary

class DoctorBase(BaseModel):
    name: str
    specialization: str
    hospital: str
    rating: float

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    message: str

class MessageResponse(BaseModel):
    id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    doctorId: int
    userId: int
    message: str

class AppointmentUserInfo(BaseModel):
    id: int
    username: str
    full_name: str
    email: str

    class Config:
        from_attributes = True

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    user_id: int
    message: str
    status: str
    created_at: datetime
    doctor: DoctorResponse
    user: AppointmentUserInfo

    class Config:
        from_attributes = True

class SymptomBase(BaseModel):
    name: str
    description: Optional[str] = None

class SymptomCreate(SymptomBase):
    pass

class SymptomResponse(SymptomBase):
    id: int
    specialties: List[str] = []

    class Config:
        from_attributes = True

class SymptomSpecialtyBase(BaseModel):
    symptom_id: int
    specialty: str

class SymptomSpecialtyCreate(SymptomSpecialtyBase):
    pass

class SymptomSpecialtyResponse(SymptomSpecialtyBase):
    id: int

    class Config:
        from_attributes = True
