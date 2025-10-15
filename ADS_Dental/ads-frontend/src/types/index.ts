export interface Address {
  id?: number;
  street: string;
  city: string;
  state: string;
  zip_code: string;
}

export interface Patient {
  patient_no?: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address?: Address;
  address_id?: number;
}

export interface Surgery {
  surgery_no?: number;
  name: string;
  phone: string;
  address?: Address;
  address_id?: number;
}

export interface Dentist {
  id?: number;
  first_name: string;
  last_name: string;
  email: string;
  specialization: string;
  surgery?: Surgery;
  surgery_id?: number;
}

export interface Appointment {
  id?: number;
  appointment_date: string;
  appointment_time: string;
  status: 'BOOKED' | 'CANCELLED' | 'COMPLETED';
  patient?: Patient;
  patient_id?: number;
  dentist?: Dentist;
  dentist_id?: number;
  surgery?: Surgery;
  surgery_id?: number;
}

export interface User {
  id?: number;
  username: string;
  email: string;
  roles: string[];
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, role: string) => Promise<void>;
  logout: () => void;
  isAdmin: boolean;
  isDentist: boolean;
  isPatient: boolean;
}

export interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'info';
  onClose: () => void;
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
}