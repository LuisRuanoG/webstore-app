import api from './api';

// Crear un empleado nuevo
export const createStaff = (staffData) =>
    api.post('/staff/', staffData).then((res) => res.data);

// Traer todos los empleados
export const getAllStaff = () =>
    api.get('/staff/').then((res) => res.data);

// Traer un empleado por id
export const getStaffById = (id) =>
    api.get(`/staff/${id}/`).then((res) => res.data);

// Actualizar un empleado (parcial)
export const updateStaff = (id, staffData) =>
    api.patch(`/staff/${id}/`, staffData).then((res) => res.data);