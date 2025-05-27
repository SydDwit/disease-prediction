import React, { useState, useEffect } from 'react';
import Navbar from "./Navbar";
import AsyncSelect from 'react-select/async';
import DoctorCard from './DoctorCard';
import { getExplanation } from '../services/explanationService';

const Home = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [appointments, setAppointments] = useState([]);
  const [appointmentsLoading, setAppointmentsLoading] = useState(true);
  const [alternativeDiseases, setAlternativeDiseases] = useState([]);
  const [analysis, setAnalysis] = useState('');
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        setAppointmentsLoading(true);
        setError('');  // Clear any previous errors
        const userId = localStorage.getItem('userId');
        
        if (!userId) {
          console.error('No user ID found in localStorage');
          setError('Please log in again to view your appointments');
          return;
        }
        
        console.log('Fetching appointments for user:', userId);
        
        const response = await fetch(`http://localhost:8000/api/users/${userId}/appointments`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          console.error('Appointments fetch error:', errorData);
          throw new Error(errorData.detail || 'Failed to fetch appointments');
        }
        
        const data = await response.json();
        console.log('Appointments data:', data);
        
        if (!Array.isArray(data)) {
          throw new Error('Invalid appointments data received');
        }
        
        setAppointments(data);
        setError('');  // Clear any errors if successful
      } catch (err) {
        console.error('Error fetching appointments:', err);
        setError(err.message || 'Failed to fetch appointments. Please try again later.');
        setAppointments([]);  // Clear appointments on error
      } finally {
        setAppointmentsLoading(false);
      }
    };

    fetchAppointments();

    // Add focus event listener to refresh appointments when tab becomes active
    const handleFocus = () => {
      fetchAppointments();
    };

    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, []);

  const loadSymptoms = async (inputValue) => {
    try {
      const response = await fetch('http://localhost:8000/api/symptoms');
      
      if (!response.ok) {
        throw new Error('Failed to load symptoms');
      }
      
      const data = await response.json();
      
      if (!data.symptoms || !Array.isArray(data.symptoms)) {
        console.error('Invalid symptoms data format:', data);
        setError('Error loading symptoms: Invalid data format');
        return [];
      }
      
      console.log(`Loaded ${data.symptoms.length} symptoms`);
      
      return data.symptoms
        .filter(symptom => 
          symptom.toLowerCase().includes(inputValue.toLowerCase())
        )
        .map(symptom => ({
          label: symptom,
          value: symptom
        }));
    } catch (err) {
      console.error('Error loading symptoms:', err);
      setError(`Error loading symptoms: ${err.message}`);
      return [];
    }
  };

  const handlePrediction = async () => {
    try {
      setLoading(true);
      setError('');
      setPrediction(null); // Clear any previous predictions
      setAlternativeDiseases([]); // Clear any alternative diseases
      setAnalysis(''); // Clear any previous analysis
      
      if (selectedSymptoms.length === 0) {
        throw new Error('Please select at least one symptom');
      }
      
      console.log('Selected symptoms:', selectedSymptoms.map(s => s.value));
      
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms: selectedSymptoms.map(s => s.value)
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = 'Prediction failed';
        
        try {
          // Try to parse as JSON to get detailed error
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || 'Prediction failed';
        } catch (e) {
          // If not JSON, use the raw text
          errorMessage = errorText || `Prediction failed with status ${response.status}`;
        }
        
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log('Prediction response:', data);
      
      if (!data.predictions || !Array.isArray(data.predictions) || data.predictions.length === 0) {
        throw new Error('No predictions returned from the server');
      }
      
      // Ensure all predictions have string disease names
      data.predictions = data.predictions.map(pred => ({
        ...pred,
        disease: String(pred.disease)
      }));
      
      // Generate alternative diseases based on the primary prediction
      const mainPrediction = data.predictions[0];
      
      // Generate two alternative diseases
      let alternatives = [
        {
          disease: `${mainPrediction.disease} (Mild)`,
          confidence: mainPrediction.confidence * 0.8,
          matching_symptoms: mainPrediction.matching_symptoms,
          symptom_coverage: mainPrediction.symptom_coverage * 0.9,
          severity_score: mainPrediction.severity_score * 0.7,
          matching_count: mainPrediction.matching_count
        },
        {
          disease: generateRelatedDisease(mainPrediction.disease, selectedSymptoms.map(s => s.value)),
          confidence: mainPrediction.confidence * 0.6,
          matching_symptoms: mainPrediction.matching_symptoms.slice(0, Math.max(1, mainPrediction.matching_symptoms.length - 2)),
          symptom_coverage: mainPrediction.symptom_coverage * 0.7,
          severity_score: mainPrediction.severity_score * 0.5,
          matching_count: Math.max(1, mainPrediction.matching_count - 1)
        }
      ];
      
      setAlternativeDiseases(alternatives);
      setPrediction(data);
      
      // Get analysis for the main prediction
      fetchAnalysis(selectedSymptoms.map(s => s.value), mainPrediction);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.message || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };
  
  // Function to fetch analysis from Gemini API
  const fetchAnalysis = async (symptoms, prediction) => {
    try {
      setLoadingAnalysis(true);
      const analysisText = await getExplanation(symptoms, prediction);
      setAnalysis(analysisText);
    } catch (err) {
      console.error('Failed to get analysis:', err);
      // Don't set error state, just leave analysis empty
    } finally {
      setLoadingAnalysis(false);
    }
  };

  // Function to generate a related disease based on symptoms and the main disease
  const generateRelatedDisease = (mainDisease, symptoms) => {
    // Common related disease mappings
    const diseaseRelationships = {
      'Fungal infection': ['Dermatitis', 'Eczema'],
      'Allergy': ['Rhinitis', 'Sinusitis', 'Asthma'],
      'GERD': ['Acid Reflux', 'Heartburn'],
      'Chronic cholestasis': ['Biliary Disease', 'Gallstones'],
      'Drug Reaction': ['Skin Allergy', 'Medication Side Effect'],
      'Peptic ulcer disease': ['Gastritis', 'Stomach Inflammation'],
      'AIDS': ['HIV Infection', 'Immunodeficiency'],
      'Diabetes': ['Prediabetes', 'Metabolic Syndrome'],
      'Gastroenteritis': ['Food Poisoning', 'Stomach Flu'],
      'Bronchial Asthma': ['Reactive Airway Disease', 'Chronic Bronchitis'],
      'Hypertension': ['High Blood Pressure', 'Cardiovascular Strain'],
      'Migraine': ['Tension Headache', 'Cluster Headache'],
      'Cervical spondylosis': ['Neck Arthritis', 'Degenerative Disc Disease'],
      'Paralysis (brain hemorrhage)': ['Stroke', 'Cerebral Infarction'],
      'Jaundice': ['Hepatitis', 'Liver Dysfunction'],
      'Malaria': ['Tropical Fever', 'Mosquito-Borne Illness'],
      'Chicken pox': ['Varicella', 'Viral Exanthem'],
      'Dengue': ['Hemorrhagic Fever', 'Arboviral Infection'],
      'Typhoid': ['Enteric Fever', 'Salmonellosis'],
      'Hepatitis A': ['Infectious Hepatitis', 'Viral Liver Disease'],
      'Hepatitis B': ['Viral Hepatitis', 'Chronic Hepatitis'],
      'Hepatitis C': ['Viral Liver Infection', 'Chronic Hepatitis'],
      'Hepatitis D': ['Delta Hepatitis', 'HDV Infection'],
      'Hepatitis E': ['Enteric Hepatitis', 'Waterborne Hepatitis'],
      'Alcoholic hepatitis': ['Alcohol-Induced Liver Disease', 'Toxic Hepatitis'],
      'Tuberculosis': ['TB', 'Pulmonary Infection'],
      'Common Cold': ['Upper Respiratory Infection', 'Viral Rhinitis'],
      'Pneumonia': ['Lung Infection', 'Bronchopneumonia'],
      'Dimorphic hemmorhoids(piles)': ['Hemorrhoids', 'Rectal Varices'],
      'Heart attack': ['Myocardial Infarction', 'Coronary Thrombosis'],
      'Varicose veins': ['Venous Insufficiency', 'Vascular Dilation'],
      'Hypothyroidism': ['Underactive Thyroid', 'Low Thyroid Function'],
      'Hyperthyroidism': ['Overactive Thyroid', 'Thyroid Hyperfunction'],
      'Hypoglycemia': ['Low Blood Sugar', 'Glucose Deficiency'],
      'Osteoarthritis': ['Degenerative Joint Disease', 'Joint Inflammation'],
      'Arthritis': ['Joint Inflammation', 'Rheumatic Disease'],
      'Paroxysmal Positional Vertigo': ['Benign Vertigo', 'Positional Dizziness'],
      'Acne': ['Pimples', 'Skin Inflammation'],
      'Urinary tract infection': ['Bladder Infection', 'Cystitis'],
      'Psoriasis': ['Skin Inflammation', 'Autoimmune Skin Disease'],
      'Impetigo': ['Skin Infection', 'Bacterial Dermatitis']
    };
    
    // Check if we have predefined relationships
    if (diseaseRelationships[mainDisease] && diseaseRelationships[mainDisease].length > 0) {
      // Return a predefined related disease
      return diseaseRelationships[mainDisease][0];
    }
    
    // If no predefined relationship, create a variation
    return `Possible ${mainDisease}`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto pt-20 px-4 space-y-6">
        {/* Welcome Message */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-800">
            Welcome, {localStorage.getItem('username')}
          </h1>
        </div>

        {/* Disease Prediction Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold mb-4">Disease Prediction</h1>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Symptoms
            </label>
            <AsyncSelect
              isMulti
              cacheOptions
              defaultOptions
              loadOptions={loadSymptoms}
              onChange={setSelectedSymptoms}
              value={selectedSymptoms}
              className="mb-4"
            />
            
            <button
              onClick={handlePrediction}
              disabled={loading || selectedSymptoms.length === 0}
              className={`w-full py-3 rounded-lg font-medium transition-all duration-150
                ${loading || selectedSymptoms.length === 0 
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700 transform hover:scale-[1.02] active:scale-[0.98]'
                }
              `}
            >
              {loading ? 'Predicting...' : 'Predict Disease'}
            </button>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}

          {prediction && (
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-4">Prediction Results</h2>
              <p className="text-sm text-gray-500 mb-3">The first prediction is the most accurate based on your symptoms. Additional predictions are alternative possibilities that may be related.</p>
              
              {/* Top 3 Predictions Section */}
              <div className="space-y-4 mb-6">
                {/* Main prediction plus alternative diseases */}
                {[...prediction.predictions.slice(0, 1), ...alternativeDiseases].slice(0, 3).map((pred, index) => {
                  // Determine background color based on prediction rank
                  const bgColorClass = index === 0 
                    ? 'bg-blue-50 border border-blue-200' 
                    : index === 1 
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-yellow-50 border border-yellow-200';
                  
                  // Determine label based on rank
                  const predictionLabel = index === 0 
                    ? 'Most Likely: ' 
                    : index === 1 
                    ? 'Alternative Possibility: '
                    : 'Related Condition: ';
                  
                  return (
                    <div key={index} className={`p-4 rounded-md ${bgColorClass}`}>
                      <div className="flex justify-between items-center">
                        <p className="font-medium text-gray-900">
                          {predictionLabel}
                          {/* Ensure disease is displayed as a string */}
                          {typeof pred.disease === 'string' ? pred.disease : String(pred.disease)}
                        </p>
                        <p className={`text-sm font-medium ${
                          pred.confidence >= 0.5 ? 'text-green-600' :
                          pred.confidence >= 0.3 ? 'text-yellow-600' :
                          'text-gray-500'
                        }`}>
                          {(pred.confidence * 100).toFixed(1)}% confidence
                        </p>
                      </div>
                      {pred.matching_symptoms && pred.matching_symptoms.length > 0 && (
                        <div className="mt-2">
                          <p className="text-sm text-gray-500">Matching symptoms:</p>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {pred.matching_symptoms.map((symptom, i) => (
                              <span key={i} className="text-xs bg-gray-100 px-2 py-1 rounded">
                                {symptom.symptom}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
              
              {/* AI Analysis Section - Moved below the top 3 predictions */}
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
                <h3 className="text-lg font-semibold text-blue-800 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                  Analysis
                </h3>
                {loadingAnalysis ? (
                  <div className="text-sm text-gray-700 italic">Generating analysis...</div>
                ) : analysis ? (
                  <div className="text-sm text-gray-700 whitespace-pre-line">{analysis}</div>
                ) : (
                  <div className="text-sm text-gray-700 italic">
                    No analysis available. Make sure the Google Gemini API key is properly configured.
                  </div>
                )}
              </div>

              <h3 className="text-lg font-semibold mb-3">Recommended Specialists</h3>
              <div className="grid gap-4 md:grid-cols-2">
                {prediction.recommended_doctors.map(doctor => (
                  <DoctorCard key={doctor.id} doctor={doctor} />
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Appointments Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4">My Appointments</h2>
          {error && (
            <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}
          {appointmentsLoading ? (
            <div className="text-center py-4">Loading appointments...</div>
          ) : appointments.length === 0 ? (
            <div className="text-gray-500 text-center py-4">No appointments found</div>
          ) : (
            <div className="space-y-4">
              {appointments.map((appointment) => (
                <div key={appointment.id} className="border rounded-lg p-4 hover:bg-gray-50">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="font-medium">Doctor</p>
                      <p className="text-gray-600">{appointment.doctor.name}</p>
                    </div>
                    <div>
                      <p className="font-medium">Specialization</p>
                      <p className="text-gray-600">{appointment.doctor.specialization}</p>
                    </div>
                    <div>
                      <p className="font-medium">Hospital</p>
                      <p className="text-gray-600">{appointment.doctor.hospital}</p>
                    </div>
                    <div>
                      <p className="font-medium">Status</p>
                      <p className={`font-medium ${
                        appointment.status === 'pending' ? 'text-yellow-600' :
                        appointment.status === 'approved' ? 'text-green-600' :
                        appointment.status === 'rejected' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {appointment.status.toUpperCase()}
                      </p>
                    </div>
                  </div>
                  <div className="mt-3">
                    <p className="font-medium">Message</p>
                    <p className="text-gray-600">{appointment.message}</p>
                  </div>
                  <div className="mt-2 text-sm text-gray-500">
                    Appointment ID: {appointment.id}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
