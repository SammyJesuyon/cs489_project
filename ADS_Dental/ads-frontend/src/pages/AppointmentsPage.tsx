import React, { useEffect, useState } from 'react';
import { Plus, Calendar, Clock, Edit, Trash2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import type { Appointment } from '../types';
import { Toast } from '../components/Toast';
import { Modal } from '../components/Modal';
import { AppointmentModal } from '../components/AppointmentModal';
import { APPOINTMENT_STATUS_COLORS } from '../utils/constants';

export const AppointmentsPage: React.FC = () => {
  const { token, isPatient, isAdmin, isDentist } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'table' | 'calendar'>('table');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);
  
  // Modal states
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showAppointmentModal, setShowAppointmentModal] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [editAppointment, setEditAppointment] = useState<Appointment | null>(null);
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');

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

  const handleDelete = async () => {
    if (!token || !deleteId) return;
    try {
      await api.deleteAppointment(token, deleteId);
      setToast({ message: 'Appointment deleted successfully', type: 'success' });
      fetchAppointments();
    } catch (error) {
      setToast({ message: 'Failed to delete appointment', type: 'error' });
        console.error(error);
    }
    setShowDeleteModal(false);
    setDeleteId(null);
  };

  const handleEdit = (appointment: Appointment) => {
    setEditAppointment(appointment);
    setModalMode('edit');
    setShowAppointmentModal(true);
  };

  const handleCreate = () => {
    setEditAppointment(null);
    setModalMode('create');
    setShowAppointmentModal(true);
  };

  const handleAppointmentSuccess = () => {
    setToast({
      message: `Appointment ${modalMode === 'create' ? 'created' : 'updated'} successfully`,
      type: 'success',
    });
    fetchAppointments();
  };

  const handleStatusUpdate = async (appointmentId: number, newStatus: 'COMPLETED' | 'CANCELLED') => {
    if (!token) return;
    try {
      await api.updateAppointment(token, appointmentId, { status: newStatus });
      setToast({ message: `Appointment marked as ${newStatus.toLowerCase()}`, type: 'success' });
      fetchAppointments();
    } catch (error) {
      setToast({ message: 'Failed to update appointment status', type: 'error' });
        console.error(error);
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
          {(isPatient || isAdmin) && (
            <button
              onClick={handleCreate}
              className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Book Appointment
            </button>
          )}
        </div>
      </div>

      {viewMode === 'table' ? (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <div className="overflow-x-auto">
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
                      <div className="text-gray-900">
                        {apt.patient ? `${apt.patient.first_name} ${apt.patient.last_name}` : 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-gray-900">
                        {apt.dentist ? `Dr. ${apt.dentist.first_name} ${apt.dentist.last_name}` : 'N/A'}
                      </div>
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
                      <div className="flex justify-end gap-2">
                        {apt.status === 'BOOKED' && isDentist && (
                          <>
                            <button
                              onClick={() => handleStatusUpdate(apt.id!, 'COMPLETED')}
                              className="text-green-600 hover:text-green-700 text-xs px-2 py-1 border border-green-600 rounded"
                              title="Mark as Completed"
                            >
                              Complete
                            </button>
                            <button
                              onClick={() => handleStatusUpdate(apt.id!, 'CANCELLED')}
                              className="text-red-600 hover:text-red-700 text-xs px-2 py-1 border border-red-600 rounded"
                              title="Cancel"
                            >
                              Cancel
                            </button>
                          </>
                        )}
                        {(isAdmin || (isPatient && apt.status === 'BOOKED')) && (
                          <>
                            <button
                              onClick={() => handleEdit(apt)}
                              className="text-teal-600 hover:text-teal-700"
                              title="Edit"
                            >
                              <Edit className="w-5 h-5" />
                            </button>
                            <button
                              onClick={() => {
                                setDeleteId(apt.id!);
                                setShowDeleteModal(true);
                              }}
                              className="text-red-600 hover:text-red-700"
                              title="Delete"
                            >
                              <Trash2 className="w-5 h-5" />
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
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
      
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDelete}
        title="Delete Appointment"
        message="Are you sure you want to delete this appointment? This action cannot be undone."
      />

      {token && (
        <AppointmentModal
          isOpen={showAppointmentModal}
          onClose={() => setShowAppointmentModal(false)}
          onSuccess={handleAppointmentSuccess}
          token={token}
          appointment={editAppointment}
          mode={modalMode}
        />
      )}
    </div>
  );
};