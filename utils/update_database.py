"""
This script updates the database with the new disease and symptom mappings.
Run this after training the model with the new dataset.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add the backend directory to the path so we can import from it
backend_path = os.path.normpath('backend')
sys.path.append(backend_path)

try:
    from backend.database import SQLALCHEMY_DATABASE_URL, Base
    from backend.seed_doctors import seed_doctors
    from backend.seed_symptoms import seed_symptoms
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

def update_database():
    """Update the database with new disease and symptom mappings"""
    
    print("Starting database update...")
    
    # Create engine and session
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False
    
    try:
        # Step 1: Remove existing doctors and symptoms
        print("Removing existing doctors and symptoms...")
        db.execute(text("DELETE FROM symptom_specialty"))
        db.execute(text("DELETE FROM symptoms"))
        db.execute(text("DELETE FROM doctors"))
        db.commit()
        
        # Step 2: Seed new doctors
        print("Adding new doctors...")
        seed_doctors()
        
        # Step 3: Seed new symptoms
        print("Adding new symptoms...")
        seed_symptoms()
        
        print("Database update completed successfully!")
        return True
        
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        db.rollback()
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    update_database() 