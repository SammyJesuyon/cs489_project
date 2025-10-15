import React, { useEffect, useState } from 'react';
import { Plus, Search, Edit, Trash2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import type { Patient } from '../types';
import { Toast } from '../components/Toast';
import { Modal } from '../components/Modal';

export const PatientsPage: React.FC = () => {
  const { token } = useAuth();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await api.getPatients(token);
      setPatients(data);
    } catch (error) {
      setToast({ message: 'Failed to load patients', type: 'error' });
        console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!token || !deleteId) return;
    try {
      await api.deletePatient(token, deleteId);
      setToast({ message: 'Patient deleted successfully', type: 'success' });
      fetchPatients();
    } catch (error) {
      setToast({ message: 'Failed to delete patient', type: 'error' });
      console.error(error);
    }
    setShowModal(false);
    setDeleteId(null);
  };

  const filteredPatients = patients.filter(patient =>
    `${patient.first_name} ${patient.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Patients</h1>
        <button className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Patient
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search patients..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">City</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredPatients.map((patient) => (
              <tr key={patient.patient_no} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="font-medium text-gray-900">{`${patient.first_name} ${patient.last_name}`}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600">{patient.email}</td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600">{patient.phone}</td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600">{patient.address?.city || 'N/A'}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  <button className="text-teal-600 hover:text-teal-700 mr-3">
                    <Edit className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => {
                      setDeleteId(patient.patient_no!);
                      setShowModal(true);
                    }}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onConfirm={handleDelete}
        title="Delete Patient"
        message="Are you sure you want to delete this patient? This action cannot be undone."
      />
    </div>
  );
};