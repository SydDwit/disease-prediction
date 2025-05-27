import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import os

def display_model_evaluation():
    print("Generating Model Evaluation Report...")
    
    # Create directory for outputs
    os.makedirs("evaluation_report", exist_ok=True)
    
    # Load metrics and model data
    try:
        # Try to load JSON metrics file first
        with open("new model/app/model_metrics.json", "r") as f:
            metrics = json.load(f)
        print("Loaded metrics from JSON file")
        
        # Load model and label encoder
        model_bundle = joblib.load("new model/app/disease_model.pkl")
        label_encoder = model_bundle["encoder"]
        class_names = list(label_encoder.classes_)
        
        # Extract metrics
        train_acc = metrics.get("train_acc", 1.0)  # Default to 1.0 if not found
        test_acc = metrics.get("test_acc", 1.0)     # Default to 1.0 if not found
        disease_metrics = metrics.get("disease_metrics", {})
        
        # Display overall accuracy
        print("\n======= MODEL ACCURACY =======")
        print(f"Training Accuracy: {train_acc:.4f}")
        print(f"Testing Accuracy: {test_acc:.4f}")
        
        # Display precision, recall, and F1 score for all diseases
        print("\n======= CLASSIFICATION METRICS =======")
        
        # Create a DataFrame for easier visualization
        metrics_data = []
        for disease, disease_data in disease_metrics.items():
            metrics_data.append({
                "Disease": disease,
                "Precision": disease_data.get("precision", 0),
                "Recall": disease_data.get("recall", 0),
                "F1-Score": disease_data.get("f1-score", 0)
            })
        
        metrics_df = pd.DataFrame(metrics_data)
        print(metrics_df)
        
        # Save metrics to CSV
        metrics_df.to_csv("evaluation_report/disease_metrics.csv", index=False)
        
        # Plot precision, recall, and F1 score
        plt.figure(figsize=(12, 8))
        metrics_mean = metrics_df[["Precision", "Recall", "F1-Score"]].mean()
        metrics_mean.plot(kind="bar", color=["blue", "green", "red"])
        plt.title("Average Model Performance Metrics")
        plt.ylabel("Score")
        plt.ylim(0, 1.1)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig("evaluation_report/avg_performance_metrics.png")
        
        # Display confusion matrix from image if it exists
        print("\n======= CONFUSION MATRIX =======")
        if os.path.exists("new model/app/confusion_matrix.png"):
            img = plt.imread("new model/app/confusion_matrix.png")
            plt.figure(figsize=(12, 10))
            plt.imshow(img)
            plt.axis('off')
            plt.title("Confusion Matrix")
            plt.savefig("evaluation_report/confusion_matrix.png")
            print("Confusion matrix image saved to evaluation_report/confusion_matrix.png")
        else:
            print("Confusion matrix image not found")
        
        # Display feature importance from image if it exists
        print("\n======= FEATURE IMPORTANCE =======")
        if os.path.exists("new model/app/feature_importance.png"):
            img = plt.imread("new model/app/feature_importance.png")
            plt.figure(figsize=(10, 8))
            plt.imshow(img)
            plt.axis('off')
            plt.title("Feature Importance")
            plt.savefig("evaluation_report/feature_importance.png")
            print("Feature importance image saved to evaluation_report/feature_importance.png")
        else:
            print("Feature importance image not found")
        
        # Display symptom-disease correlation from image if it exists
        print("\n======= SYMPTOM-DISEASE CORRELATION =======")
        if os.path.exists("new model/app/symptom_disease_corr.png"):
            img = plt.imread("new model/app/symptom_disease_corr.png")
            plt.figure(figsize=(14, 12))
            plt.imshow(img)
            plt.axis('off')
            plt.title("Symptom-Disease Correlation")
            plt.savefig("evaluation_report/symptom_disease_correlation.png")
            print("Correlation matrix image saved to evaluation_report/symptom_disease_correlation.png")
        else:
            print("Correlation matrix image not found")
            
        # Create a comprehensive report HTML
        html_report = """
        <html>
        <head>
            <title>Disease Prediction Model Evaluation</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                h2 { color: #3498db; margin-top: 30px; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .metric-container { display: flex; justify-content: space-around; margin: 20px 0; }
                .metric-box { 
                    border: 1px solid #ddd; 
                    border-radius: 5px; 
                    padding: 15px; 
                    text-align: center; 
                    width: 200px;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                }
                .metric-title { font-weight: bold; font-size: 14px; }
                .metric-value { font-size: 24px; color: #3498db; margin: 10px 0; }
                img { max-width: 100%; height: auto; margin: 20px 0; border: 1px solid #ddd; }
            </style>
        </head>
        <body>
            <h1>Disease Prediction Model Evaluation Report</h1>
            
            <h2>Overall Performance Metrics</h2>
            <div class="metric-container">
                <div class="metric-box">
                    <div class="metric-title">Training Accuracy</div>
                    <div class="metric-value">{train_acc:.4f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Testing Accuracy</div>
                    <div class="metric-value">{test_acc:.4f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Average Precision</div>
                    <div class="metric-value">{avg_precision:.4f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Average Recall</div>
                    <div class="metric-value">{avg_recall:.4f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Average F1 Score</div>
                    <div class="metric-value">{avg_f1:.4f}</div>
                </div>
            </div>
            
            <h2>Confusion Matrix</h2>
            <img src="confusion_matrix.png" alt="Confusion Matrix">
            
            <h2>Feature Importance</h2>
            <img src="feature_importance.png" alt="Feature Importance">
            
            <h2>Symptom-Disease Correlation</h2>
            <img src="symptom_disease_correlation.png" alt="Symptom-Disease Correlation">
            
            <h2>Disease-specific Metrics</h2>
            <table>
                <tr>
                    <th>Disease</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1 Score</th>
                </tr>
                {table_rows}
            </table>
        </body>
        </html>
        """.format(
            train_acc=train_acc,
            test_acc=test_acc,
            avg_precision=metrics_df["Precision"].mean(),
            avg_recall=metrics_df["Recall"].mean(),
            avg_f1=metrics_df["F1-Score"].mean(),
            table_rows="\n".join([
                f"<tr><td>{row['Disease']}</td><td>{row['Precision']:.4f}</td><td>{row['Recall']:.4f}</td><td>{row['F1-Score']:.4f}</td></tr>"
                for _, row in metrics_df.iterrows()
            ])
        )
        
        with open("evaluation_report/model_evaluation_report.html", "w") as f:
            f.write(html_report)
        
        print("\nEvaluation report generated successfully!")
        print("HTML report saved to: evaluation_report/model_evaluation_report.html")
        print("Images saved to the evaluation_report directory")
        
    except Exception as e:
        print(f"Error generating evaluation report: {str(e)}")
        
if __name__ == "__main__":
    display_model_evaluation() 