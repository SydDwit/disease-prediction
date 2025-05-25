from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import SQLALCHEMY_DATABASE_URL
from models import Base, Doctor, User

def reset_database():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("Successfully dropped all tables")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Successfully created all tables with updated schema")
        
        # Create a session to add sample data
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Add sample doctors with various specialties
        sample_doctors = [
            # Neurologists
            Doctor(name="Dr. Sarah Chen", specialization="Neurologist", hospital="Neurology Institute", rating=4.9),
            Doctor(name="Dr. James Wilson", specialization="Neurologist", hospital="Brain & Spine Center", rating=4.8),
            
            # Cardiologists
            Doctor(name="Dr. Michael Lee", specialization="Cardiologist", hospital="Heart Center", rating=4.9),
            Doctor(name="Dr. Emily Brown", specialization="Cardiologist", hospital="Cardiovascular Institute", rating=4.7),
            
            # Gastroenterologists
            Doctor(name="Dr. David Martinez", specialization="Gastroenterologist", hospital="Digestive Health Center", rating=4.8),
            Doctor(name="Dr. Lisa Wong", specialization="Gastroenterologist", hospital="GI Specialists", rating=4.6),
            
            # Endocrinologists
            Doctor(name="Dr. Robert Taylor", specialization="Endocrinologist", hospital="Diabetes & Hormone Center", rating=4.8),
            Doctor(name="Dr. Patricia Anderson", specialization="Endocrinologist", hospital="Endocrine Institute", rating=4.7),
            
            # Pulmonologists
            Doctor(name="Dr. Thomas Johnson", specialization="Pulmonologist", hospital="Respiratory Care Center", rating=4.8),
            Doctor(name="Dr. Maria Garcia", specialization="Pulmonologist", hospital="Lung Health Institute", rating=4.7),
            
            # Oncologists
            Doctor(name="Dr. William Clark", specialization="Oncologist", hospital="Cancer Treatment Center", rating=4.9),
            Doctor(name="Dr. Jennifer Lewis", specialization="Oncologist", hospital="Comprehensive Cancer Center", rating=4.8),
            
            # Emergency Medicine
            Doctor(name="Dr. Peter Safar", specialization="Emergency Medicine", hospital="Emergency Care Center", rating=4.9),
            Doctor(name="Dr. Susan White", specialization="Emergency Medicine", hospital="Acute Care Hospital", rating=4.7),
            
            # Infectious Disease
            Doctor(name="Dr. Richard Brown", specialization="Infectious Disease", hospital="Infection Control Center", rating=4.8),
            Doctor(name="Dr. Anna Martinez", specialization="Infectious Disease", hospital="Tropical Disease Institute", rating=4.7),
            
            # Rheumatologists
            Doctor(name="Dr. Amanda Cooper", specialization="Rheumatologist", hospital="Arthritis & Rheumatism Center", rating=4.7),
            Doctor(name="Dr. Steven Park", specialization="Rheumatologist", hospital="Joint & Bone Institute", rating=4.8),
            
            # Dermatologists
            Doctor(name="Dr. Rachel Green", specialization="Dermatologist", hospital="Skin Care Institute", rating=4.8),
            Doctor(name="Dr. Mark Thompson", specialization="Dermatologist", hospital="Dermatology Center", rating=4.7),
            
            # Psychiatrists
            Doctor(name="Dr. Daniel Kim", specialization="Psychiatrist", hospital="Mental Health Center", rating=4.8),
            Doctor(name="Dr. Laura Chen", specialization="Psychiatrist", hospital="Behavioral Health Institute", rating=4.7),
            
            # Ophthalmologists
            Doctor(name="Dr. John Murphy", specialization="Ophthalmologist", hospital="Eye Institute", rating=4.8),
            Doctor(name="Dr. Sarah Palmer", specialization="Ophthalmologist", hospital="Vision Care Center", rating=4.7),
            
            # ENT (Otolaryngologists)
            Doctor(name="Dr. Michael Chang", specialization="ENT", hospital="Ear Nose Throat Center", rating=4.8),
            Doctor(name="Dr. Rebecca Wilson", specialization="ENT", hospital="Head & Neck Institute", rating=4.7),
            
            # Orthopedists
            Doctor(name="Dr. Christopher Lee", specialization="Orthopedist", hospital="Orthopedic Center", rating=4.8),
            Doctor(name="Dr. Jessica Taylor", specialization="Orthopedist", hospital="Sports Medicine Institute", rating=4.7),
            
            # Urologists
            Doctor(name="Dr. Robert Chen", specialization="Urologist", hospital="Urology Center", rating=4.8),
            Doctor(name="Dr. Michelle Park", specialization="Urologist", hospital="Kidney Institute", rating=4.7),
            
            # Allergists/Immunologists
            Doctor(name="Dr. David Cohen", specialization="Allergist", hospital="Allergy & Asthma Center", rating=4.8),
            Doctor(name="Dr. Karen Wu", specialization="Immunologist", hospital="Immunology Institute", rating=4.7),
            
            # Nephrologists
            Doctor(name="Dr. James Lee", specialization="Nephrologist", hospital="Kidney Disease Center", rating=4.8),
            Doctor(name="Dr. Linda Martinez", specialization="Nephrologist", hospital="Renal Institute", rating=4.7),
            
            # Hematologists
            Doctor(name="Dr. Thomas Wilson", specialization="Hematologist", hospital="Blood Disorders Center", rating=4.8),
            Doctor(name="Dr. Nancy Rodriguez", specialization="Hematologist", hospital="Hematology Institute", rating=4.7),
            
            # Geriatricians
            Doctor(name="Dr. William Brown", specialization="Geriatrician", hospital="Senior Care Center", rating=4.8),
            Doctor(name="Dr. Elizabeth Chen", specialization="Geriatrician", hospital="Elder Care Institute", rating=4.7),
            
            # Pediatricians
            Doctor(name="Dr. Robert Davis", specialization="Pediatrician", hospital="Children's Hospital", rating=4.8),
            Doctor(name="Dr. Mary Johnson", specialization="Pediatrician", hospital="Pediatric Care Center", rating=4.7),
            
            # Family Medicine
            Doctor(name="Dr. John Smith", specialization="Family Medicine", hospital="Family Care Center", rating=4.8),
            Doctor(name="Dr. Lisa Anderson", specialization="Family Medicine", hospital="Community Health Center", rating=4.7),
            
            # Dentists
            Doctor(name="Dr. Michael White", specialization="Dentist", hospital="Dental Care Center", rating=4.8),
            Doctor(name="Dr. Jennifer Brown", specialization="Dentist", hospital="Oral Health Institute", rating=4.7),

            # Adding 15 more specialized doctors
            # Neurosurgeons
            Doctor(name="Dr. Andrew Kim", specialization="Neurosurgeon", hospital="Brain Surgery Center", rating=4.9),
            Doctor(name="Dr. Victoria Chang", specialization="Neurosurgeon", hospital="Spine Surgery Institute", rating=4.8),

            # Plastic Surgeons
            Doctor(name="Dr. Benjamin Moore", specialization="Plastic Surgeon", hospital="Reconstructive Surgery Center", rating=4.8),

            # Thoracic Surgeon
            Doctor(name="Dr. Alexander Wright", specialization="Thoracic Surgeon", hospital="Chest Surgery Institute", rating=4.9),

            # Vascular Surgeon
            Doctor(name="Dr. Sophia Rodriguez", specialization="Vascular Surgeon", hospital="Vascular Disease Center", rating=4.8),

            # Pain Management
            Doctor(name="Dr. Nathan Phillips", specialization="Pain Management", hospital="Pain Treatment Center", rating=4.7),

            # Sports Medicine
            Doctor(name="Dr. Oliver Martinez", specialization="Sports Medicine", hospital="Sports Injury Clinic", rating=4.8),

            # Colorectal Surgeon
            Doctor(name="Dr. Isabella Kim", specialization="Colorectal Surgeon", hospital="Colorectal Surgery Center", rating=4.8),

            # Hepatologist
            Doctor(name="Dr. Lucas Thompson", specialization="Hepatologist", hospital="Liver Disease Institute", rating=4.9),

            # Movement Disorder Specialist
            Doctor(name="Dr. Emma Watson", specialization="Movement Disorder Specialist", hospital="Movement Disorders Center", rating=4.8),

            # Sleep Medicine
            Doctor(name="Dr. Adrian Chen", specialization="Sleep Medicine", hospital="Sleep Disorders Center", rating=4.7),

            # Reproductive Endocrinologist
            Doctor(name="Dr. Sophia Lee", specialization="Reproductive Endocrinologist", hospital="Fertility Center", rating=4.8),

            # Addiction Medicine
            Doctor(name="Dr. Marcus Johnson", specialization="Addiction Medicine", hospital="Addiction Treatment Center", rating=4.7),

            # Pediatric Surgeon
            Doctor(name="Dr. Caroline Davis", specialization="Pediatric Surgeon", hospital="Children's Surgical Center", rating=4.9),

            # Radiation Oncologist
            Doctor(name="Dr. Derek Wilson", specialization="Radiation Oncologist", hospital="Radiation Therapy Center", rating=4.8)
        ]
        
        # Add sample admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password="admin123",  # In a real app, this should be hashed
            gender="other",
            is_admin=True
        )
        
        # Add the sample data
        db.add(admin_user)
        for doctor in sample_doctors:
            db.add(doctor)
            
        # Commit the changes
        db.commit()
        print("Successfully added sample data")
        
        # Close the session
        db.close()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    reset_database() 