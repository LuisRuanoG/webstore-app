import api from './api';

export const createOrder = (orderData) =>
    api.post('/orders/', orderData).then((res) => res.data);

export const getAllOrders = () =>
    api.get('/orders/').then((res) => res.data);

export const getOrderById = (id) =>
    api.get(`/orders/${id}/`).then((res) => res.data);

export const updateOrder = (id, orderData) =>
    api.patch(`/orders/${id}/`, orderData).then((res) => res.data);
