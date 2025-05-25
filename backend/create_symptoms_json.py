import pandas as pd
import json

# Load the dataset
df = pd.read_csv('../data.csv')

# Get all column names except 'diseases' as these are the symptoms
symptoms_list = [col for col in df.columns if col != 'diseases']

# Create the symptoms dictionary
symptoms_data = {
    "symptoms": symptoms_list
}

# Save to JSON file
with open('models/symptoms.json', 'w') as f:
    json.dump(symptoms_data, f, indent=4)

print("Symptoms JSON file created successfully!")
print(f"Total number of symptoms: {len(symptoms_list)}")