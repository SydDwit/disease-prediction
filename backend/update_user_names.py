from database import engine, SessionLocal
from sqlalchemy import text
from models import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("\nCurrent Users:")
        print("-" * 50)
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Full Name: {user.full_name}")
        print("-" * 50)
    finally:
        db.close()

def update_user_full_name(user_id, new_full_name):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.full_name = new_full_name
            db.commit()
            print(f"\nSuccessfully updated user {user.username}'s full name to: {new_full_name}")
        else:
            print(f"\nNo user found with ID {user_id}")
    finally:
        db.close()

def main():
    while True:
        print("\nUpdate User Full Names")
        print("1. List all users")
        print("2. Update a user's full name")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            list_users()
        elif choice == "2":
            try:
                user_id = int(input("Enter user ID: "))
                new_full_name = input("Enter new full name: ")
                update_user_full_name(user_id, new_full_name)
            except ValueError:
                print("Please enter a valid user ID (number)")
        elif choice == "3":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 