"""
This module contains mappings between diseases and medical specialties.
These mappings are based on general medical knowledge and common practices.
"""

DISEASE_TO_SPECIALTY = {
    # Neurological diseases
    'wernicke korsakoff syndrome': ['Neurologist', 'Psychiatrist'],
    'brain cancer': ['Neurosurgeon', 'Neuro-oncologist'],
    'alzheimer disease': ['Neurologist', 'Geriatrician'],
    'amyotrophic lateral sclerosis (als)': ['Neurologist'],
    'carpal tunnel syndrome': ['Orthopedist', 'Hand Surgeon'],
    'multiple sclerosis': ['Neurologist', 'Immunologist'],
    'parkinsons disease': ['Neurologist', 'Movement Disorder Specialist'],
    'epilepsy': ['Neurologist'],
    'migraine': ['Neurologist', 'Internal Medicine'],
    'stroke': ['Neurologist', 'Vascular Neurologist'],
    
    # Gastrointestinal diseases
    'crohn disease': ['Gastroenterologist', 'Colorectal Surgeon'],
    'ulcerative colitis': ['Gastroenterologist', 'Colorectal Surgeon'],
    'celiac disease': ['Gastroenterologist', 'Immunologist'],
    'cirrhosis': ['Gastroenterologist', 'Hepatologist'],
    'hepatitis': ['Gastroenterologist', 'Hepatologist', 'Infectious Disease'],
    
    # Cardiovascular diseases
    'heart disease': ['Cardiologist', 'Internal Medicine'],
    'heart attack': ['Cardiologist', 'Emergency Medicine'],
    'heart failure': ['Cardiologist', 'Internal Medicine'],
    'high blood pressure': ['Cardiologist', 'Internal Medicine'],
    'arrhythmia': ['Cardiologist', 'Electrophysiologist'],
    
    # Respiratory diseases
    'asthma': ['Pulmonologist', 'Allergist'],
    'copd': ['Pulmonologist', 'Internal Medicine'],
    'lung cancer': ['Pulmonologist', 'Oncologist', 'Thoracic Surgeon'],
    'pneumonia': ['Pulmonologist', 'Infectious Disease'],
    'tuberculosis': ['Pulmonologist', 'Infectious Disease'],
    
    # Endocrine diseases
    'diabetes': ['Endocrinologist'],
    'thyroid disease': ['Endocrinologist'],
    'cushing syndrome': ['Endocrinologist'],
    'addisons disease': ['Endocrinologist'],
    
    # Mental health conditions
    'depression': ['Psychiatrist', 'Psychologist'],
    'anxiety': ['Psychiatrist', 'Psychologist'],
    'bipolar disorder': ['Psychiatrist'],
    'schizophrenia': ['Psychiatrist'],
    'mental disorder': ['Psychiatrist', 'Psychologist'],
    
    # Emergency conditions
    'heart attack': ['Emergency Medicine', 'Cardiologist'],
    'stroke': ['Emergency Medicine', 'Neurologist'],
    'severe trauma': ['Emergency Medicine', 'Trauma Surgeon'],
    'sepsis': ['Emergency Medicine', 'Critical Care', 'Infectious Disease'],
    
    # Add specific mappings for commonly predicted diseases
    'salivary gland disorder': ['ENT, Oral & Maxillofacial Surgeon'],
    'poisoning': ['Emergency Medicine', 'Toxicologist'],
    'poisoning due to anticonvulsants': ['Emergency Medicine', 'Toxicologist', 'Neurologist'],
    'drug poisoning': ['Emergency Medicine', 'Toxicologist'],
    
    # Respiratory conditions
    'cough': ['Pulmonologist', 'Internal Medicine', 'ENT'],
    'respiratory infection': ['Pulmonologist', 'Infectious Disease'],
    'breathing difficulty': ['Pulmonologist', 'Emergency Medicine'],
    
    # Urological conditions
    'erectile dysfunction': ['Urologist', 'Endocrinologist', 'Internal Medicine'],
    'prostate cancer': ['Urologist', 'Oncologist'],
    'benign prostatic hyperplasia': ['Urologist'],
    'urinary tract infection': ['Urologist', 'Internal Medicine'],
    'kidney stones': ['Urologist', 'Nephrologist'],
    
    # Default fallback
    'default': ['Internal Medicine', 'Family Medicine', 'General Practice']
}

def get_relevant_specialties(disease):
    """
    Get relevant medical specialties for a given disease.
    
    Args:
        disease (str): The name of the disease
        
    Returns:
        list: List of relevant medical specialties
    """
    disease = disease.lower()
    
    # Direct disease lookup
    if disease in DISEASE_TO_SPECIALTY:
        return DISEASE_TO_SPECIALTY[disease]
        
    # Keyword-based mapping for diseases not directly listed
    keywords_to_specialties = {
        # Neurological keywords
        'brain': ['Neurologist', 'Neurosurgeon'],
        'nerve': ['Neurologist'],
        'spinal': ['Neurologist', 'Neurosurgeon'],
        'seizure': ['Neurologist'],
        'cognitive': ['Neurologist', 'Psychiatrist'],
        
        # Mental health keywords
        'mental': ['Psychiatrist', 'Psychologist'],
        'psychiatric': ['Psychiatrist'],
        'behavioral': ['Psychiatrist', 'Psychologist'],
        'mood': ['Psychiatrist'],
        'depression': ['Psychiatrist', 'Psychologist'],
        'anxiety': ['Psychiatrist', 'Psychologist'],
        
        # Respiratory keywords
        'cough': ['Pulmonologist', 'Internal Medicine'],
        'respiratory': ['Pulmonologist'],
        'breathing': ['Pulmonologist'],
        'airway': ['Pulmonologist', 'ENT'],
        
        # Emergency and toxicology keywords
        'poisoning': ['Emergency Medicine', 'Toxicologist'],
        'overdose': ['Emergency Medicine', 'Toxicologist'],
        'toxic': ['Emergency Medicine', 'Toxicologist'],
        
        # Salivary and oral keywords
        'salivary': ['ENT', 'Oral & Maxillofacial Surgeon'],
        'gland': ['ENT', 'Endocrinologist'],
        'oral': ['ENT', 'Oral & Maxillofacial Surgeon'],
        
        # Default keywords
        'general': ['Internal Medicine', 'Family Medicine'],
        'chronic': ['Internal Medicine', 'Family Medicine'],
        'primary': ['Internal Medicine', 'Family Medicine'],
        
        # Urological keywords
        'erectile': ['Urologist', 'Endocrinologist'],
        'prostate': ['Urologist', 'Oncologist'],
        'urinary': ['Urologist', 'Nephrologist'],
        'bladder': ['Urologist'],
        'kidney': ['Urologist', 'Nephrologist'],
        'testicular': ['Urologist'],
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