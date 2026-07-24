import api from './api';

export const createOrderItem = (orderId, itemData) =>
    api.post(`/orders/${orderId}/items`, itemData).then((res) => res.data);
