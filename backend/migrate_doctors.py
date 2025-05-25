from database import engine
from sqlalchemy import text

def migrate():
    try:
        # Disable foreign key checks, drop and recreate the table
        with engine.connect() as connection:
            # Disable foreign key checks
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
            
            # Drop and recreate the table
            connection.execute(text("DROP TABLE IF EXISTS doctors;"))
            connection.execute(text("""
                CREATE TABLE doctors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    specialization VARCHAR(255) NOT NULL,
                    hospital VARCHAR(255) NOT NULL,
                    rating FLOAT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Re-enable foreign key checks
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
            
            connection.commit()
            print("Successfully recreated doctors table!")
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate() 