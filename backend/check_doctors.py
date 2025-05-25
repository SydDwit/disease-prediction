from database import SessionLocal
from models import Doctor

def check_doctors():
    db = SessionLocal()
    try:
        doctors = db.query(Doctor).all()
        print("\nAvailable doctors:")
        for doctor in doctors:
            print(f"ID: {doctor.id}, Name: {doctor.name}, Specialization: {doctor.specialization}, Hospital: {doctor.hospital}")
    finally:
        db.close()

if __name__ == "__main__":
    check_doctors() 