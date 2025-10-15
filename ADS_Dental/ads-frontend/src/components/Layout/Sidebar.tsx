import React from 'react';
import { Users, UserCog, Building2, MapPin, Calendar, LogOut } from 'lucide-react';
import type { User } from '../../types';

interface SidebarProps {
  user: User;
  currentPage: string;
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ user, currentPage, onNavigate, onLogout }) => {
  const navigation = [
    { name: 'Dashboard', icon: Users, id: 'dashboard', roles: ['ADMIN', 'DENTIST', 'PATIENT'] },
    { name: 'Patients', icon: Users, id: 'patients', roles: ['ADMIN'] },
    { name: 'Dentists', icon: UserCog, id: 'dentists', roles: ['ADMIN'] },
    { name: 'Surgeries', icon: Building2, id: 'surgeries', roles: ['ADMIN', 'DENTIST'] },
    { name: 'Appointments', icon: Calendar, id: 'appointments', roles: ['ADMIN', 'DENTIST', 'PATIENT'] },
    { name: 'Addresses', icon: MapPin, id: 'addresses', roles: ['ADMIN'] },
  ];

  const filteredNav = navigation.filter(item =>
    item.roles.some(role => user?.roles.includes(role))
  );

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 p-6 border-b">
        <div className="w-10 h-10 bg-teal-500 rounded-lg flex items-center justify-center">
          <Users className="w-6 h-6 text-white" />
        </div>
        <span className="font-bold text-xl text-gray-800">Dental Care</span>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {filteredNav.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentPage === item.id
                  ? 'bg-teal-50 text-teal-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t">
        <button
          onClick={onLogout}
          className="w-full flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5" />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </div>
  );
};