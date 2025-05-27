/**
 * Service for getting disease analysis using Gemini API
 */

const API_URL = 'http://localhost:8000/api';

/**
 * Get an analysis for a disease prediction based on symptoms
 * 
 * @param {Array} symptoms - List of symptom strings
 * @param {Object} prediction - The prediction object with disease and confidence
 * @returns {Promise<string>} - The analysis text
 */
export const getExplanation = async (symptoms, prediction) => {
  try {
    const response = await fetch(`${API_URL}/explain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        symptoms,
        disease: prediction.disease,
        confidence: prediction.confidence
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to get analysis: ${response.status}`);
    }

    const data = await response.json();
    return data.explanation;
  } catch (error) {
    console.error('Error getting analysis:', error);
    return 'Unable to generate analysis at this time.';
  }
};

export default {
  getExplanation,
}; 