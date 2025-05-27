import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
import os

def generate_correlation_graphs():
    print("Generating correlation graphs and metric visualizations...")
    
    # Create directory for outputs
    os.makedirs("evaluation_report", exist_ok=True)
    
    try:
        # Load training data
        train_data = pd.read_csv("data/Training.csv")
        
        # Load model bundle and metrics
        model_bundle = joblib.load("new model/app/disease_model.pkl")
        with open("new model/app/model_metrics.json", "r") as f:
            metrics = json.load(f)
        
        # Extract disease metrics
        disease_metrics = metrics.get("disease_metrics", {})
        
        # 1. Symptom-Disease Correlation Heatmap
        print("Generating symptom-disease correlation heatmap...")
        
        # Extract the symptoms from the training data
        symptoms = train_data.columns[:-1]  # All columns except 'prognosis'
        diseases = train_data['prognosis'].unique()
        
        # Create correlation matrix
        corr_matrix = pd.DataFrame(0, index=symptoms, columns=diseases)
        
        # Calculate correlation
        for disease in diseases:
            disease_rows = train_data[train_data['prognosis'] == disease]
            for symptom in symptoms:
                corr_matrix.loc[symptom, disease] = disease_rows[symptom].mean()
        
        # Filter to show only relevant correlations (where correlation > 0)
        # And select top symptoms for visualization clarity
        nonzero_symptoms = []
        for symptom in symptoms:
            if corr_matrix.loc[symptom].sum() > 0:
                nonzero_symptoms.append(symptom)
                
        # Select a subset of symptoms and diseases for better visualization
        top_symptoms = nonzero_symptoms[:30]  # Top 30 symptoms
        
        # Create filtered correlation matrix
        filtered_corr = corr_matrix.loc[top_symptoms]
        
        # Plot heatmap
        plt.figure(figsize=(20, 15))
        sns.heatmap(filtered_corr, cmap='viridis', annot=False, linewidths=.5)
        plt.title('Top 30 Symptoms Correlation with Diseases', fontsize=16)
        plt.xlabel('Diseases', fontsize=14)
        plt.ylabel('Symptoms', fontsize=14)
        plt.xticks(rotation=90, fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        plt.tight_layout()
        plt.savefig("evaluation_report/symptom_disease_correlation.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        # 2. Top Symptoms for Each Disease
        print("Generating top symptoms for diseases...")
        
        # Create a metric to aggregate performance across diseases
        metrics_data = []
        for disease, data in disease_metrics.items():
            if 'top_symptoms' in data:
                metrics_data.append({
                    'Disease': disease,
                    'Precision': data.get('precision', 0),
                    'Recall': data.get('recall', 0),
                    'F1-Score': data.get('f1-score', 0),
                    'Top Symptoms': ', '.join([s['symptom'] for s in data.get('top_symptoms', [])[:5]])
                })
        
        metrics_df = pd.DataFrame(metrics_data)
        
        # 3. Disease Performance Metrics
        print("Generating disease performance metrics visualization...")
        
        # Plot precision, recall, and F1 scores for top diseases
        top_diseases = metrics_df.sort_values('F1-Score', ascending=False).head(15)
        
        metrics_plot = pd.DataFrame({
            'Precision': top_diseases['Precision'],
            'Recall': top_diseases['Recall'],
            'F1-Score': top_diseases['F1-Score']
        }, index=top_diseases['Disease'])
        
        plt.figure(figsize=(14, 10))
        metrics_plot.plot(kind='bar', figsize=(14, 10))
        plt.title('Performance Metrics for Top 15 Diseases', fontsize=16)
        plt.xlabel('Disease', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.ylim(0, 1.1)
        plt.legend(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("evaluation_report/disease_performance_metrics.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        # 4. Top Symptoms Importance
        print("Generating top symptoms importance visualization...")
        
        # Aggregate top symptoms across all diseases
        symptom_importance = {}
        for disease, data in disease_metrics.items():
            if 'top_symptoms' in data:
                for symptom_data in data.get('top_symptoms', []):
                    symptom = symptom_data.get('symptom')
                    importance = symptom_data.get('importance', 0)
                    
                    if symptom in symptom_importance:
                        symptom_importance[symptom] += importance
                    else:
                        symptom_importance[symptom] = importance
        
        # Convert to DataFrame and sort
        symptom_df = pd.DataFrame({
            'Symptom': list(symptom_importance.keys()),
            'Importance': list(symptom_importance.values())
        })
        symptom_df = symptom_df.sort_values('Importance', ascending=False).head(20)
        
        # Plot
        plt.figure(figsize=(12, 10))
        plt.barh(symptom_df['Symptom'], symptom_df['Importance'], color='teal')
        plt.title('Top 20 Most Important Symptoms Across All Diseases', fontsize=16)
        plt.xlabel('Cumulative Importance', fontsize=14)
        plt.ylabel('Symptom', fontsize=14)
        plt.gca().invert_yaxis()  # Display highest importance at the top
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("evaluation_report/top_symptoms_importance.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        # 5. Performance Distribution
        print("Generating performance distribution visualization...")
        
        plt.figure(figsize=(10, 6))
        sns.kdeplot(metrics_df['Precision'], label='Precision', shade=True)
        sns.kdeplot(metrics_df['Recall'], label='Recall', shade=True)
        sns.kdeplot(metrics_df['F1-Score'], label='F1-Score', shade=True)
        plt.title('Distribution of Performance Metrics Across Diseases', fontsize=16)
        plt.xlabel('Score', fontsize=14)
        plt.ylabel('Density', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("evaluation_report/performance_distribution.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        print("All correlation graphs and visualizations generated successfully!")
        
    except Exception as e:
        print(f"Error generating correlation graphs: {str(e)}")

if __name__ == "__main__":
    generate_correlation_graphs() 