import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import json

def train_and_save_model(
    train_csv_path="data/Training.csv", 
    model_save_dir="backend/models",
    analysis_dir="training_analysis"
):
    # Create directories if they don't exist
    os.makedirs(model_save_dir, exist_ok=True)
    os.makedirs(analysis_dir, exist_ok=True)
    
    # Normalize paths for cross-platform compatibility
    train_csv_path = os.path.normpath(train_csv_path)
    model_save_dir = os.path.normpath(model_save_dir)
    analysis_dir = os.path.normpath(analysis_dir)
    
    # Load data
    print(f"Loading data from {train_csv_path}...")
    df = pd.read_csv(train_csv_path)
    X = df.drop("prognosis", axis=1)
    y = df["prognosis"]

    # Encode labels
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    # Train model
    print("Training Random Forest model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Predictions and metrics
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)
    
    # Generate classification report
    report = classification_report(y_test, y_pred_test, target_names=le.classes_, output_dict=True)

    # Save metrics to file
    metrics_path = os.path.join(analysis_dir, "model_metrics.txt")
    with open(metrics_path, "w") as f:
        f.write(f"Train Accuracy: {train_acc:.4f}\nTest Accuracy: {test_acc:.4f}\n")
        f.write("\nClassification Report (Test):\n")
        f.write(classification_report(y_test, y_pred_test, target_names=le.classes_))

    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    
    # Confusion Matrix Visualization
    cm = confusion_matrix(y_test, y_pred_test)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=False, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix (Test Set)")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_dir, "confusion_matrix.png"))
    plt.close()

    # Feature importance plot
    importances = clf.feature_importances_
    indices = importances.argsort()[-10:][::-1]  # Top 10
    plt.figure(figsize=(8, 6))
    plt.barh(range(10), importances[indices], align="center")
    plt.yticks(range(10), [X.columns[i] for i in indices])
    plt.title("Top 10 Symptom Feature Importances")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_dir, "feature_importance.png"))
    plt.close()

    # Symptom-Disease Correlation Matrix
    corr_matrix = pd.DataFrame(0, index=X.columns, columns=le.classes_)
    for i in range(len(X)):
        symptoms_on = X.iloc[i][X.iloc[i] == 1].index.tolist()
        diagnosis = le.inverse_transform([y_encoded[i]])[0]
        for sym in symptoms_on:
            corr_matrix.loc[sym, diagnosis] += 1

    plt.figure(figsize=(16, 12))
    sns.heatmap(
        corr_matrix, cmap="viridis", cbar_kws={"label": "Occurrence"}, yticklabels=True
    )
    plt.title("Symptom-Disease Correlation Matrix")
    plt.xlabel("Disease")
    plt.ylabel("Symptom")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_dir, "symptom_disease_corr.png"))
    plt.close()

    # Save model metrics as JSON for the backend
    disease_metrics = {}
    for disease in le.classes_:
        if disease in report:
            disease_data = report[disease]
            # Get top symptoms for this disease
            disease_idx = np.where(le.classes_ == disease)[0][0]
            disease_samples = np.where(y_encoded == disease_idx)[0]
            symptom_counts = X.iloc[disease_samples].sum().sort_values(ascending=False)
            top_symptoms = []
            for symptom, count in symptom_counts.head(5).items():
                if count > 0:
                    importance = count / len(disease_samples)
                    top_symptoms.append({"symptom": symptom, "importance": float(importance)})
            
            disease_metrics[disease] = {
                "precision": float(disease_data["precision"]),
                "recall": float(disease_data["recall"]),
                "f1-score": float(disease_data["f1-score"]),
                "top_symptoms": top_symptoms
            }
    
    metrics_json = {
        "train_acc": float(train_acc),
        "test_acc": float(test_acc),
        "disease_metrics": disease_metrics
    }
    
    with open(os.path.join(model_save_dir, "model_metrics.json"), "w") as f:
        json.dump(metrics_json, f, indent=2)

    # Create symptoms.json for the backend
    symptoms_list = []
    for symptom in X.columns:
        importance = float(importances[list(X.columns).index(symptom)])
        symptoms_list.append({"name": symptom, "importance": importance})
    
    symptoms_json = {"symptoms": symptoms_list}
    with open(os.path.join(model_save_dir, "symptoms.json"), "w") as f:
        json.dump(symptoms_json, f, indent=2)
    
    # Save model and label encoder separately as expected by the backend
    print(f"Saving model to {model_save_dir}...")
    model_path = os.path.join(model_save_dir, "random_forest_disease_model.pkl")
    encoder_path = os.path.join(model_save_dir, "label_encoder.pkl")
    joblib.dump(clf, model_path)
    joblib.dump(le, encoder_path)
    
    print("Model training and saving complete!")


if __name__ == "__main__":
    train_and_save_model() 