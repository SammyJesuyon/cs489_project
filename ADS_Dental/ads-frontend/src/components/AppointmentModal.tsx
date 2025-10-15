import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import type { Appointment, Patient, Dentist, Surgery } from '../types';
import { api } from '../api/apiService';

interface AppointmentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  token: string;
  appointment?: Appointment | null;
  mode: 'create' | 'edit';
}

export const AppointmentModal: React.FC<AppointmentModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  token,
  appointment,
  mode,
}) => {
  const [formData, setFormData] = useState({
    appointment_date: '',
    appointment_time: '',
    status: 'BOOKED' as 'BOOKED' | 'CANCELLED' | 'COMPLETED',
    patient_id: '',
    dentist_id: '',
    surgery_id: '',
  });

  const [patients, setPatients] = useState<Patient[]>([]);
  const [dentists, setDentists] = useState<Dentist[]>([]);
  const [surgeries, setSurgeries] = useState<Surgery[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchData();
      if (appointment && mode === 'edit') {
        setFormData({
          appointment_date: appointment.appointment_date,
          appointment_time: appointment.appointment_time,
          status: appointment.status,
          patient_id: appointment.patient_id?.toString() || '',
          dentist_id: appointment.dentist_id?.toString() || '',
          surgery_id: appointment.surgery_id?.toString() || '',
        });
      } else {
        resetForm();
      }
    }
  }, [isOpen, appointment, mode]);

  const fetchData = async () => {
    try {
      const [patientsData, dentistsData, surgeriesData] = await Promise.all([
        api.getPatients(token),
        api.getDentists(token),
        api.getSurgeries(token),
      ]);
      setPatients(patientsData);
      setDentists(dentistsData);
      setSurgeries(surgeriesData);
    } catch (err) {
      setError('Failed to load data');
        console.error(err);
    }
  };

  const resetForm = () => {
    setFormData({
      appointment_date: '',
      appointment_time: '',
      status: 'BOOKED',
      patient_id: '',
      dentist_id: '',
      surgery_id: '',
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload = {
        appointment_date: formData.appointment_date,
        appointment_time: formData.appointment_time,
        status: formData.status,
        patient_id: parseInt(formData.patient_id),
        dentist_id: parseInt(formData.dentist_id),
        surgery_id: parseInt(formData.surgery_id),
      };

      if (mode === 'create') {
        await api.createAppointment(token, payload as Appointment);
      } else if (appointment?.id) {
        await api.updateAppointment(token, appointment.id, payload);
      }

      onSuccess();
      onClose();
      resetForm();
    } catch (err) {
      setError(`Failed to ${mode} appointment`);
        console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b sticky top-0 bg-white">
          <h2 className="text-2xl font-semibold text-gray-800">
            {mode === 'create' ? 'Book Appointment' : 'Edit Appointment'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date *
              </label>
              <input
                type="date"
                value={formData.appointment_date}
                onChange={(e) =>
                  setFormData({ ...formData, appointment_date: e.target.value })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Time *
              </label>
              <input
                type="time"
                value={formData.appointment_time}
                onChange={(e) =>
                  setFormData({ ...formData, appointment_time: e.target.value })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Patient *
            </label>
            <select
              value={formData.patient_id}
              onChange={(e) =>
                setFormData({ ...formData, patient_id: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              required
            >
              <option value="">Select a patient</option>
              {patients.map((patient) => (
                <option key={patient.patient_no} value={patient.patient_no}>
                  {patient.first_name} {patient.last_name} - {patient.email}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dentist *
            </label>
            <select
              value={formData.dentist_id}
              onChange={(e) =>
                setFormData({ ...formData, dentist_id: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              required
            >
              <option value="">Select a dentist</option>
              {dentists.map((dentist) => (
                <option key={dentist.id} value={dentist.id}>
                  Dr. {dentist.first_name} {dentist.last_name} -{' '}
                  {dentist.specialization}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Surgery *
            </label>
            <select
              value={formData.surgery_id}
              onChange={(e) =>
                setFormData({ ...formData, surgery_id: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              required
            >
              <option value="">Select a surgery</option>
              {surgeries.map((surgery) => (
                <option key={surgery.surgery_no} value={surgery.surgery_no}>
                  {surgery.name} - {surgery.address?.city}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status *
            </label>
            <select
              value={formData.status}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  status: e.target.value as 'BOOKED' | 'CANCELLED' | 'COMPLETED',
                })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              required
            >
              <option value="BOOKED">Booked</option>
              <option value="COMPLETED">Completed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition-colors disabled:bg-gray-400"
            >
              {loading ? 'Saving...' : mode === 'create' ? 'Book Appointment' : 'Update Appointment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};