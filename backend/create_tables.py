from database import engine
import models

def create_tables():
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Successfully created all tables!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables() 