import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import joblib
import json
import os
from collections import defaultdict

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

print("Loading filtered dataset...")
df = pd.read_csv('filtered_data.csv')

# Calculate disease weights based on frequency
disease_counts = df['diseases'].value_counts()
total_samples = len(df)
class_weights = {disease: total_samples / (len(disease_counts) * count) 
                for disease, count in disease_counts.items()}

# Prepare features and labels
X = df.drop('diseases', axis=1)
y = df['diseases']

# Label encoding
print("Encoding labels...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-test split
print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Train Random Forest model with improved parameters
print("\nTraining Random Forest model...")
rf_model = RandomForestClassifier(
    n_estimators=200,  # Increased from 100
    max_depth=30,      # Increased from 20
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced_subsample',  # Better handling of imbalanced classes
    random_state=42,
    n_jobs=-1
)

# Train with cross-validation to ensure stability
n_splits = 5
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
cv_scores = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), 1):
    X_fold_train, X_fold_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]
    
    rf_model.fit(X_fold_train, y_fold_train)
    fold_score = rf_model.score(X_fold_val, y_fold_val)
    cv_scores.append(fold_score)
    print(f"Fold {fold} accuracy: {fold_score:.4f}")

print(f"\nCross-validation mean accuracy: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})")

# Final training on full training set
rf_model.fit(X_train, y_train)

# Evaluate model
print("\nEvaluating model...")
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Calculate and store feature importance per disease
disease_feature_importance = defaultdict(dict)
feature_names = X.columns

for idx, disease in enumerate(label_encoder.classes_):
    disease_mask = (y_test == idx)
    if np.any(disease_mask):
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test == idx, 
            y_pred == idx, 
            average='binary'
        )
        disease_feature_importance[disease] = {
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'top_symptoms': []
        }
        
        # Get feature importance for this disease
        tree_feature_importance = []
        for tree in rf_model.estimators_:
            tree_importance = tree.feature_importances_
            predictions = tree.predict(X_test[disease_mask]) if np.any(disease_mask) else []
            correct_predictions = np.mean(predictions == idx) if len(predictions) > 0 else 0
            tree_feature_importance.append(tree_importance * correct_predictions)
        
        avg_feature_importance = np.mean(tree_feature_importance, axis=0)
        top_features_idx = np.argsort(avg_feature_importance)[-10:]  # Top 10 symptoms
        
        disease_feature_importance[disease]['top_symptoms'] = [
            {
                'symptom': feature_names[idx],
                'importance': float(avg_feature_importance[idx])
            }
            for idx in top_features_idx
        ]

# Save detailed metrics
metrics = {
    'accuracy': accuracy,
    'cross_validation_scores': {
        'mean': float(np.mean(cv_scores)),
        'std': float(np.std(cv_scores)),
        'scores': [float(score) for score in cv_scores]
    },
    'disease_metrics': disease_feature_importance
}

with open('models/model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)

# Print detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model and encoder
print("\nSaving model files...")
joblib.dump(rf_model, 'models/random_forest_disease_model.pkl', compress=3)
joblib.dump(label_encoder, 'models/label_encoder.pkl', compress=3)

# Create and save symptoms.json with importance scores
symptoms_importance = dict(zip(feature_names, rf_model.feature_importances_))
symptoms_data = {
    "symptoms": [
        {"name": symptom, "importance": float(importance)}
        for symptom, importance in symptoms_importance.items()
    ]
}

with open('models/symptoms.json', 'w') as f:
    json.dump(symptoms_data, f, indent=4)

print("\nSaved files:")
print("1. models/random_forest_disease_model.pkl")
print("2. models/label_encoder.pkl")
print("3. models/symptoms.json")
print("4. models/model_metrics.json")

print("\nModel training complete!") 