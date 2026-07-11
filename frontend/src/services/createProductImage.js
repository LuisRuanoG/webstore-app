import api from './api';

export const createProductImage = (productId, imageData) =>
    api.post(`/products/${productId}/images`, imageData).then((res) => res.data);

export const updateProductImage = (imageId, imageData) =>
    api.patch(`/product-images/${imageId}`, imageData).then((res) => res.data);

export const deleteProductImage = (imageId) =>
    api.delete(`/product-images/${imageId}`).then((res) => res.data);