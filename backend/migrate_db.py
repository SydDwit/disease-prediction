from database import engine
from sqlalchemy import text

# SQL to add is_admin column
sql = text("""
ALTER TABLE users
ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE;
""")

if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            connection.execute(sql)
            connection.commit()
            print("Successfully added is_admin column to users table!")
    except Exception as e:
        print(f"Error during migration: {e}") 