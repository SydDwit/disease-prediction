import numpy as np
import pandas as pd
import joblib
import json
from typing import List, Dict, Any
from collections import defaultdict

# Load model and related files
model = joblib.load('models/random_forest_disease_model.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')

with open('models/symptoms.json', 'r') as f:
    symptoms_data = json.load(f)
    SYMPTOMS = [s['name'] for s in symptoms_data['symptoms']]
    SYMPTOM_IMPORTANCE = {s['name']: s['importance'] for s in symptoms_data['symptoms']}

with open('models/model_metrics.json', 'r') as f:
    model_metrics = json.load(f)
    DISEASE_METRICS = model_metrics['disease_metrics']

# Constants
MIN_CONFIDENCE_THRESHOLD = 0.3
HIGH_CONFIDENCE_THRESHOLD = 0.6
MAX_PREDICTIONS = 3

def predict_diseases(symptoms: List[str]) -> Dict[str, Any]:
    """
    Predict diseases based on symptoms with improved confidence handling
    and consideration of common conditions.
    """
    # Validate symptoms
    valid_symptoms = [s for s in symptoms if s in SYMPTOMS]
    if not valid_symptoms:
        return {
            "error": "No valid symptoms provided",
            "valid_symptoms": SYMPTOMS
        }
    
    # Create feature vector
    feature_vector = pd.DataFrame(np.zeros((1, len(SYMPTOMS))), columns=SYMPTOMS)
    for symptom in valid_symptoms:
        feature_vector[symptom] = 1
    
    # Get model predictions and probabilities
    probabilities = model.predict_proba(feature_vector)[0]
    
    # Calculate confidence scores with adjustments
    predictions = []
    for idx, prob in enumerate(probabilities):
        disease = label_encoder.classes_[idx]
        
        # Skip if probability is too low
        if prob < MIN_CONFIDENCE_THRESHOLD:
            continue
            
        # Get disease metrics
        disease_info = DISEASE_METRICS.get(disease, {})
        precision = disease_info.get('precision', 0.5)
        recall = disease_info.get('recall', 0.5)
        
        # Calculate symptom match score
        disease_top_symptoms = {s['symptom']: s['importance'] 
                              for s in disease_info.get('top_symptoms', [])}
        matching_symptoms = set(valid_symptoms) & set(disease_top_symptoms.keys())
        symptom_score = sum(disease_top_symptoms.get(s, 0) for s in matching_symptoms)
        
        # Adjust confidence based on multiple factors
        confidence = prob * 0.4 + precision * 0.3 + recall * 0.2 + symptom_score * 0.1
        
        # Additional adjustments for common vs rare conditions
        if len(matching_symptoms) / len(valid_symptoms) > 0.5:  # If more than 50% symptoms match
            confidence *= 1.2
        
        predictions.append({
            "disease": disease,
            "confidence": round(confidence * 100, 2),
            "matching_symptoms": list(matching_symptoms),
            "missing_key_symptoms": list(set(disease_top_symptoms.keys()) - set(valid_symptoms))
        })
    
    # Sort by confidence and get top predictions
    predictions.sort(key=lambda x: x['confidence'], reverse=True)
    top_predictions = predictions[:MAX_PREDICTIONS]
    
    # Prepare response
    response = {
        "success": True,
        "predictions": top_predictions,
        "input_symptoms": valid_symptoms,
        "confidence_levels": {
            "high": HIGH_CONFIDENCE_THRESHOLD * 100,
            "minimum": MIN_CONFIDENCE_THRESHOLD * 100
        }
    }
    
    # Add warning if confidence is low
    highest_confidence = top_predictions[0]['confidence'] if top_predictions else 0
    if highest_confidence < (MIN_CONFIDENCE_THRESHOLD * 100):
        response["warning"] = "Low confidence in predictions. Please consult a healthcare provider."
    
    return response 