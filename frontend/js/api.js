const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/items';

// Obtener todos los objetos 3D pertenecientes a un espacio
export async function fetchItemsBySpace(spaceId) {
    try {
        const response = await fetch(`${API_BASE_URL}/space/${spaceId}`);
        if (!response.ok) throw new Error('Error al obtener ítems del espacio');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return [];
    }
}

// Crear un nuevo objeto 3D en la base de datos (POST)
export async function createSpatialItem(itemData) {
    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(itemData)
        });
        if (!response.ok) throw new Error('Error al guardar el objeto');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Actualizar posición, rotación o escala de un objeto existente (PUT)
export async function updateSpatialItem(itemId, itemData) {
    try {
        const response = await fetch(`${API_BASE_URL}/${itemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(itemData)
        });
        if (!response.ok) throw new Error('Error al actualizar el objeto');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Eliminar un objeto 3D por su ID (DELETE)
export async function deleteSpatialItem(itemId) {
    try {
        const response = await fetch(`${API_BASE_URL}/${itemId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Error al eliminar el objeto');
        if (response.status === 204) return;
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}