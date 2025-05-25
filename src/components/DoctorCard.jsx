import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DoctorCard = ({ doctor }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleBookAppointment = () => {
    navigate('/book-appointment', { state: { doctor } });
  };

  return (
    <>
      <div 
        onClick={openModal}
        className="border rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer bg-white"
      >
        <h4 className="font-medium text-lg">{doctor.name}</h4>
        <p className="text-sm text-gray-600">{doctor.specialization}</p>
        <p className="text-sm text-gray-600">{doctor.hospital}</p>
        <div className="mt-2 text-sm">
          <p>Experience: {doctor.experience} years</p>
          <div className="flex items-center mt-1">
            <span className="text-yellow-500">★</span>
            <span className="ml-1">{doctor.rating}/5</span>
          </div>
        </div>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold">{doctor.name}</h3>
              <button
                onClick={closeModal}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-3">
              <div>
                <h4 className="font-medium">Specialization</h4>
                <p className="text-gray-600">{doctor.specialization}</p>
              </div>
              
              <div>
                <h4 className="font-medium">Hospital</h4>
                <p className="text-gray-600">{doctor.hospital}</p>
              </div>
              
              <div>
                <h4 className="font-medium">Experience</h4>
                <p className="text-gray-600">{doctor.experience} years</p>
              </div>
              
              <div>
                <h4 className="font-medium">Rating</h4>
                <div className="flex items-center">
                  {[...Array(5)].map((_, index) => (
                    <span
                      key={index}
                      className={`text-xl ${
                        index < Math.floor(doctor.rating)
                          ? 'text-yellow-500'
                          : 'text-gray-300'
                      }`}
                    >
                      ★
                    </span>
                  ))}
                  <span className="ml-2 text-gray-600">({doctor.rating}/5)</span>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium">Contact</h4>
                <p className="text-gray-600">{doctor.contact}</p>
                <p className="text-gray-600">{doctor.email}</p>
              </div>

              <button
                className="w-full mt-4 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
                onClick={() => {
                  closeModal();
                  handleBookAppointment();
                }}
              >
                Book Appointment
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DoctorCard; 