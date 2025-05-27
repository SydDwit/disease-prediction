import joblib
import json
import os
import pandas as pd

# Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "new model", "app", "disease_model.pkl")
output_dir = os.path.join(base_dir, "backend", "models")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the model
print(f"Loading model from {model_path}...")
model_bundle = joblib.load(model_path)

# Extract symptoms
if isinstance(model_bundle, dict) and "symptoms" in model_bundle:
    # If the model is saved as a bundle with symptoms
    symptoms = model_bundle["symptoms"]
    print(f"Found {len(symptoms)} symptoms in the model bundle")
elif hasattr(model_bundle, "feature_names_in_"):
    # If the model has feature_names_in_ attribute (scikit-learn model)
    symptoms = model_bundle.feature_names_in_.tolist()
    print(f"Extracted {len(symptoms)} symptoms from model.feature_names_in_")
else:
    # Try to read from Training.csv
    try:
        data_path = os.path.join(base_dir, "data", "Training.csv")
        print(f"Attempting to read symptoms from {data_path}...")
        df = pd.read_csv(data_path)
        symptoms = df.drop("prognosis", axis=1).columns.tolist()
        print(f"Extracted {len(symptoms)} symptoms from Training.csv")
    except Exception as e:
        print(f"Error reading Training.csv: {e}")
        symptoms = []

# If we have symptoms, create the JSON file
if symptoms:
    # Create the symptoms JSON structure
    symptoms_data = {
        "symptoms": symptoms
    }
    
    # Save to JSON file
    output_path = os.path.join(output_dir, "symptoms.json")
    with open(output_path, "w") as f:
        json.dump(symptoms_data, f, indent=2)
    
    print(f"Successfully saved {len(symptoms)} symptoms to {output_path}")
else:
    print("No symptoms found. Could not create symptoms.json file.") 