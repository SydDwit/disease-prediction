from database import SessionLocal
from models import User

def check_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.is_admin == True).first()
        if admin:
            print("\nAdmin user found:")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Is Admin: {admin.is_admin}")
        else:
            print("\nNo admin user found in the database")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin() 