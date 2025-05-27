from database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as connection:
        try:
            # First add the column as nullable
            connection.execute(text("""
                ALTER TABLE appointments 
                ADD COLUMN user_id INT NULL;
            """))
            
            # Add the foreign key constraint
            connection.execute(text("""
                ALTER TABLE appointments
                ADD CONSTRAINT fk_user
                FOREIGN KEY (user_id) 
                REFERENCES users(id)
                ON DELETE CASCADE;
            """))
            
            # Get the first user's ID to use as default
            result = connection.execute(text("SELECT id FROM users LIMIT 1"))
            default_user_id = result.scalar()
            
            if default_user_id:
                # Update existing records with the default user
                connection.execute(text(f"""
                    UPDATE appointments 
                    SET user_id = {default_user_id} 
                    WHERE user_id IS NULL;
                """))
                
                # Now make the column NOT NULL
                connection.execute(text("""
                    ALTER TABLE appointments 
                    MODIFY COLUMN user_id INT NOT NULL;
                """))
            
            connection.commit()
            print("Migration successful: Added user_id column to appointments table")
        except Exception as e:
            print(f"Migration failed: {str(e)}")
            connection.rollback()

if __name__ == "__main__":
    migrate() 