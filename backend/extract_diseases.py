import pandas as pd
import json
import os
from disease_specialties import get_relevant_specialties

# Read the dataset
df = pd.read_csv('data.csv')  # Assuming data.csv is in the root directory

# Get unique diseases and sort them
unique_diseases = sorted(df['diseases'].unique())

# Create a dictionary with diseases and their counts
disease_info = {
    disease: {
        'count': int(df[df['diseases'] == disease].shape[0]),
        'mapped_specialties': get_relevant_specialties(disease)  # Get specialties for each disease
    }
    for disease in unique_diseases
}

# Save to JSON file
with open('diseases_list.json', 'w') as f:
    json.dump(disease_info, f, indent=4)

print(f"Found {len(unique_diseases)} unique diseases and saved them to diseases_list.json")

# Print some statistics
specialties_count = {}
unmapped_diseases = []

for disease, info in disease_info.items():
    specialties = info['mapped_specialties']
    if specialties == ['Internal Medicine', 'Family Medicine', 'General Practice']:
        unmapped_diseases.append(disease)
    for specialty in specialties:
        specialties_count[specialty] = specialties_count.get(specialty, 0) + 1

print("\nTop 10 most common specialties:")
for specialty, count in sorted(specialties_count.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{specialty}: {count} diseases")

print(f"\nNumber of diseases with only default specialties: {len(unmapped_diseases)}")
print("\nSample of unmapped diseases:")
for disease in sorted(unmapped_diseases)[:10]:
    print(f"- {disease}") 