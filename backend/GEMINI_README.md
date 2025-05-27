# Gemini API Integration for Disease Prediction

This README explains how to set up and use the Google Gemini API integration for providing AI-powered explanations of disease predictions.

## Overview

The integration uses Google's Gemini API to analyze symptoms and disease predictions, providing human-readable explanations that help users understand why a particular disease was predicted based on their symptoms.

## Setup Instructions

### 1. Get a Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or sign in with your Google account
3. Create a new API key
4. Copy your API key for the next step

### 2. Set Up Your Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```
# Google Gemini API key
GOOGLE_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.

### 3. Install Required Dependencies

Make sure you have the required Python packages installed:

```bash
cd backend
pip install python-dotenv google-generativeai pandas
```

## Testing the Integration

We've provided a test script to verify that your Gemini API integration is working correctly:

```bash
cd backend
python test_gemini.py
```

If everything is set up correctly, you should see a successful test message and a generated explanation.

## How It Works

1. When a user makes a disease prediction, the frontend sends the symptoms and prediction to the `/api/explain` endpoint
2. The backend uses the `explain_with_gemini` function from `new model/utils.py` to generate an explanation
3. The explanation is returned to the frontend and displayed to the user

## Troubleshooting

If you encounter issues:

1. **API Key Issues**: Make sure your API key is correctly set in the `.env` file
2. **Import Errors**: Ensure the `new model` directory is accessible and contains the `utils.py` file with the `explain_with_gemini` function
3. **Network Issues**: Check your internet connection, as the Gemini API requires internet access
4. **Rate Limiting**: Google may impose rate limits on API calls. If you're making many requests, you might hit these limits

## Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/app)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv) 