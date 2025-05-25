import React, { useState, useEffect } from 'react';
import Navbar from "./Navbar";
import AsyncSelect from 'react-select/async';
import DoctorCard from './DoctorCard';

const Home = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadSymptoms = async (inputValue) => {
    try {
      const response = await fetch('http://localhost:8000/api/symptoms');
      const data = await response.json();
      
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
      return [];
    }
  };

  const handlePrediction = async () => {
    try {
      setLoading(true);
      setError('');
      
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
        throw new Error('Prediction failed');
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError('Failed to get prediction');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto pt-20 px-4">
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
              className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 
                        disabled:bg-gray-400 disabled:cursor-not-allowed"
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
              <div className="bg-blue-50 p-4 rounded-md mb-6">
                <p className="font-medium">Predicted Disease: {prediction.disease}</p>
                <p className="text-sm text-gray-600">
                  Confidence: {(prediction.confidence * 100).toFixed(2)}%
                </p>
              </div>

              <h3 className="text-lg font-semibold mb-3">Recommended Doctors</h3>
              <div className="grid gap-4 md:grid-cols-2">
                {prediction.recommended_doctors.map(doctor => (
                  <DoctorCard key={doctor.id} doctor={doctor} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
