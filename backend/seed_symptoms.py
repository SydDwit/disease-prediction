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
        
        # Add symptoms from the new dataset with their specialty mappings
        new_dataset_symptoms = {
            # Skin-related symptoms
            'itching': ['Dermatologist', 'Allergist'],
            'skin_rash': ['Dermatologist', 'Allergist'],
            'nodal_skin_eruptions': ['Dermatologist'],
            'dischromic_patches': ['Dermatologist'],
            'skin_peeling': ['Dermatologist'],
            'pus_filled_pimples': ['Dermatologist'],
            'blackheads': ['Dermatologist'],
            'scurring': ['Dermatologist'],
            'silver_like_dusting': ['Dermatologist'],
            'small_dents_in_nails': ['Dermatologist'],
            'inflammatory_nails': ['Dermatologist'],
            'blister': ['Dermatologist'],
            'red_sore_around_nose': ['Dermatologist', 'ENT'],
            'yellow_crust_ooze': ['Dermatologist'],
            'red_spots_over_body': ['Dermatologist', 'Allergist', 'Infectious Disease'],
            
            # Respiratory symptoms
            'continuous_sneezing': ['ENT', 'Allergist'],
            'breathlessness': ['Pulmonologist', 'Cardiologist'],
            'phlegm': ['Pulmonologist', 'ENT'],
            'throat_irritation': ['ENT'],
            'runny_nose': ['ENT', 'Allergist'],
            'congestion': ['ENT', 'Allergist'],
            'chest_pain': ['Cardiologist', 'Pulmonologist'],
            'cough': ['Pulmonologist', 'ENT'],
            'rusty_sputum': ['Pulmonologist'],
            'mucoid_sputum': ['Pulmonologist'],
            'blood_in_sputum': ['Pulmonologist'],
            
            # General symptoms
            'shivering': ['Infectious Disease', 'General Practitioner'],
            'chills': ['Infectious Disease', 'General Practitioner'],
            'fatigue': ['General Practitioner', 'Internal Medicine'],
            'lethargy': ['General Practitioner', 'Internal Medicine'],
            'high_fever': ['Infectious Disease', 'General Practitioner'],
            'mild_fever': ['General Practitioner', 'Infectious Disease'],
            'sweating': ['General Practitioner', 'Endocrinologist'],
            'dehydration': ['General Practitioner', 'Internal Medicine'],
            'headache': ['Neurologist', 'General Practitioner'],
            'dizziness': ['Neurologist', 'ENT'],
            'weakness_in_limbs': ['Neurologist', 'Orthopedist'],
            'malaise': ['General Practitioner', 'Internal Medicine'],
            
            # Pain-related symptoms
            'joint_pain': ['Rheumatologist', 'Orthopedist'],
            'stomach_pain': ['Gastroenterologist'],
            'back_pain': ['Orthopedist', 'Neurologist'],
            'neck_pain': ['Orthopedist', 'Neurologist'],
            'knee_pain': ['Orthopedist'],
            'hip_joint_pain': ['Orthopedist'],
            'muscle_pain': ['Orthopedist', 'Rheumatologist'],
            'belly_pain': ['Gastroenterologist'],
            'pain_behind_the_eyes': ['Ophthalmologist', 'Neurologist'],
            'pain_during_bowel_movements': ['Gastroenterologist', 'Colorectal Surgeon'],
            'pain_in_anal_region': ['Gastroenterologist', 'Colorectal Surgeon'],
            'abdominal_pain': ['Gastroenterologist'],
            
            # Gastrointestinal symptoms
            'acidity': ['Gastroenterologist'],
            'ulcers_on_tongue': ['ENT', 'Gastroenterologist'],
            'vomiting': ['Gastroenterologist', 'General Practitioner'],
            'indigestion': ['Gastroenterologist'],
            'loss_of_appetite': ['Gastroenterologist', 'Internal Medicine'],
            'constipation': ['Gastroenterologist'],
            'diarrhoea': ['Gastroenterologist', 'Infectious Disease'],
            'yellowish_skin': ['Hepatologist', 'Gastroenterologist'],
            'dark_urine': ['Urologist', 'Hepatologist'],
            'yellow_urine': ['Urologist', 'Hepatologist'],
            'yellowing_of_eyes': ['Hepatologist', 'Ophthalmologist'],
            'nausea': ['Gastroenterologist', 'General Practitioner'],
            'stomach_bleeding': ['Gastroenterologist', 'Emergency Medicine'],
            'distention_of_abdomen': ['Gastroenterologist'],
            'irritation_in_anus': ['Gastroenterologist', 'Colorectal Surgeon'],
            'swelling_of_stomach': ['Gastroenterologist'],
            'bloody_stool': ['Gastroenterologist', 'Colorectal Surgeon'],
            'irritable_bowel_syndrome': ['Gastroenterologist'],
            'passage_of_gases': ['Gastroenterologist'],
            'internal_itching': ['Gastroenterologist', 'Dermatologist'],
            
            # Urinary symptoms
            'burning_micturition': ['Urologist'],
            'spotting_urination': ['Urologist'],
            'bladder_discomfort': ['Urologist'],
            'foul_smell_of_urine': ['Urologist'],
            'continuous_feel_of_urine': ['Urologist'],
            'polyuria': ['Urologist', 'Endocrinologist'],
            
            # Neurological symptoms
            'altered_sensorium': ['Neurologist'],
            'lack_of_concentration': ['Neurologist', 'Psychiatrist'],
            'unsteadiness': ['Neurologist'],
            'spinning_movements': ['Neurologist', 'ENT'],
            'loss_of_balance': ['Neurologist', 'ENT'],
            'loss_of_smell': ['ENT', 'Neurologist'],
            'movement_stiffness': ['Neurologist'],
            'muscle_weakness': ['Neurologist', 'Orthopedist'],
            'stiff_neck': ['Neurologist', 'Orthopedist'],
            'visual_disturbances': ['Ophthalmologist', 'Neurologist'],
            
            # Cardiovascular symptoms
            'fast_heart_rate': ['Cardiologist'],
            'palpitations': ['Cardiologist'],
            'swollen_blood_vessels': ['Vascular Surgeon', 'Cardiologist'],
            'prominent_veins_on_calf': ['Vascular Surgeon'],
            
            # Endocrine symptoms
            'weight_gain': ['Endocrinologist', 'Internal Medicine'],
            'weight_loss': ['Endocrinologist', 'Internal Medicine'],
            'excessive_hunger': ['Endocrinologist'],
            'increased_appetite': ['Endocrinologist'],
            'enlarged_thyroid': ['Endocrinologist'],
            'irregular_sugar_level': ['Endocrinologist'],
            
            # Musculoskeletal symptoms
            'swelling_joints': ['Rheumatologist', 'Orthopedist'],
            'painful_walking': ['Orthopedist'],
            'muscle_wasting': ['Neurologist', 'Orthopedist'],
            'swollen_extremeties': ['Vascular Surgeon', 'Rheumatologist'],
            'swollen_legs': ['Vascular Surgeon', 'Cardiologist'],
            'brittle_nails': ['Dermatologist'],
            
            # Psychiatric/psychological symptoms
            'anxiety': ['Psychiatrist', 'Psychologist'],
            'depression': ['Psychiatrist', 'Psychologist'],
            'irritability': ['Psychiatrist', 'Psychologist'],
            'mood_swings': ['Psychiatrist', 'Psychologist'],
            'restlessness': ['Psychiatrist', 'Psychologist'],
            
            # Miscellaneous symptoms
            'patches_in_throat': ['ENT'],
            'cold_hands_and_feets': ['Vascular Surgeon', 'Endocrinologist'],
            'obesity': ['Endocrinologist', 'Internal Medicine'],
            'sunken_eyes': ['Ophthalmologist', 'General Practitioner'],
            'watering_from_eyes': ['Ophthalmologist'],
            'blurred_and_distorted_vision': ['Ophthalmologist'],
            'redness_of_eyes': ['Ophthalmologist'],
            'sinus_pressure': ['ENT'],
            'puffy_face_and_eyes': ['Allergist', 'Endocrinologist'],
            'toxic_look_(typhos)': ['Infectious Disease', 'Emergency Medicine'],
            'slurred_speech': ['Neurologist'],
            'fluid_overload': ['Cardiologist', 'Nephrologist'],
            'drying_and_tingling_lips': ['Dermatologist'],
            'abnormal_menstruation': ['Gynecologist'],
            'family_history': ['Geneticist', 'Internal Medicine'],
            'receiving_blood_transfusion': ['Hematologist'],
            'receiving_unsterile_injections': ['Infectious Disease'],
            'coma': ['Neurologist', 'Emergency Medicine'],
            'history_of_alcohol_consumption': ['Gastroenterologist', 'Hepatologist', 'Psychiatrist'],
            'bruising': ['Hematologist', 'Dermatologist'],
            'weakness_of_one_body_side': ['Neurologist']
        }
        
        for symptom_name, specialties in new_dataset_symptoms.items():
            if symptom_name in added_symptoms:  # Skip if already added
                continue
                
            # Format the symptom name for display (replace underscores with spaces, capitalize)
            display_name = ' '.join(word.capitalize() for word in symptom_name.split('_'))
                
            symptom = Symptom(
                name=display_name,
                description=f"Symptom requiring consultation with: {', '.join(specialties)}"
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