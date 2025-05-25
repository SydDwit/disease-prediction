from database import SessionLocal
from models import Doctor

def seed_more_doctors():
    db = SessionLocal()
    try:
        # Additional doctors with diverse specializations
        doctors = [
            # Specialists for Neurological conditions
            {
                "name": "Dr. Oliver Sacks",
                "specialization": "Neurologist",
                "hospital": "Brain & Nerve Institute",
                "rating": 4.9
            },
            {
                "name": "Dr. Benjamin Carson",
                "specialization": "Neurosurgeon",
                "hospital": "Advanced Neurosurgery Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Maya Rodriguez",
                "specialization": "Movement Disorder Specialist",
                "hospital": "Movement Disorders Clinic",
                "rating": 4.8
            },
            
            # Specialists for Cardiovascular conditions
            {
                "name": "Dr. Denton Cooley",
                "specialization": "Cardiologist",
                "hospital": "Heart Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Elena Martinez",
                "specialization": "Electrophysiologist",
                "hospital": "Cardiac Rhythm Center",
                "rating": 4.8
            },
            {
                "name": "Dr. William Harvey",
                "specialization": "Vascular Surgeon",
                "hospital": "Vascular Institute",
                "rating": 4.7
            },
            
            # Specialists for Respiratory conditions
            {
                "name": "Dr. Sarah Chen",
                "specialization": "Pulmonologist",
                "hospital": "Respiratory Care Institute",
                "rating": 4.8
            },
            {
                "name": "Dr. Thomas Young",
                "specialization": "Critical Care",
                "hospital": "Intensive Care Unit",
                "rating": 4.9
            },
            {
                "name": "Dr. Maria Santos",
                "specialization": "Sleep Medicine",
                "hospital": "Sleep Disorders Center",
                "rating": 4.7
            },
            
            # Specialists for Gastrointestinal conditions
            {
                "name": "Dr. Michael Kirsch",
                "specialization": "Gastroenterologist",
                "hospital": "Digestive Health Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Lisa Kumar",
                "specialization": "Hepatologist",
                "hospital": "Liver Disease Institute",
                "rating": 4.7
            },
            {
                "name": "Dr. David Cohen",
                "specialization": "Colorectal Surgeon",
                "hospital": "Colorectal Surgery Center",
                "rating": 4.8
            },
            
            # Specialists for Endocrine conditions
            {
                "name": "Dr. Robert Williams",
                "specialization": "Endocrinologist",
                "hospital": "Endocrine & Diabetes Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Patricia Lee",
                "specialization": "Reproductive Endocrinologist",
                "hospital": "Fertility Center",
                "rating": 4.8
            },
            
            # Specialists for Infectious Diseases
            {
                "name": "Dr. Anthony Fauci",
                "specialization": "Infectious Disease",
                "hospital": "Infectious Disease Institute",
                "rating": 4.9
            },
            {
                "name": "Dr. Emily White",
                "specialization": "Travel Medicine",
                "hospital": "Travel Health Clinic",
                "rating": 4.7
            },
            
            # Specialists for Rheumatological conditions
            {
                "name": "Dr. Daniel Wallace",
                "specialization": "Rheumatologist",
                "hospital": "Arthritis & Rheumatism Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Susan Black",
                "specialization": "Immunologist",
                "hospital": "Immunology Center",
                "rating": 4.7
            },
            
            # Specialists for Renal/Urological conditions
            {
                "name": "Dr. Richard Fine",
                "specialization": "Nephrologist",
                "hospital": "Kidney Disease Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Jennifer Urology",
                "specialization": "Urologist",
                "hospital": "Urology Institute",
                "rating": 4.7
            },
            
            # Specialists for Hematological conditions
            {
                "name": "Dr. Ernest Beutler",
                "specialization": "Hematologist",
                "hospital": "Blood Disorders Center",
                "rating": 4.8
            },
            {
                "name": "Dr. James Holland",
                "specialization": "Oncologist",
                "hospital": "Cancer Treatment Institute",
                "rating": 4.9
            },
            
            # Mental Health specialists
            {
                "name": "Dr. Aaron Beck",
                "specialization": "Psychiatrist",
                "hospital": "Mental Health Institute",
                "rating": 4.8
            },
            {
                "name": "Dr. Kay Redfield",
                "specialization": "Psychologist",
                "hospital": "Behavioral Health Center",
                "rating": 4.7
            },
            
            # Additional Primary Care
            {
                "name": "Dr. Barbara Starfield",
                "specialization": "Internal Medicine",
                "hospital": "Primary Care Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Ian McWhinney",
                "specialization": "Family Medicine",
                "hospital": "Family Health Center",
                "rating": 4.7
            },
            
            # Emergency and Critical Care
            {
                "name": "Dr. Peter Safar",
                "specialization": "Emergency Medicine",
                "hospital": "Emergency Care Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Max Harry Weil",
                "specialization": "Critical Care",
                "hospital": "Critical Care Unit",
                "rating": 4.8
            },
            
            # Specialists for ENT conditions
            {
                "name": "Dr. Howard House",
                "specialization": "ENT",
                "hospital": "Ear Nose Throat Institute",
                "rating": 4.8
            },
            {
                "name": "Dr. William House",
                "specialization": "Otologist",
                "hospital": "Hearing & Balance Center",
                "rating": 4.7
            },
            
            # Specialists for Eye conditions
            {
                "name": "Dr. Charles Kelman",
                "specialization": "Ophthalmologist",
                "hospital": "Eye Institute",
                "rating": 4.8
            },
            {
                "name": "Dr. Stephen Trokel",
                "specialization": "Retina Specialist",
                "hospital": "Retina Care Center",
                "rating": 4.9
            },
            
            # Specialists for Skin conditions
            {
                "name": "Dr. Albert Kligman",
                "specialization": "Dermatologist",
                "hospital": "Skin & Dermatology Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Marion Sulzberger",
                "specialization": "Allergist",
                "hospital": "Allergy & Immunology Center",
                "rating": 4.7
            },
            
            # Additional Surgical specialists
            {
                "name": "Dr. Michael DeBakey",
                "specialization": "Thoracic Surgeon",
                "hospital": "Cardiothoracic Surgery Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Joseph Murray",
                "specialization": "Transplant Surgeon",
                "hospital": "Transplant Institute",
                "rating": 4.8
            },
            {
                "name": "Dr. Leonard Miller",
                "specialization": "Plastic Surgeon",
                "hospital": "Plastic & Reconstructive Surgery Center",
                "rating": 4.7
            },
            
            # Additional specialists
            {
                "name": "Dr. Virginia Apgar",
                "specialization": "Pediatrician",
                "hospital": "Children's Medical Center",
                "rating": 4.9
            },
            {
                "name": "Dr. Robert Butler",
                "specialization": "Geriatrician",
                "hospital": "Senior Care Center",
                "rating": 4.8
            },
            {
                "name": "Dr. Scott Haldeman",
                "specialization": "Physical Medicine",
                "hospital": "Rehabilitation Center",
                "rating": 4.7
            }
        ]

        # Add doctors to database
        for doctor_data in doctors:
            doctor = Doctor(**doctor_data)
            db.add(doctor)
        
        db.commit()
        print("Successfully added additional doctors!")

    except Exception as e:
        print(f"Error seeding additional doctors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_more_doctors() 