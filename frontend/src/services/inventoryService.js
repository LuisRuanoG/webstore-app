import api from './api';

export const createInventory = (inventoryData) =>
    api.post('/inventory/', inventoryData).then((res) => res.data);

export const getAllInventory = (productId) =>
    api.get('/inventory/', { params: { product_id: productId } }).then((res) => res.data);
