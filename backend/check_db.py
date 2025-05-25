from database import SessionLocal
from models import User, Doctor

def check_database():
    db = SessionLocal()
    try:
        # Check users
        users = db.query(User).all()
        print("\nUsers in database:")
        print("-----------------")
        for user in users:
            print(f"Username: {user.username}, Email: {user.email}, Is Admin: {user.is_admin}")
        print(f"Total users: {len(users)}")

        # Check doctors
        doctors = db.query(Doctor).all()
        print("\nDoctors in database:")
        print("------------------")
        for doctor in doctors:
            print(f"Name: {doctor.name}, Specialization: {doctor.specialization}, Hospital: {doctor.hospital}")
        print(f"Total doctors: {len(doctors)}")

    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database() 