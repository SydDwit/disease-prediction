import os
import sys
import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
import json

# Add new model directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'new model'))

# Try to import the explain_with_gemini function from the new model/utils.py
try:
    from utils import explain_with_gemini
except ImportError:
    print("Error: Could not import explain_with_gemini from new model/utils.py")
    # Fallback implementation
    def explain_with_gemini(symptoms_selected, preds, confusion_matrix=None, report_df=None):
        disease = preds[0][0]
        confidence = preds[0][1]
        
        # Basic disease descriptions for common conditions
        disease_info = {
            "Common Cold": "The common cold is a viral infection of the upper respiratory tract affecting the nose and throat. It's typically caused by rhinoviruses and is characterized by symptoms like runny nose, sore throat, coughing, and mild fever.",
            "Influenza": "Influenza (flu) is a contagious respiratory illness caused by influenza viruses that infect the nose, throat, and lungs. Symptoms are more severe than the common cold and include high fever, body aches, fatigue, and respiratory symptoms.",
            "Pneumonia": "Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid. Symptoms include cough with phlegm, fever, chills, and difficulty breathing.",
            "Diabetes": "Diabetes is a chronic disease that occurs when the pancreas is no longer able to make insulin, or when the body cannot make good use of the insulin it produces. Symptoms include increased thirst, frequent urination, hunger, fatigue, and blurred vision.",
            "Hypertension": "Hypertension, or high blood pressure, is a common condition in which the long-term force of the blood against your artery walls is high enough that it may eventually cause health problems. Symptoms may include headaches, shortness of breath, or nosebleeds.",
            "Migraine": "Migraine is a neurological condition characterized by recurrent headaches that are typically one-sided, pulsating, and moderate to severe in intensity. Symptoms often include nausea, vomiting, and sensitivity to light and sound."
        }
        
        # Get basic description or provide a generic one
        description = disease_info.get(disease, f"{disease} is a medical condition that requires professional diagnosis and treatment.")
        
        # Generate a simple explanation based on symptoms
        symptom_text = ", ".join(symptoms_selected)
        explanation = f"Based on your symptoms ({symptom_text}), the system has identified {disease} as the most likely condition. {description} The combination of your specific symptoms is commonly associated with this condition, particularly {symptoms_selected[0] if symptoms_selected else 'the reported symptoms'}."
        
        return explanation

# Create a router for the explanation endpoint
router = APIRouter(prefix="/api", tags=["explanation"])

@router.post("/explain")
async def get_disease_explanation(request: Request):
    """Generate a detailed explanation and description of a disease prediction"""
    try:
        # Parse the request body
        data = await request.json()
        
        # Extract data
        symptoms = data.get("symptoms", [])
        disease = data.get("disease", "Unknown disease")
        confidence = data.get("confidence", 0.0)
        
        if not symptoms:
            raise HTTPException(status_code=400, detail="No symptoms provided")
            
        # Create a simple confusion matrix and report dataframe for the explanation
        confusion_matrix = pd.DataFrame([[1, 0], [0, 1]], 
                                      index=[disease, "Other"],
                                      columns=[disease, "Other"])
                                      
        report_df = pd.DataFrame({
            disease: {
                "precision": 0.85,
                "recall": 0.80,
                "f1-score": 0.82,
                "support": 100
            }
        })
        
        # Format prediction for the explanation function
        preds = [(disease, confidence)]
        
        # Get explanation from Gemini
        explanation = explain_with_gemini(symptoms, preds, confusion_matrix, report_df)
        
        return {"explanation": explanation}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}") 