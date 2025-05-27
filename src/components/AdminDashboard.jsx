import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalDoctors: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is logged in as admin
    const isAdmin = localStorage.getItem('isAdmin') === 'true';
    if (!isAdmin) {
      navigate('/admin');
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        // Fetch doctors
        const doctorsResponse = await fetch('http://localhost:8000/api/admin/doctors');
        if (!doctorsResponse.ok) throw new Error('Failed to fetch doctors');
        const doctorsData = await doctorsResponse.json();
        console.log('Doctors data:', doctorsData);
        setDoctors(doctorsData);

        // Fetch users
        const usersResponse = await fetch('http://localhost:8000/api/admin/users');
        if (!usersResponse.ok) throw new Error('Failed to fetch users');
        const usersData = await usersResponse.json();
        console.log('Users data:', usersData);
        setUsers(usersData);

        // Fetch stats
        const statsResponse = await fetch('http://localhost:8000/api/admin/stats');
        if (!statsResponse.ok) throw new Error('Failed to fetch stats');
        const statsData = await statsResponse.json();
        console.log('Stats data:', statsData);
        setStats(statsData);

        // Fetch messages
        const messagesResponse = await fetch('http://localhost:8000/api/admin/messages');
        if (!messagesResponse.ok) throw new Error('Failed to fetch messages');
        const messagesData = await messagesResponse.json();
        setMessages(messagesData);

        // Fetch appointments
        const appointmentsResponse = await fetch('http://localhost:8000/api/admin/appointments');
        if (!appointmentsResponse.ok) throw new Error('Failed to fetch appointments');
        const appointmentsData = await appointmentsResponse.json();
        setAppointments(appointmentsData);

      } catch (err) {
        console.error('Dashboard error:', err);
        setError('Failed to load dashboard data: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  // Add doctor handler
  const handleAddDoctor = async () => {
    // Implementation for adding a new doctor
  };

  // Delete doctor handler
  const handleDeleteDoctor = async (doctorId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/admin/doctors/${doctorId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setDoctors(doctors.filter(doctor => doctor.id !== doctorId));
      } else {
        throw new Error('Failed to delete doctor');
      }
    } catch (err) {
      setError('Failed to delete doctor: ' + err.message);
    }
  };

  // Delete message handler
  const handleDeleteMessage = async (messageId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/admin/messages/${messageId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setMessages(messages.filter(message => message.id !== messageId));
      } else {
        throw new Error('Failed to delete message');
      }
    } catch (err) {
      setError('Failed to delete message: ' + err.message);
    }
  };

  const handleAppointmentStatus = async (appointmentId, newStatus) => {
    try {
      const response = await fetch(`http://localhost:8000/api/admin/appointments/${appointmentId}?status=${newStatus}`, {
        method: 'PUT'
      });

      if (response.ok) {
        setAppointments(appointments.map(appointment => 
          appointment.id === appointmentId 
            ? { ...appointment, status: newStatus }
            : appointment
        ));
      } else {
        throw new Error('Failed to update appointment status');
      }
    } catch (err) {
      setError('Failed to update appointment status: ' + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>

        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-4">Loading...</div>
        ) : (
          <>
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-semibold text-gray-700">Total Users</h3>
                <p className="text-3xl font-bold text-blue-600">{stats.totalUsers}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-semibold text-gray-700">Total Doctors</h3>
                <p className="text-3xl font-bold text-blue-600">{stats.totalDoctors}</p>
              </div>
            </div>

            {/* Appointments Section */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Appointment Requests</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Patient</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Doctor</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {appointments.length === 0 ? (
                      <tr>
                        <td colSpan="6" className="px-6 py-4 text-center text-gray-500">
                          No appointment requests found
                        </td>
                      </tr>
                    ) : (
                      appointments.map(appointment => (
                        <tr key={appointment.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {new Date(appointment.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4">
                            <div className="text-sm">
                              <p className="font-medium text-gray-900">{appointment.user.full_name}</p>
                              <p className="text-gray-500">{appointment.user.email}</p>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {appointment.doctor ? (
                              <div className="text-sm">
                                <p className="font-medium text-gray-900">{appointment.doctor.name}</p>
                                <p className="text-gray-500">{appointment.doctor.specialization}</p>
                              </div>
                            ) : (
                              'Unknown Doctor'
                            )}
                          </td>
                          <td className="px-6 py-4">
                            <p className="text-gray-900">{appointment.message}</p>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              appointment.status === 'approved' ? 'bg-green-100 text-green-800' :
                              appointment.status === 'rejected' ? 'bg-red-100 text-red-800' :
                              'bg-yellow-100 text-yellow-800'
                            }`}>
                              {appointment.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                            {appointment.status === 'pending' && (
                              <>
                                <button
                                  onClick={() => handleAppointmentStatus(appointment.id, 'approved')}
                                  className="text-green-600 hover:text-green-900"
                                >
                                  Approve
                                </button>
                                <button
                                  onClick={() => handleAppointmentStatus(appointment.id, 'rejected')}
                                  className="text-red-600 hover:text-red-900"
                                >
                                  Reject
                                </button>
                              </>
                            )}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Messages Section */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">User Messages</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {messages.length === 0 ? (
                      <tr>
                        <td colSpan="3" className="px-6 py-4 text-center text-gray-500">
                          No messages found
                        </td>
                      </tr>
                    ) : (
                      messages.map(message => (
                        <tr key={message.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {new Date(message.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4">
                            <p className="text-gray-900">{message.message}</p>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <button
                              onClick={() => handleDeleteMessage(message.id)}
                              className="text-red-600 hover:text-red-800"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Doctors Management */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-900">Doctors Management</h2>
                <button 
                  onClick={handleAddDoctor}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Add New Doctor
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Specialization</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hospital</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rating</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {doctors.length === 0 ? (
                      <tr>
                        <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                          No doctors found
                        </td>
                      </tr>
                    ) : (
                      doctors.map(doctor => (
                        <tr key={doctor.id}>
                          <td className="px-6 py-4 whitespace-nowrap">{doctor.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{doctor.specialization}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{doctor.hospital}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{doctor.rating}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <button className="text-blue-600 hover:text-blue-800 mr-3">Edit</button>
                            <button 
                              onClick={() => handleDeleteDoctor(doctor.id)}
                              className="text-red-600 hover:text-red-800"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Users List */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Registered Users</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gender</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Joined Date</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {users.length === 0 ? (
                      <tr>
                        <td colSpan="4" className="px-6 py-4 text-center text-gray-500">
                          No users found
                        </td>
                      </tr>
                    ) : (
                      users.map(user => (
                        <tr key={user.id}>
                          <td className="px-6 py-4 whitespace-nowrap">{user.username}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{user.email}</td>
                          <td className="px-6 py-4 whitespace-nowrap">{user.gender}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {new Date(user.created_at).toLocaleDateString()}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard; 