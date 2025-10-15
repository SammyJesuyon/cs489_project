import React from 'react';
import { useAuth } from './hooks/useAuth';
import { LoginPage } from './pages/LoginPage';
import { DashboardLayout } from './components/Layout/DashboardLayout';

const App: React.FC = () => {
  const { user } = useAuth();

  return user ? <DashboardLayout /> : <LoginPage />;
};

export default App;