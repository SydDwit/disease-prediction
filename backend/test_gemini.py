"""
Test script for the Gemini API integration
"""
import os
import sys
import pandas as pd

# Add the new model directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'new model'))

# Try to import explain_with_gemini
try:
    from utils import explain_with_gemini
    print("✅ Successfully imported explain_with_gemini function from utils.py")
except ImportError as e:
    print(f"❌ Error importing explain_with_gemini: {e}")
    print("Please ensure the 'new model' directory contains utils.py with the explain_with_gemini function.")
    sys.exit(1)

# Check if GOOGLE_API_KEY is set
try:
    # Try to load dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Successfully loaded dotenv")
    except ImportError:
        print("⚠️ python-dotenv not installed. Will rely on environment variables.")
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        print("Please set the GOOGLE_API_KEY environment variable with your Google Gemini API key.")
        print("You can create a .env file in the backend directory with the following content:")
        print("GOOGLE_API_KEY=your_api_key_here")
        sys.exit(1)
    
    if api_key == "your_api_key_here":
        print("❌ GOOGLE_API_KEY is set to the default placeholder value")
        print("Please replace 'your_api_key_here' with your actual Google Gemini API key.")
        sys.exit(1)
        
    print(f"✅ GOOGLE_API_KEY is set (begins with {api_key[:4]}...)")
    
except Exception as e:
    print(f"❌ Error checking API key: {e}")
    sys.exit(1)

# Test data
test_symptoms = ["fever", "cough", "fatigue"]
test_prediction = ("Common Cold", 0.85)

# Create a simple confusion matrix for testing
confusion_matrix = pd.DataFrame(
    [[0.9, 0.05, 0.05], [0.1, 0.8, 0.1], [0.05, 0.15, 0.8]],
    index=["Common Cold", "Flu", "COVID-19"],
    columns=["Common Cold", "Flu", "COVID-19"]
)

# Create a classification report for testing
report_df = pd.DataFrame({
    "Common Cold": {
        "precision": 0.90,
        "recall": 0.85,
        "f1-score": 0.87,
        "support": 100
    }
})

# Test the explanation function
print("\nTesting Gemini API explanation generation...")
print(f"Symptoms: {', '.join(test_symptoms)}")
print(f"Prediction: {test_prediction[0]} with {test_prediction[1]*100:.1f}% confidence")

try:
    explanation = explain_with_gemini(test_symptoms, [test_prediction], confusion_matrix, report_df)
    print("\n=== Generated Explanation ===")
    print(explanation)
    print("=== End of Explanation ===\n")
    print("✅ Gemini API test successful!")
except Exception as e:
    print(f"❌ Error generating explanation: {e}")
    print("Please check your API key and internet connection.")
    sys.exit(1) 