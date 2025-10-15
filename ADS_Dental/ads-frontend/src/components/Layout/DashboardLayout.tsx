import React, { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { Sidebar } from './Sidebar';
import { DashboardPage } from '../../pages/DashboardPage';
import { PatientsPage } from '../../pages/PatientsPage';
import { DentistsPage } from '../../pages/DentistsPage';
import { SurgeriesPage } from '../../pages/SurgeriesPage';
import { AppointmentsPage } from '../../pages/AppointmentsPage';
import { AddressesPage } from '../../pages/AddressesPage';

export const DashboardLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const { user, logout } = useAuth();

  if (!user) return null;

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'patients':
        return <PatientsPage />;
      case 'dentists':
        return <DentistsPage />;
      case 'surgeries':
        return <SurgeriesPage />;
      case 'appointments':
        return <AppointmentsPage />;
      case 'addresses':
        return <AddressesPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between p-6 border-b lg:hidden">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-teal-500 rounded-lg flex items-center justify-center">
              <Menu className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-xl text-gray-800">Dental Care</span>
          </div>
          <button onClick={() => setSidebarOpen(false)}>
            <X className="w-6 h-6 text-gray-600" />
          </button>
        </div>
        <Sidebar
          user={user}
          currentPage={currentPage}
          onNavigate={setCurrentPage}
          onLogout={logout}
        />
      </div>

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'lg:ml-64' : ''}`}>
        {/* Top Bar */}
        <div className="bg-white shadow-sm border-b">
          <div className="flex items-center justify-between p-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              <Menu className="w-6 h-6 text-gray-600" />
            </button>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <div className="font-medium text-gray-800">{user.username}</div>
                {/* <div className="text-sm text-gray-500">{user.roles.join(', ')}</div> */}
              </div>
              <div className="w-10 h-10 bg-teal-500 rounded-full flex items-center justify-center">
                <span className="text-white font-medium">{user.username.charAt(0).toUpperCase()}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <div className="p-6">{renderPage()}</div>
      </div>
    </div>
  );
};