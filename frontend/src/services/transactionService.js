import api from './api';

export const getAllTransactions = (orderId) =>
    api.get(`/orders/${orderId}/transactions`).then((res) => res.data);

export const getTransactionById = (id) =>
    api.get(`/transactions/${id}`).then((res) => res.data);
