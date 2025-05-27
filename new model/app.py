import streamlit as st
import pandas as pd
import numpy as np
from utils import load_model, load_metrics, predict_top3, explain_with_gemini
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Smart Symptom Classifier", layout="wide")
tabs = st.tabs(["Prediction", "Dataset", "Model Evaluation"])

with tabs[0]:
    st.title("Smart Symptom Classifier: Prediction")

    model_bundle = load_model()
    all_symptoms = model_bundle["symptoms"]

    st.markdown("**Select symptoms (one-hot format):**")
    symptoms_selected = st.multiselect("Symptoms", all_symptoms)

    if st.button("Predict"):
        if len(symptoms_selected) == 0:
            st.warning("Please select at least one symptom.")
        else:
            preds, input_features = predict_top3(symptoms_selected)
            st.subheader("Top 3 Predictions")
            for idx, (disease, score) in enumerate(preds):
                highlight = "**" if idx == 0 else ""
                st.markdown(
                    f"{highlight}{idx+1}. {disease} ({score*100:.2f}%){highlight}"
                )

            # Model explainability (Gemini)
            metrics = load_metrics()
            confusion_matrix = pd.DataFrame(
                metrics["confusion_matrix"],
                index=model_bundle["encoder"].classes_,
                columns=model_bundle["encoder"].classes_,
            )
            report_df = (
                pd.DataFrame(metrics["report"])
                .transpose()[["precision", "recall", "f1-score"]]
                .dropna()
            )
            st.subheader("Model Reasoning (via Gemini API)")
            reason = explain_with_gemini(
                symptoms_selected, preds, confusion_matrix, report_df
            )
            st.info(reason)

with tabs[1]:
    st.title("Dataset")
    st.markdown("**Training Dataset**")
    train_df = pd.read_csv("data/Training.csv")
    st.dataframe(train_df, use_container_width=True)
    st.markdown("**Testing Dataset**")
    test_df = pd.read_csv("data/Testing.csv")
    st.dataframe(test_df, use_container_width=True)

with tabs[2]:
    st.title("Model Evaluation")

    metrics = load_metrics()
    model_bundle = load_model()
    le = model_bundle["encoder"]

    # Confusion matrix
    st.subheader("Confusion Matrix")
    cm = metrics["confusion_matrix"]
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=False,
        fmt="d",
        cmap="Blues",
        xticklabels=le.classes_,
        yticklabels=le.classes_,
        ax=ax1,
    )
    ax1.set_xlabel("Predicted")
    ax1.set_ylabel("Actual")
    st.pyplot(fig1)

    # Feature importances
    st.subheader("Top 10 Symptom Importances")
    importances = metrics["feature_importances"]
    symptoms = model_bundle["symptoms"]
    indices = np.argsort(importances)[-10:][::-1]
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.barh(range(10), importances[indices], align="center")
    ax2.set_yticks(range(10))
    ax2.set_yticklabels([symptoms[i] for i in indices])
    ax2.set_xlabel("Importance")
    st.pyplot(fig2)

    # Classification report
    st.subheader("Classification Report (Test)")
    report_df = (
        pd.DataFrame(metrics["report"])
        .transpose()[["precision", "recall", "f1-score"]]
        .dropna()
    )
    st.dataframe(report_df)

    # Symptom-disease correlation (show image if exists)
    st.subheader("Symptom-Disease Correlation Matrix")
    corr_img = "app/symptom_disease_corr.png"
    if os.path.exists(corr_img):
        st.image(corr_img, use_container_width=True)
    else:
        st.write("Correlation matrix image not found. Please retrain the model.")

    # Accuracy scores
    st.markdown(f"**Train Accuracy:** {metrics['train_acc']:.4f}")
    st.markdown(f"**Test Accuracy:** {metrics['test_acc']:.4f}")
