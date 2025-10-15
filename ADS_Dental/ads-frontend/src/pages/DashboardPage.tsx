import React, { useEffect, useState } from 'react';
import { Users, UserCog, Calendar, Building2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';

export const DashboardPage: React.FC = () => {
  const { isAdmin, isDentist, isPatient, token } = useAuth();
  const [stats, setStats] = useState({
    patients: 0,
    dentists: 0,
    appointments: 0,
    surgeries: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      if (!token) return;
      try {
        const [patients, dentists, appointments, surgeries] = await Promise.all([
          api.getPatients(token),
          api.getDentists(token),
          api.getAppointments(token),
          api.getSurgeries(token),
        ]);
        setStats({
          patients: patients.length,
          dentists: dentists.length,
          appointments: appointments.length,
          surgeries: surgeries.length,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    };
    fetchStats();
  }, [token]);

  const adminCards = [
    { title: 'Total Patients', value: stats.patients, icon: Users, color: 'bg-blue-500' },
    { title: 'Total Dentists', value: stats.dentists, icon: UserCog, color: 'bg-teal-500' },
    { title: 'Appointments', value: stats.appointments, icon: Calendar, color: 'bg-purple-500' },
    { title: 'Surgeries', value: stats.surgeries, icon: Building2, color: 'bg-orange-500' },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {isAdmin && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {adminCards.map((card) => {
            const Icon = card.icon;
            return (
              <div key={card.title} className="bg-white rounded-xl shadow-sm p-6 border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm mb-1">{card.title}</p>
                    <p className="text-3xl font-bold text-gray-800">{card.value}</p>
                  </div>
                  <div className={`${card.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {isDentist && (
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Appointments</h2>
          <p className="text-gray-600">View and manage your scheduled appointments.</p>
        </div>
      )}

      {isPatient && (
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Welcome Back!</h2>
          <p className="text-gray-600 mb-4">Book a new appointment or view your upcoming visits.</p>
          <button className="bg-teal-500 text-white px-6 py-2 rounded-lg hover:bg-teal-600">
            Book Appointment
          </button>
        </div>
      )}
    </div>
  );
};