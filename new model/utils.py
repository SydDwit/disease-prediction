import joblib
import numpy as np
import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

MODEL_PATH = "app/disease_model.pkl"
METRICS_PATH = "app/model_metrics.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def load_metrics():
    return joblib.load(METRICS_PATH)


def predict_top3(symptoms_selected):
    model_bundle = load_model()
    clf = model_bundle["model"]
    le = model_bundle["encoder"]
    all_symptoms = model_bundle["symptoms"]
    # Encode input as one-hot
    input_features = np.zeros(len(all_symptoms))
    for idx, sym in enumerate(all_symptoms):
        if sym in symptoms_selected:
            input_features[idx] = 1
    probs = clf.predict_proba([input_features])[0]
    top_idxs = np.argsort(probs)[::-1][:3]
    preds = [(le.inverse_transform([i])[0], probs[i]) for i in top_idxs]
    return preds, input_features


def explain_with_gemini(symptoms_selected, preds, confusion_matrix=None, report_df=None):
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        return "No Gemini API key set. Please add GOOGLE_API_KEY to your .env file."
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    pred_str = ", ".join([f"{d} ({s*100:.1f}%)" for d, s in preds])
    cm_str = confusion_matrix.to_string() if confusion_matrix is not None else "Not available"
    class_metrics_str = report_df.to_string() if report_df is not None else "Not available"
    
    prompt = f"""
Given the symptoms: {', '.join(symptoms_selected)}
The model predicted these diseases (with probabilities): {pred_str}.

I need a detailed, informative explanation about the top predicted disease. Please include:

1. A thorough description of what {preds[0][0]} is, including its causes, typical progression, and how it affects the body

2. An explanation of why the symptoms ({', '.join(symptoms_selected)}) specifically point to {preds[0][0]}, discussing how each symptom relates to the disease process

3. How these symptoms typically manifest in this condition, including any patterns or characteristics that are distinctive

4. Information about why this prediction makes medical sense, considering the combination of symptoms

5. Any important health information that a patient should know about this condition

Make your explanation detailed, educational, and conversational - as if a doctor is explaining the condition to a patient. Avoid medical jargon when possible, but include necessary medical terms with simple explanations.

DO NOT MENTION ANYTHING ABOUT THE MODEL, PREDICTION SYSTEM, OR MACHINE LEARNING IN YOUR RESPONSE.
DO NOT REFER TO CONFIDENCE SCORES OR PROBABILITIES.
DO NOT MENTION THE CONFUSION MATRIX OR METRICS.
FOCUS SOLELY ON PROVIDING A HELPFUL MEDICAL EXPLANATION OF THE DISEASE AND HOW IT RELATES TO THE GIVEN SYMPTOMS.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API call failed: {e}"
