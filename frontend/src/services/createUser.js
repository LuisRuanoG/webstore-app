import api from './api'; // Importamos el cuartel central

// Función para guardar un usuario nuevo en la base de datos
export const createUser = (userData) =>
    api.post('/users/', userData).then((res) => res.data);

//Función para traer todos los usuarios del backend
export const getAllUsers = () =>
    api.get('/users/').then((res) => res.data);