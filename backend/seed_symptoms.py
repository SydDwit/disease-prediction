from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import SQLALCHEMY_DATABASE_URL
from models import Base, Symptom, symptom_specialty
from disease_specialties import DISEASE_TO_SPECIALTY, get_relevant_specialties

def seed_symptoms():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.execute(text("DELETE FROM symptom_specialty"))
        db.execute(text("DELETE FROM symptoms"))
        db.commit()
        
        print("Successfully cleared existing symptom data")
        
        # Keep track of added symptoms to avoid duplicates
        added_symptoms = set()
        
        # Add diseases as symptoms with their specialty mappings
        for disease, specialties in DISEASE_TO_SPECIALTY.items():
            if disease == 'default' or disease in added_symptoms:  # Skip defaults and duplicates
                continue
                
            # Create the symptom
            symptom = Symptom(
                name=disease,
                description=f"Condition requiring consultation with: {', '.join(specialties)}"
            )
            db.add(symptom)
            db.flush()  # Get the ID without committing
            
            # Add specialty mappings
            for specialty in specialties:
                db.execute(
                    symptom_specialty.insert().values(
                        symptom_id=symptom.id,
                        specialty=specialty
                    )
                )
            
            added_symptoms.add(disease)
        
        # Add keyword-based symptoms
        keywords_to_specialties = {
            'brain disorder': ['Neurologist', 'Neurosurgeon'],
            'nerve pain': ['Neurologist'],
            'spinal pain': ['Neurologist', 'Neurosurgeon'],
            'seizures': ['Neurologist'],
            'cognitive decline': ['Neurologist', 'Psychiatrist'],
            'mental health issues': ['Psychiatrist', 'Psychologist'],
            'behavioral problems': ['Psychiatrist', 'Psychologist'],
            'mood disorder': ['Psychiatrist'],
            'chronic cough': ['Pulmonologist', 'Internal Medicine'],
            'respiratory problems': ['Pulmonologist'],
            'breathing issues': ['Pulmonologist'],  # Changed from 'breathing difficulty' to avoid duplicate
            'airway obstruction': ['Pulmonologist', 'ENT'],
            'toxic exposure': ['Emergency Medicine', 'Toxicologist'],
            'salivary gland problems': ['ENT', 'Oral & Maxillofacial Surgeon'],
            'oral cavity issues': ['ENT', 'Oral & Maxillofacial Surgeon'],
            'chronic illness': ['Internal Medicine', 'Family Medicine'],
            'urinary problems': ['Urologist', 'Nephrologist'],
            'kidney problems': ['Urologist', 'Nephrologist'],
            'prostate issues': ['Urologist', 'Oncologist']
        }
        
        for symptom_name, specialties in keywords_to_specialties.items():
            if symptom_name in added_symptoms:  # Skip if already added
                continue
                
            symptom = Symptom(
                name=symptom_name,
                description=f"Condition requiring consultation with: {', '.join(specialties)}"
            )
            db.add(symptom)
            db.flush()
            
            for specialty in specialties:
                db.execute(
                    symptom_specialty.insert().values(
                        symptom_id=symptom.id,
                        specialty=specialty
                    )
                )
            
            added_symptoms.add(symptom_name)
        
        db.commit()
        print(f"Successfully added {len(added_symptoms)} symptoms")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_symptoms() 