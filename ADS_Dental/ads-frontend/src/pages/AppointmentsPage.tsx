import React, { useEffect, useState } from 'react';
import { Plus, Calendar, Clock, Edit, Trash2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import type { Appointment } from '../types';
import { Toast } from '../components/Toast';
import { APPOINTMENT_STATUS_COLORS } from '../utils/constants';

export const AppointmentsPage: React.FC = () => {
  const { token, isPatient } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'table' | 'calendar'>('table');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await api.getAppointments(token);
      setAppointments(data);
    } catch (error) {
      setToast({ message: 'Failed to load appointments', type: 'error' });
        console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    return APPOINTMENT_STATUS_COLORS[status as keyof typeof APPOINTMENT_STATUS_COLORS] || 'bg-gray-100 text-gray-700';
  };

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Appointments</h1>
        <div className="flex gap-3">
          <div className="bg-white border rounded-lg p-1 flex gap-1">
            <button
              onClick={() => setViewMode('table')}
              className={`px-4 py-2 rounded ${viewMode === 'table' ? 'bg-teal-500 text-white' : 'text-gray-600'}`}
            >
              Table
            </button>
            <button
              onClick={() => setViewMode('calendar')}
              className={`px-4 py-2 rounded ${viewMode === 'calendar' ? 'bg-teal-500 text-white' : 'text-gray-600'}`}
            >
              Calendar
            </button>
          </div>
          {isPatient && (
            <button className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Book Appointment
            </button>
          )}
        </div>
      </div>

      {viewMode === 'table' ? (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date & Time</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Patient</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Dentist</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Surgery</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {appointments.map((apt) => (
                <tr key={apt.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-2 text-gray-900">
                      <Clock className="w-4 h-4 text-gray-400" />
                      <div>
                        <div className="font-medium">{apt.appointment_date}</div>
                        <div className="text-sm text-gray-500">{apt.appointment_time}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-gray-900">{apt.patient ? `${apt.patient.first_name} ${apt.patient.last_name}` : 'N/A'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-gray-900">Dr. {apt.dentist ? `${apt.dentist.first_name} ${apt.dentist.last_name}` : 'N/A'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                    {apt.surgery?.name || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(apt.status)}`}>
                      {apt.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button className="text-teal-600 hover:text-teal-700 mr-3">
                      <Edit className="w-5 h-5" />
                    </button>
                    <button className="text-red-600 hover:text-red-700">
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <div className="text-center text-gray-600 py-12">
            <Calendar className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p>Calendar view coming soon</p>
          </div>
        </div>
      )}

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
};