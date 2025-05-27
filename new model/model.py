import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os


def train_and_save_model(
    train_csv_path="data/Training.csv", model_save_path="app/disease_model.pkl"
):
    # Load data
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
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Predictions and metrics
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    # Save metrics to file
    with open("app/model_metrics.txt", "w") as f:
        f.write(f"Train Accuracy: {train_acc:.4f}\nTest Accuracy: {test_acc:.4f}\n")
        f.write("\nClassification Report (Test):\n")
        f.write(classification_report(y_test, y_pred_test, target_names=le.classes_))

    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print("\nClassification Report (Test):")
    print(classification_report(y_test, y_pred_test, target_names=le.classes_))

    # Confusion Matrix Visualization
    cm = confusion_matrix(y_test, y_pred_test)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=False, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix (Test Set)")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig("app/confusion_matrix.png")
    plt.close()

    # Feature importance plot (Top 10)
    importances = clf.feature_importances_
    indices = importances.argsort()[-10:][::-1]  # Top 10
    plt.figure(figsize=(8, 6))
    plt.barh(range(10), importances[indices], align="center")
    plt.yticks(range(10), [X.columns[i] for i in indices])
    plt.title("Top 10 Symptom Feature Importances")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig("app/feature_importance.png")
    plt.close()

    # Symptom-Disease Correlation Matrix
    # Create one-hot matrix: rows=symptoms, columns=diseases
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
    plt.savefig("app/symptom_disease_corr.png")
    plt.close()

    # Save model and label encoder
    joblib.dump(
        {"model": clf, "encoder": le, "symptoms": X.columns.tolist()}, model_save_path
    )
    print("Model and encoder saved!")


if __name__ == "__main__":
    # Ensure app directory exists
    os.makedirs("app", exist_ok=True)
    train_and_save_model()
