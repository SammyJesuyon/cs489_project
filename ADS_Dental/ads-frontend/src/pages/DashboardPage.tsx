import React, { useEffect, useState } from 'react';
import { Users, UserCog, Calendar, Building2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import { AppointmentModal } from '../components/AppointmentModal';
import { Toast } from '../components/Toast';

export const DashboardPage: React.FC = () => {
  const { isAdmin, isDentist, isPatient, token } = useAuth();
  const [stats, setStats] = useState({
    patients: 0,
    dentists: 0,
    appointments: 0,
    surgeries: 0,
  });

  const [showAppointmentModal, setShowAppointmentModal] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

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

  const handleAppointmentSuccess = () => {
    setToast({ message: 'Appointment booked successfully', type: 'success' });
    // Refresh stats
    if (token) {
      api.getAppointments(token).then((appointments) => {
        setStats((prev) => ({ ...prev, appointments: appointments.length }));
      });
    }
  };

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
          <p className="text-gray-600 mb-4">View and manage your scheduled appointments.</p>
          <div className="bg-teal-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Appointments</p>
                <p className="text-2xl font-bold text-teal-600">{stats.appointments}</p>
              </div>
              <Calendar className="w-10 h-10 text-teal-500" />
            </div>
          </div>
        </div>
      )}

      {isPatient && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Welcome Back!</h2>
            <p className="text-gray-600 mb-4">Book a new appointment or view your upcoming visits.</p>
            <button
              onClick={() => setShowAppointmentModal(true)}
              className="bg-teal-500 text-white px-6 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2"
            >
              <Calendar className="w-5 h-5" />
              Book Appointment
            </button>
          </div>

          <div className="bg-gradient-to-br from-teal-500 to-blue-500 rounded-xl shadow-sm p-6 text-white">
            <h3 className="text-lg font-semibold mb-2">Your Appointments</h3>
            <p className="text-3xl font-bold">{stats.appointments}</p>
            <p className="text-sm mt-2 opacity-90">Total appointments booked</p>
          </div>
        </div>
      )}

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}

      {token && (
        <AppointmentModal
          isOpen={showAppointmentModal}
          onClose={() => setShowAppointmentModal(false)}
          onSuccess={handleAppointmentSuccess}
          token={token}
          appointment={null}
          mode="create"
        />
      )}
    </div>
  );
};