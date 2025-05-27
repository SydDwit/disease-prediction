import joblib
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "new model", "app", "disease_model.pkl")
output_path = os.path.join(base_dir, "new model", "app", "label_encoder.pkl")

print(f"Loading model from {model_path}...")
model_bundle = joblib.load(model_path)

# Extract or create disease classes
if isinstance(model_bundle, dict):
    # If model is stored as a dictionary bundle
    if "label_encoder" in model_bundle:
        label_encoder = model_bundle["label_encoder"]
        print(f"Found existing label encoder in model bundle with {len(label_encoder.classes_)} classes")
    elif "classes_" in model_bundle:
        label_encoder = LabelEncoder()
        label_encoder.classes_ = model_bundle["classes_"]
        print(f"Created label encoder from classes in model bundle: {len(label_encoder.classes_)} classes")
    else:
        # Try to extract from model
        model = model_bundle.get("model", model_bundle)
        if hasattr(model, "classes_"):
            label_encoder = LabelEncoder()
            label_encoder.classes_ = model.classes_
            print(f"Created label encoder from model classes: {len(label_encoder.classes_)} classes")
        else:
            # Create a default label encoder with common diseases
            print("No classes found in model, creating default label encoder")
            label_encoder = LabelEncoder()
            # Read disease names from diseases_list.json if available
            try:
                import json
                with open(os.path.join(base_dir, "diseases_list.json"), "r") as f:
                    diseases_data = json.load(f)
                    diseases = [d["disease"] for d in diseases_data]
                    print(f"Loaded {len(diseases)} diseases from diseases_list.json")
            except:
                # Fallback to common disease names
                diseases = [
                    "Common Cold", "Pneumonia", "Diabetes", "Hypertension", 
                    "Arthritis", "Migraine", "Asthma", "Influenza",
                    "Hepatitis", "Dengue", "Tuberculosis", "Malaria",
                    "Typhoid", "Jaundice", "Chicken pox", "Measles",
                    "Acne", "Psoriasis", "Impetigo"
                ]
            label_encoder.classes_ = np.array(diseases)
else:
    # If model is a direct model object
    if hasattr(model_bundle, "classes_"):
        label_encoder = LabelEncoder()
        label_encoder.classes_ = model_bundle.classes_
        print(f"Created label encoder from model classes: {len(label_encoder.classes_)} classes")
    else:
        # Try to infer from the model structure
        print("Model doesn't have classes attribute, trying to infer from structure")
        label_encoder = LabelEncoder()
        try:
            # For ensemble models, classes might be in estimators
            if hasattr(model_bundle, "estimators_") and len(model_bundle.estimators_) > 0:
                if hasattr(model_bundle.estimators_[0], "classes_"):
                    label_encoder.classes_ = model_bundle.estimators_[0].classes_
                    print(f"Created label encoder from first estimator: {len(label_encoder.classes_)} classes")
            else:
                # Read disease names from diseases_list.json
                import json
                with open(os.path.join(base_dir, "diseases_list.json"), "r") as f:
                    diseases_data = json.load(f)
                    diseases = [d["disease"] for d in diseases_data]
                    label_encoder.classes_ = np.array(diseases)
                    print(f"Created label encoder with {len(diseases)} diseases from diseases_list.json")
        except Exception as e:
            print(f"Error inferring classes: {e}")
            # Create a default label encoder
            diseases = [
                "Common Cold", "Pneumonia", "Diabetes", "Hypertension", 
                "Arthritis", "Migraine", "Asthma", "Influenza",
                "Hepatitis", "Dengue", "Tuberculosis", "Malaria",
                "Typhoid", "Jaundice", "Chicken pox", "Measles",
                "Acne", "Psoriasis", "Impetigo"
            ]
            label_encoder.classes_ = np.array(diseases)
            print(f"Created default label encoder with {len(diseases)} common diseases")

# Save the label encoder
print(f"Saving label encoder with {len(label_encoder.classes_)} classes to {output_path}")
joblib.dump(label_encoder, output_path)
print("Label encoder saved successfully!") 