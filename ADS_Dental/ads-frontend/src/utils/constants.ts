export const NAVIGATION_ITEMS = [
  { name: 'Dashboard', id: 'dashboard', roles: ['ADMIN', 'DENTIST', 'PATIENT'] },
  { name: 'Patients', id: 'patients', roles: ['ADMIN'] },
  { name: 'Dentists', id: 'dentists', roles: ['ADMIN'] },
  { name: 'Surgeries', id: 'surgeries', roles: ['ADMIN', 'DENTIST'] },
  { name: 'Appointments', id: 'appointments', roles: ['ADMIN', 'DENTIST', 'PATIENT'] },
  { name: 'Addresses', id: 'addresses', roles: ['ADMIN'] },
];

export const APPOINTMENT_STATUS_COLORS = {
  BOOKED: 'bg-blue-100 text-blue-700',
  COMPLETED: 'bg-green-100 text-green-700',
  CANCELLED: 'bg-red-100 text-red-700',
};