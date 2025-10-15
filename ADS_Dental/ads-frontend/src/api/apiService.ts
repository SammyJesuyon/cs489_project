import type { Patient, Dentist, Surgery, Appointment, Address } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private getHeaders(token?: string): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  async login(username: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });

    if (!response.ok) throw new Error('Login failed');
    return response.json();
  }

  async register(username: string, email: string, password: string, role: string) {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ username, email, password, role }),
    });

    if (!response.ok) throw new Error('Registration failed');
    return response.json();
  }

  // Patients
  async getPatients(token: string): Promise<Patient[]> {
    const response = await fetch(`${API_URL}/patients`, {
      headers: this.getHeaders(token),
    });
    if (!response.ok) throw new Error('Failed to fetch patients');
    return response.json();
  }

  async createPatient(token: string, data: Patient): Promise<Patient> {
    const response = await fetch(`${API_URL}/patients`, {
      method: 'POST',
      headers: this.getHeaders(token),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create patient');
    return response.json();
  }

  async updatePatient(token: string, id: number, data: Patient): Promise<Patient> {
    const response = await fetch(`${API_URL}/patients/${id}`, {
      method: 'PUT',
      headers: this.getHeaders(token),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update patient');
    return response.json();
  }

  async deletePatient(token: string, id: number): Promise<void> {
    const response = await fetch(`${API_URL}/patients/${id}`, {
      method: 'DELETE',
      headers: this.getHeaders(token),
    });
    if (!response.ok) throw new Error('Failed to delete patient');
  }

  // Dentists
  async getDentists(token: string): Promise<Dentist[]> {
    const response = await fetch(`${API_URL}/dentists`, {
      headers: this.getHeaders(token),
    });
    if (!response.ok) throw new Error('Failed to fetch dentists');
    return response.json();
  }

  // Surgeries
  async getSurgeries(token: string): Promise<Surgery[]> {
    const response = await fetch(`${API_URL}/surgeries`, {
      headers: this.getHeaders(token),
    });
    if (!response.ok) throw new Error('Failed to fetch surgeries');
    return response.json();
  }

  // Appointments
  async getAppointments(token: string): Promise<Appointment[]> {
    const response = await fetch(`${API_URL}/appointments`, {
      headers: this.getHeaders(token),
    });
    if (!response.ok) throw new Error('Failed to fetch appointments');
    return response.json();
  }

  async createAppointment(token: string, data: Appointment): Promise<Appointment> {
    const response = await fetch(`${API_URL}/appointments`, {
      method: 'POST',
      headers: this.getHeaders(token),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create appointment');
    return response.json();
  }

  async updateAppointment(token: string, id: number, data: Partial<Appointment>): Promise<Appointment> {
    const response = await fetch(`${API_URL}/appointments/${id}`, {
      method: 'PUT',
      headers: this.getHeaders(token),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update appointment');
    return response.json();
  }

  // Addresses
  async getAddresses(token: string): Promise<Address[]> {
    const response = await fetch(`${API_URL}/addresses`, {
      headers: this.getHeaders(token),
    });
    if (!response.ok) throw new Error('Failed to fetch addresses');
    return response.json();
  }
}

export const api = new ApiService();