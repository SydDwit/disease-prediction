from database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as connection:
        try:
            # First add the column as nullable
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN full_name VARCHAR(255) NULL;
            """))
            
            # Update existing records with username as default
            connection.execute(text("""
                UPDATE users 
                SET full_name = username 
                WHERE full_name IS NULL;
            """))
            
            # Make the column NOT NULL
            connection.execute(text("""
                ALTER TABLE users 
                MODIFY COLUMN full_name VARCHAR(255) NOT NULL;
            """))
            
            connection.commit()
            print("Migration successful: Added full_name column to users table")
        except Exception as e:
            print(f"Migration failed: {str(e)}")
            connection.rollback()

if __name__ == "__main__":
    migrate() 