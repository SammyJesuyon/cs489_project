import React, { useEffect, useState } from 'react';
import { Plus, MapPin, Edit, Trash2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import type { Surgery } from '../types';

export const SurgeriesPage: React.FC = () => {
  const { token } = useAuth();
  const [surgeries, setSurgeries] = useState<Surgery[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSurgeries = async () => {
      if (!token) return;
      setLoading(true);
      try {
        const data = await api.getSurgeries(token);
        setSurgeries(data);
      } catch (error) {
        console.error('Failed to load surgeries:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSurgeries();
  }, [token]);

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Surgeries</h1>
        <button className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Surgery
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {surgeries.map((surgery) => (
          <div key={surgery.surgery_no} className="bg-white rounded-xl shadow-sm p-6 border">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">{surgery.name}</h3>
                <div className="space-y-1 text-sm text-gray-600">
                  <div className="flex items-center gap-2">
                    <span>📞</span>
                    <span>{surgery.phone}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4" />
                    <span>
                      {surgery.address?.street}, {surgery.address?.city}, {surgery.address?.state} {surgery.address?.zip_code}
                    </span>
                  </div>
                </div>
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
          </div>
        ))}
      </div>
    </div>
  );
};