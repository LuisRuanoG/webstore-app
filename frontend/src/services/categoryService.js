import api from './api'; // Importamos el cuartel central

// Función para guardar una categoría nueva en la base de datos
export const createCategory = (name) =>
    api.post('/categories/', {name}).then((res) => res.data);

//Función para traer todas las categorías del backend
export const getAllCategories = () =>
    api.get('/categories/').then((res) => res.data);

//Función para patch una categoría en la base de datos
export const updateCategory = (id, name) =>
    api.patch(`/categories/${id}/`, {name}).then((res) => res.data);



