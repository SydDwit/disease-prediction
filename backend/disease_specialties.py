"""
This module contains mappings between diseases and medical specialties.
These mappings are based on general medical knowledge and common practices.
"""

DISEASE_TO_SPECIALTY = {
    # Neurological diseases
    '(vertigo) paroymsal positional vertigo': ['Neurologist', 'ENT'],
    'migraine': ['Neurologist', 'Internal Medicine'],
    'paralysis (brain hemorrhage)': ['Neurologist', 'Neurosurgeon'],
    'cervical spondylosis': ['Neurologist', 'Orthopedist'],
    
    # Infectious diseases
    'aids': ['Infectious Disease', 'Immunologist'],
    'chicken pox': ['Infectious Disease', 'Dermatologist'],
    'dengue': ['Infectious Disease', 'Internal Medicine'],
    'typhoid': ['Infectious Disease', 'Gastroenterologist'],
    'hepatitis a': ['Gastroenterologist', 'Hepatologist', 'Infectious Disease'],
    'hepatitis b': ['Gastroenterologist', 'Hepatologist', 'Infectious Disease'],
    'hepatitis c': ['Gastroenterologist', 'Hepatologist', 'Infectious Disease'],
    'hepatitis d': ['Gastroenterologist', 'Hepatologist', 'Infectious Disease'],
    'hepatitis e': ['Gastroenterologist', 'Hepatologist', 'Infectious Disease'],
    'tuberculosis': ['Pulmonologist', 'Infectious Disease'],
    'common cold': ['General Practitioner', 'ENT'],
    'pneumonia': ['Pulmonologist', 'Infectious Disease'],
    'malaria': ['Infectious Disease', 'Internal Medicine'],
    'impetigo': ['Dermatologist', 'Infectious Disease'],
    
    # Dermatological conditions
    'acne': ['Dermatologist'],
    'psoriasis': ['Dermatologist', 'Immunologist'],
    'fungal infection': ['Dermatologist', 'Infectious Disease'],
    
    # Gastrointestinal diseases
    'alcoholic hepatitis': ['Gastroenterologist', 'Hepatologist'],
    'jaundice': ['Gastroenterologist', 'Hepatologist'],
    'chronic cholestasis': ['Gastroenterologist', 'Hepatologist'],
    'peptic ulcer diseae': ['Gastroenterologist'],
    'gastroenteritis': ['Gastroenterologist', 'Infectious Disease'],
    'gerd': ['Gastroenterologist'],
    'dimorphic hemmorhoids(piles)': ['Gastroenterologist', 'Colorectal Surgeon'],
    
    # Cardiovascular diseases
    'heart attack': ['Cardiologist', 'Emergency Medicine'],
    'varicose veins': ['Vascular Surgeon', 'Cardiologist'],
    'hypertension': ['Cardiologist', 'Internal Medicine'],
    
    # Respiratory diseases
    'bronchial asthma': ['Pulmonologist', 'Allergist'],
    
    # Endocrine diseases
    'diabetes': ['Endocrinologist'],
    'hyperthyroidism': ['Endocrinologist'],
    'hypothyroidism': ['Endocrinologist'],
    'hypoglycemia': ['Endocrinologist'],
    
    # Allergic conditions
    'allergy': ['Allergist', 'Immunologist'],
    'drug reaction': ['Allergist', 'Dermatologist'],
    
    # Musculoskeletal conditions
    'arthritis': ['Rheumatologist', 'Orthopedist'],
    'osteoarthristis': ['Orthopedist', 'Rheumatologist'],
    
    # Urological conditions
    'urinary tract infection': ['Urologist', 'Internal Medicine'],
    
    # Default fallback
    'default': ['Internal Medicine', 'Family Medicine', 'General Practice']
}

def get_relevant_specialties(disease):
    """
    Get relevant medical specialties for a given disease.
    
    Args:
        disease (str or int): The name of the disease or disease ID
        
    Returns:
        list: List of relevant medical specialties
    """
    # Convert to string if it's not already
    if not isinstance(disease, str):
        disease = str(disease)
    
    disease = disease.lower()
    
    # Direct disease lookup
    if disease in DISEASE_TO_SPECIALTY:
        return DISEASE_TO_SPECIALTY[disease]
        
    # Keyword-based mapping for diseases not directly listed
    keywords_to_specialties = {
        # Neurological keywords
        'vertigo': ['Neurologist', 'ENT'],
        'brain': ['Neurologist', 'Neurosurgeon'],
        'nerve': ['Neurologist'],
        'spinal': ['Neurologist', 'Orthopedist'],
        'migraine': ['Neurologist'],
        'paralysis': ['Neurologist', 'Neurosurgeon'],
        
        # Infectious disease keywords
        'infection': ['Infectious Disease'],
        'viral': ['Infectious Disease'],
        'bacterial': ['Infectious Disease'],
        'hepatitis': ['Gastroenterologist', 'Hepatologist'],
        'malaria': ['Infectious Disease'],
        'dengue': ['Infectious Disease'],
        'tuberculosis': ['Pulmonologist', 'Infectious Disease'],
        
        # Skin keywords
        'skin': ['Dermatologist'],
        'acne': ['Dermatologist'],
        'rash': ['Dermatologist', 'Allergist'],
        'psoriasis': ['Dermatologist'],
        'fungal': ['Dermatologist', 'Infectious Disease'],
        
        # Gastrointestinal keywords
        'liver': ['Gastroenterologist', 'Hepatologist'],
        'stomach': ['Gastroenterologist'],
        'intestine': ['Gastroenterologist'],
        'ulcer': ['Gastroenterologist'],
        'jaundice': ['Gastroenterologist', 'Hepatologist'],
        'hepatitis': ['Gastroenterologist', 'Hepatologist'],
        'cholestasis': ['Gastroenterologist'],
        'gastritis': ['Gastroenterologist'],
        'piles': ['Gastroenterologist', 'Colorectal Surgeon'],
        
        # Cardiovascular keywords
        'heart': ['Cardiologist'],
        'vein': ['Vascular Surgeon', 'Cardiologist'],
        'artery': ['Cardiologist', 'Vascular Surgeon'],
        'hypertension': ['Cardiologist', 'Internal Medicine'],
        
        # Respiratory keywords
        'lung': ['Pulmonologist'],
        'asthma': ['Pulmonologist', 'Allergist'],
        'respiratory': ['Pulmonologist'],
        'pneumonia': ['Pulmonologist', 'Infectious Disease'],
        
        # Endocrine keywords
        'diabetes': ['Endocrinologist'],
        'thyroid': ['Endocrinologist'],
        'hormone': ['Endocrinologist'],
        'glucose': ['Endocrinologist'],
        
        # Allergic keywords
        'allergy': ['Allergist', 'Immunologist'],
        'immune': ['Immunologist', 'Allergist'],
        
        # Musculoskeletal keywords
        'joint': ['Orthopedist', 'Rheumatologist'],
        'bone': ['Orthopedist'],
        'arthritis': ['Rheumatologist', 'Orthopedist'],
        
        # Urological keywords
        'urinary': ['Urologist'],
        'bladder': ['Urologist'],
        'kidney': ['Nephrologist', 'Urologist'],
    }
    
    # Check for keyword matches
    matched_specialties = set()
    for keyword, specialties in keywords_to_specialties.items():
        if keyword in disease:
            matched_specialties.update(specialties)
    
    if matched_specialties:
        return list(matched_specialties)
    
    # Return default specialties if no match found
    return DISEASE_TO_SPECIALTY['default'] 