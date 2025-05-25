from database import SessionLocal
from models import User

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # Create admin user with simple credentials
            admin = User(
                username="admin",
                email="admin@example.com",
                password="admin123",  # In a real app, this should be hashed
                gender="other",
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin() 