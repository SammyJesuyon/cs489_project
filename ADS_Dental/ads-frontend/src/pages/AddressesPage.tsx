import React, { useEffect, useState } from 'react';
import { Plus, MapPin, Edit, Trash2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/apiService';
import type { Address } from '../types';

export const AddressesPage: React.FC = () => {
  const { token } = useAuth();
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'city' | 'state'>('city');

  useEffect(() => {
    const fetchAddresses = async () => {
      if (!token) return;
      setLoading(true);
      try {
        const data = await api.getAddresses(token);
        setAddresses(data);
      } catch (error) {
        console.error('Failed to load addresses:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAddresses();
  }, [token]);

  const sortedAddresses = [...addresses].sort((a, b) => {
    if (sortBy === 'city') {
      return a.city.localeCompare(b.city);
    }
    return a.state.localeCompare(b.state);
  });

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Addresses</h1>
        <div className="flex items-center gap-3">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'city' | 'state')}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          >
            <option value="city">Sort by City</option>
            <option value="state">Sort by State</option>
          </select>
          <button className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 flex items-center gap-2">
            <Plus className="w-5 h-5" />
            Add Address
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedAddresses.map((address) => (
          <div key={address.id} className="bg-white rounded-xl shadow-sm p-6 border hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center">
                <MapPin className="w-5 h-5 text-teal-600" />
              </div>
              <div className="flex gap-2">
                <button className="text-teal-600 hover:text-teal-700">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="text-red-600 hover:text-red-700">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="space-y-1 text-sm text-gray-600">
              <p className="font-medium text-gray-800">{address.street}</p>
              <p>{address.city}, {address.state}</p>
              <p>{address.zip_code}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};