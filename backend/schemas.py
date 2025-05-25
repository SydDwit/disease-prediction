from pydantic import BaseModel, EmailStr, constr, Field
from datetime import datetime
from typing import Optional, Literal, List

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

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

class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    recommended_doctors: List[DoctorResponse]

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
    message: str

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    message: str
    status: str
    created_at: datetime

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
