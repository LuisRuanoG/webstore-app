import api from './api'; // Importamos el cuartel central

// Función para POST un producto nuevo en la base de datos
export const createProduct = (productData) =>
    api.post('/products/', productData).then((res) => res.data);

//funcion para GET todos los productos del backend
export const getAllProducts = () =>
    api.get('/products/').then((res) => res.data);

//funcion para get by id un producto del backend
export const getProductById = (id) =>
    api.get(`/products/${id}/`).then((res) => res.data);

//funcion para patch un producto en la base de datos
export const patchProduct = (id, productData) =>
    api.patch(`/products/${id}/`, productData).then((res) => res.data);
