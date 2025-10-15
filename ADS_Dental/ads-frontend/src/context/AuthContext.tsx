import React, { useState, useEffect } from 'react';
import type { User } from '../types';
import { api } from '../api/apiService';
import { AuthContext } from './AuthContextInstance';


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = async (username: string, password: string) => {
    const data = await api.login(username, password);
    setToken(data.access_token);
    const userData: User = {
      username,
      email: username,
      roles: data.roles || ['PATIENT'],
    };
    setUser(userData);
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const register = async (username: string, email: string, password: string, role: string) => {
    await api.register(username, email, password, role);
    await login(username, password);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const isAdmin = user?.roles.includes('ADMIN') || false;
  const isDentist = user?.roles.includes('DENTIST') || false;
  const isPatient = user?.roles.includes('PATIENT') || false;

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isAdmin, isDentist, isPatient }}>
      {children}
    </AuthContext.Provider>
  );
};