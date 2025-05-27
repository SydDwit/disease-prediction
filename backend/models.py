from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Boolean, ForeignKey, Text, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Association table for symptoms and specialties
symptom_specialty = Table(
    'symptom_specialty',
    Base.metadata,
    Column('symptom_id', Integer, ForeignKey('symptoms.id')),
    Column('specialty', String(100))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(Enum('male', 'female', 'other'), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)
    hospital = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Doctor {self.name}>"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), server_default='pending', nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Symptom(Base):
    __tablename__ = "symptoms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True)
    description = Column(Text, nullable=True)
    specialties = relationship(
        "Doctor",
        secondary="symptom_specialty",
        primaryjoin="Symptom.id == symptom_specialty.c.symptom_id",
        secondaryjoin="Doctor.specialization == symptom_specialty.c.specialty",
        viewonly=True
    )
