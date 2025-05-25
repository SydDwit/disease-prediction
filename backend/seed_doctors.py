from database import SessionLocal
from models import Doctor

def seed_doctors():
    db = SessionLocal()
    try:
        # Check if we already have doctors
        existing_doctors = db.query(Doctor).count()
        if existing_doctors > 0:
            print("Doctors already exist in the database!")
            return

        # Sample doctors data
        doctors = [
            {
                "name": "Dr. John Smith",
                "specialization": "Cardiologist",
                "hospital": "City Heart Hospital",
                "rating": 4.8
            },
            {
                "name": "Dr. Sarah Johnson",
                "specialization": "Neurologist",
                "hospital": "Central Medical Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Michael Brown",
                "specialization": "Pulmonologist",
                "hospital": "Respiratory Care Center",
                "rating": 4.7
            },
            {
                "name": "Dr. Emily Davis",
                "specialization": "Dermatologist",
                "hospital": "Skin & Care Clinic",
                "rating": 4.6
            },
            {
                "name": "Dr. Robert Wilson",
                "specialization": "General Physician",
                "hospital": "Community Health Center",
                "rating": 4.5
            },
            # Additional doctors with diverse specializations
            {
                "name": "Dr. James Wilson",
                "specialization": "Internal Medicine",
                "hospital": "Princeton General Hospital",
                "rating": 4.9
            },
            {
                "name": "Dr. Lisa Cuddy",
                "specialization": "Emergency Medicine",
                "hospital": "City Emergency Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Eric Foreman",
                "specialization": "Neurologist",
                "hospital": "Neuroscience Institute",
                "rating": 4.7
            },
            {
                "name": "Dr. Allison Cameron",
                "specialization": "Immunologist",
                "hospital": "Medical Research Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Gregory House",
                "specialization": "Diagnostic Medicine",
                "hospital": "Princeton Teaching Hospital",
                "rating": 4.9
            },
            {
                "name": "Dr. Robert Chase",
                "specialization": "Surgeon",
                "hospital": "Central Surgical Hospital",
                "rating": 4.7
            },
            {
                "name": "Dr. Lawrence Kutner",
                "specialization": "Sports Medicine",
                "hospital": "Sports Rehabilitation Center",
                "rating": 4.6
            },
            {
                "name": "Dr. Chris Taub",
                "specialization": "Plastic Surgeon",
                "hospital": "Aesthetic Medical Center",
                "rating": 4.5
            },
            {
                "name": "Dr. Remy Hadley",
                "specialization": "Internal Medicine",
                "hospital": "Community Health Hospital",
                "rating": 4.7
            },
            {
                "name": "Dr. Jessica Adams",
                "specialization": "Emergency Medicine",
                "hospital": "Urgent Care Center",
                "rating": 4.6
            },
            {
                "name": "Dr. Chi Park",
                "specialization": "Neurosurgeon",
                "hospital": "Brain and Spine Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Martha Masters",
                "specialization": "Pediatrician",
                "hospital": "Children's Medical Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Sam Wilson",
                "specialization": "Cardiologist",
                "hospital": "Heart Institute",
                "rating": 4.8
            },
            {
                "name": "Dr. Peter Lewis",
                "specialization": "Oncologist",
                "hospital": "Cancer Treatment Center",
                "rating": 4.7
            },
            {
                "name": "Dr. Rachel Green",
                "specialization": "Dermatologist",
                "hospital": "Skin Care Clinic",
                "rating": 4.6
            }
        ]

        # Add doctors to database
        for doctor_data in doctors:
            doctor = Doctor(**doctor_data)
            db.add(doctor)
        
        db.commit()
        print("Successfully added sample doctors!")

    except Exception as e:
        print(f"Error seeding doctors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_doctors() 