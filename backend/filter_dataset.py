import pandas as pd
import numpy as np
from collections import defaultdict

# Read the original dataset
print("Reading dataset...")
df = pd.read_csv('data.csv')

# Get disease counts
disease_counts = df['diseases'].value_counts()
print(f"Original number of diseases: {len(disease_counts)}")

# Create disease categories
common_diseases = disease_counts[disease_counts >= 1000].index
moderate_diseases = disease_counts[(disease_counts >= 100) & (disease_counts < 1000)].index
rare_diseases = disease_counts[disease_counts < 100].index

print(f"\nDisease Categories:")
print(f"Common diseases (>=1000 cases): {len(common_diseases)}")
print(f"Moderate diseases (100-999 cases): {len(moderate_diseases)}")
print(f"Rare diseases (<100 cases): {len(rare_diseases)}")

# Select diseases based on frequency
selected_diseases = list(common_diseases) + list(moderate_diseases)
df_filtered = df[df['diseases'].isin(selected_diseases)]

# Calculate symptom importance scores
symptom_columns = df.columns[1:]  # All columns except 'diseases'
symptom_scores = defaultdict(float)

for symptom in symptom_columns:
    # Calculate frequency
    freq_score = df_filtered[symptom].mean()
    
    # Calculate disease specificity (how unique the symptom is to specific diseases)
    disease_symptom_counts = df_filtered[df_filtered[symptom] == 1]['diseases'].value_counts()
    specificity_score = 1 - (len(disease_symptom_counts) / len(selected_diseases))
    
    # Combined score
    symptom_scores[symptom] = (freq_score + specificity_score) / 2

# Convert to pandas Series and sort
symptom_importance = pd.Series(symptom_scores)
sorted_symptoms = symptom_importance.sort_values(ascending=False)

# Select top 200 most important symptoms (increased from 100)
top_symptoms = sorted_symptoms.head(200).index
selected_columns = ['diseases'] + list(top_symptoms)

# Create final filtered dataset
final_df = df_filtered[selected_columns]

# Print statistics
print("\nDataset Statistics:")
print(f"Original dataset shape: {df.shape}")
print(f"Filtered dataset shape: {final_df.shape}")
print(f"Number of unique diseases: {final_df['diseases'].nunique()}")
print(f"Number of symptoms: {len(final_df.columns) - 1}")

# Calculate coverage
total_cases = len(df)
filtered_cases = len(final_df)
coverage_percentage = (filtered_cases / total_cases) * 100
print(f"\nData coverage: {coverage_percentage:.2f}% of original cases")

# Save filtered dataset
final_df.to_csv('filtered_data.csv', index=False)
print("\nFiltered dataset saved to 'filtered_data.csv'")

# Save symptom list with importance scores
with open('selected_symptoms.txt', 'w') as f:
    f.write("Selected Symptoms (with importance scores):\n")
    for i, symptom in enumerate(top_symptoms, 1):
        score = symptom_scores[symptom]
        f.write(f"{i}. {symptom} (Score: {score:.4f})\n")

# Save disease list with categories
with open('selected_diseases.txt', 'w') as f:
    f.write("Selected Diseases:\n\nCommon Diseases (>=1000 cases):\n")
    for disease in common_diseases:
        count = disease_counts[disease]
        f.write(f"- {disease} ({count} cases)\n")
    
    f.write("\nModerate Diseases (100-999 cases):\n")
    for disease in moderate_diseases:
        count = disease_counts[disease]
        f.write(f"- {disease} ({count} cases)\n") 