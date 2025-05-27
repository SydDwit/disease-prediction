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

        # Sample doctors data with specialties matching the new disease dataset
        doctors = [
            # Neurologists for vertigo, migraine, paralysis, etc.
            {
                "name": "Dr. Sarah Johnson",
                "specialization": "Neurologist",
                "hospital": "Central Medical Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Eric Foreman",
                "specialization": "Neurologist",
                "hospital": "Neuroscience Institute",
                "rating": 4.7
            },
            
            # ENT specialists for vertigo, common cold, etc.
            {
                "name": "Dr. Maya Patel",
                "specialization": "ENT",
                "hospital": "Ear Nose Throat Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Thomas Wright",
                "specialization": "ENT",
                "hospital": "Head & Neck Institute",
                "rating": 4.6
            },
            
            # Infectious Disease specialists for AIDS, hepatitis, etc.
            {
                "name": "Dr. Olivia Martinez",
                "specialization": "Infectious Disease",
                "hospital": "Infection Control Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Benjamin Lee",
                "specialization": "Infectious Disease",
                "hospital": "Tropical Medicine Institute",
                "rating": 4.7
            },
            
            # Gastroenterologists for hepatitis, GERD, etc.
            {
                "name": "Dr. William Chen",
                "specialization": "Gastroenterologist",
                "hospital": "Digestive Health Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Sophia Rodriguez",
                "specialization": "Gastroenterologist",
                "hospital": "GI Care Clinic",
                "rating": 4.7
            },
            
            # Hepatologists for hepatitis, jaundice, etc.
            {
                "name": "Dr. Daniel Kim",
                "specialization": "Hepatologist",
                "hospital": "Liver Disease Center",
                "rating": 4.8
            },
            
            # Dermatologists for acne, psoriasis, fungal infections
            {
                "name": "Dr. Emily Davis",
                "specialization": "Dermatologist",
                "hospital": "Skin & Care Clinic",
                "rating": 4.6
            },
            {
                "name": "Dr. Rachel Green",
                "specialization": "Dermatologist",
                "hospital": "Advanced Dermatology Center",
                "rating": 4.7
            },
            
            # Cardiologists for heart attack, hypertension
            {
                "name": "Dr. John Smith",
                "specialization": "Cardiologist",
                "hospital": "City Heart Hospital",
                "rating": 4.8
            },
            {
                "name": "Dr. Sam Wilson",
                "specialization": "Cardiologist",
                "hospital": "Heart Institute",
                "rating": 4.9
            },
            
            # Pulmonologists for tuberculosis, pneumonia, asthma
            {
                "name": "Dr. Michael Brown",
                "specialization": "Pulmonologist",
                "hospital": "Respiratory Care Center",
                "rating": 4.7
            },
            {
                "name": "Dr. Aisha Khan",
                "specialization": "Pulmonologist",
                "hospital": "Lung Health Institute",
                "rating": 4.8
            },
            
            # Endocrinologists for diabetes, thyroid disorders
            {
                "name": "Dr. Jennifer Lopez",
                "specialization": "Endocrinologist",
                "hospital": "Diabetes & Hormone Center",
                "rating": 4.7
            },
            {
                "name": "Dr. David Park",
                "specialization": "Endocrinologist",
                "hospital": "Metabolic Health Institute",
                "rating": 4.6
            },
            
            # Rheumatologists and Orthopedists for arthritis
            {
                "name": "Dr. Robert Taylor",
                "specialization": "Rheumatologist",
                "hospital": "Arthritis Treatment Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Lisa Wang",
                "specialization": "Orthopedist",
                "hospital": "Joint & Bone Center",
                "rating": 4.7
            },
            
            # Allergists for allergies and drug reactions
            {
                "name": "Dr. James Wilson",
                "specialization": "Allergist",
                "hospital": "Allergy & Asthma Center",
                "rating": 4.8
            },
            
            # Immunologists
            {
                "name": "Dr. Allison Cameron",
                "specialization": "Immunologist",
                "hospital": "Medical Research Center",
                "rating": 4.8
            },
            
            # Urologists for UTIs
            {
                "name": "Dr. Christopher Miller",
                "specialization": "Urologist",
                "hospital": "Urology Specialists",
                "rating": 4.7
            },
            
            # Vascular surgeons for varicose veins
            {
                "name": "Dr. Natalie Adams",
                "specialization": "Vascular Surgeon",
                "hospital": "Vascular Health Center",
                "rating": 4.6
            },
            
            # General practitioners for common conditions
            {
                "name": "Dr. Robert Wilson",
                "specialization": "General Practitioner",
                "hospital": "Community Health Center",
                "rating": 4.5
            },
            {
                "name": "Dr. Maria Garcia",
                "specialization": "General Practitioner",
                "hospital": "Family Health Clinic",
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