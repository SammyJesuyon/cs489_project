import React, { useEffect, useState } from 'react';
import { Plus, UserCog, Edit, Trash2, Building2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import type { Dentist } from '../types';

export const DentistsPage: React.FC = () => {
  const { token } = useAuth();
  const [dentists, setDentists] = useState<Dentist[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDentists = async () => {
      if (!token) return;
      setLoading(true);
      try {
        const data = await api.getDentists(token);
        setDentists(data);
      } catch (error) {
        console.error('Failed to load dentists:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDentists();
  }, [token]);

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Dentists</h1>
        <button className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Dentist
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {dentists.map((dentist) => (
          <div key={dentist.id} className="bg-white rounded-xl shadow-sm p-6 border hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center">
                <UserCog className="w-6 h-6 text-teal-600" />
              </div>
              <div className="flex gap-2">
                <button className="text-teal-600 hover:text-teal-700">
                  <Edit className="w-5 h-5" />
                </button>
                <button className="text-red-600 hover:text-red-700">
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-1">
              Dr. {dentist.first_name} {dentist.last_name}
            </h3>
            <p className="text-teal-600 text-sm mb-3">{dentist.specialization}</p>
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <Building2 className="w-4 h-4" />
                <span>{dentist.surgery?.name || 'Not assigned'}</span>
              </div>
              <div className="flex items-center gap-2">
                <span>📧</span>
                <span className="truncate">{dentist.email}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};