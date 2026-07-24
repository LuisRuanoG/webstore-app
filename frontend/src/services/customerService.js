import api from './api';

export const createCustomer = (customerData) =>
    api.post('/customers/', customerData).then((res) => res.data);

export const getAllCustomers = () =>
    api.get('/customers/').then((res) => res.data);

export const getCustomerById = (id) =>
    api.get(`/customers/${id}/`).then((res) => res.data);

export const updateCustomer = (id, customerData) =>
    api.patch(`/customers/${id}/`, customerData).then((res) => res.data);
