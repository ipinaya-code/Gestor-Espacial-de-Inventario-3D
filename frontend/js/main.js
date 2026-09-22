import * as THREE from 'three';
import { SpatialScene } from './scene.js';
import { createItemMesh } from './components/item3d.js';
import { 
    createSpatialItem, 
    updateSpatialItem, 
    deleteSpatialItem 
} from './api.js';

const spaceId = 'almacen_principal';
const savedTheme = localStorage.getItem('spatial-theme');
if (savedTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
}

const spatialScene = new SpatialScene('webgl-canvas');
spatialScene.render();

// Manejo del Theme Switcher
const themeToggleBtn = document.getElementById('theme-toggle-btn');
const themeText = document.getElementById('theme-text');

function applyTheme(isLight) {
    if (isLight) {
        document.documentElement.setAttribute('data-theme', 'light');
        themeText.textContent = 'Modo Oscuro';
        themeToggleBtn.innerHTML = '☀️ Modo Oscuro';
    } else {
        document.documentElement.removeAttribute('data-theme');
        themeText.textContent = 'Modo Claro';
        themeToggleBtn.innerHTML = '🌙 Modo Claro';
    }
    localStorage.setItem('spatial-theme', isLight ? 'light' : 'dark');
    spatialScene.updateThemeColors(isLight);
}

applyTheme(savedTheme === 'light');

themeToggleBtn?.addEventListener('click', (event) => {
    event.preventDefault();
    const isLight = document.documentElement.getAttribute('data-theme') !== 'light';
    applyTheme(isLight);
});

// Raycaster para selección de objetos 3D
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let selectedMesh = null;
const sessionItemsKey = `spatial-items-${spaceId}`;

function getSessionItems() {
    try {
        return JSON.parse(sessionStorage.getItem(sessionItemsKey) || '[]');
    } catch (error) {
        return [];
    }
}

function saveSessionItem(item) {
    sessionStorage.setItem(sessionItemsKey, JSON.stringify([...getSessionItems(), item]));
}

function removeSessionItem(itemId) {
    const items = getSessionItems().filter(item => item.id !== itemId);
    sessionStorage.setItem(sessionItemsKey, JSON.stringify(items));
}

function addItemToScene(itemData, select = false) {
    const mesh = createItemMesh(itemData);
    spatialScene.addItem(mesh);

    if (select) {
        spatialScene.attachGizmo(mesh);
        selectedMesh = mesh;
    }

    return mesh;
}

getSessionItems().forEach(item => addItemToScene(item));

// Resaltar el botón activo en la barra superior (HUD)
function updateActiveKeyUI(mode) {
    document.querySelectorAll('.shortcut-item').forEach(el => el.classList.remove('active'));
    
    if (mode === 'translate') document.getElementById('key-m')?.classList.add('active');
    if (mode === 'rotate') document.getElementById('key-r')?.classList.add('active');
    if (mode === 'scale') document.getElementById('key-s')?.classList.add('active');
}

// Evento de Selección 3D
window.addEventListener('pointerdown', (event) => {
    if (event.target.tagName !== 'CANVAS') return;

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, spatialScene.camera);
    
    const targets = spatialScene.scene.children.filter(
        child => child !== spatialScene.gridHelper && child !== spatialScene.transform
    );
    
    const intersects = raycaster.intersectObjects(targets, true);

    if (intersects.length > 0) {
        let selected = intersects[0].object;
        while (selected.parent && selected.parent.type !== 'Scene') {
            selected = selected.parent;
        }

        if (selected.userData && selected.userData.id) {
            selectedMesh = selected;
            spatialScene.attachGizmo(selectedMesh);

            document.getElementById('pos-x').value = selectedMesh.position.x.toFixed(1);
            document.getElementById('pos-y').value = selectedMesh.position.y.toFixed(1);
            document.getElementById('pos-z').value = selectedMesh.position.z.toFixed(1);
        }
    } else {
        // Deseleccionar al hacer clic fuera
        spatialScene.detachGizmo();
        selectedMesh = null;
    }
});

// Actualizar campos de texto mientras se arrastra el Gizmo
spatialScene.transform.addEventListener('change', () => {
    if (selectedMesh) {
        document.getElementById('pos-x').value = selectedMesh.position.x.toFixed(1);
        document.getElementById('pos-y').value = selectedMesh.position.y.toFixed(1);
        document.getElementById('pos-z').value = selectedMesh.position.z.toFixed(1);
    }
});

// Guardar cambios en el backend (PUT) automáticamente cuando se suelta el Gizmo
spatialScene.transform.addEventListener('dragging-changed', async (event) => {
    // evento.value es false cuando el usuario suelta el mouse o el dedo
    if (!event.value && selectedMesh && selectedMesh.userData?.id) {
        const updatedData = {
            name: selectedMesh.userData.name,
            position: {
                x: parseFloat(selectedMesh.position.x.toFixed(2)),
                y: parseFloat(selectedMesh.position.y.toFixed(2)),
                z: parseFloat(selectedMesh.position.z.toFixed(2))
            },
            rotation: {
                x: parseFloat(selectedMesh.rotation.x.toFixed(2)),
                y: parseFloat(selectedMesh.rotation.y.toFixed(2)),
                z: parseFloat(selectedMesh.rotation.z.toFixed(2))
            },
            scale: {
                x: parseFloat(selectedMesh.scale.x.toFixed(2)),
                y: parseFloat(selectedMesh.scale.y.toFixed(2)),
                z: parseFloat(selectedMesh.scale.z.toFixed(2))
            },
            color: selectedMesh.userData.color || '#00f3ff',
            space_id: spaceId
        };

        try {
            await updateSpatialItem(selectedMesh.userData.id, updatedData);
        } catch (err) {
            console.error('Error al sincronizar con el backend:', err);
        }
    }
});

// Crear objetos desde el formulario
const itemForm = document.getElementById('item-form');
const addItemButton = document.getElementById('btn-add');

itemForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (addItemButton.disabled) return;

    addItemButton.disabled = true;
    
    const newItem = {
        name: document.getElementById('name').value,
        position: {
            x: parseFloat(document.getElementById('pos-x').value) || 0,
            y: parseFloat(document.getElementById('pos-y').value) || 0.5,
            z: parseFloat(document.getElementById('pos-z').value) || 0
        },
        dimensions: { width: 1, height: 1, depth: 1 },
        color: document.getElementById('color').value,
        space_id: spaceId
    };

    try {
        const usingDefaultPosition = newItem.position.x === 0
            && newItem.position.y === 0.5
            && newItem.position.z === 0;

        if (usingDefaultPosition) {
            const positionIsUsed = position => spatialScene.scene.children.some(child => {
                if (!child.userData?.id) return false;
                return child.position.x === position.x
                    && child.position.y === position.y
                    && child.position.z === position.z;
            });

            while (positionIsUsed(newItem.position)) {
                newItem.position.x += 1.5;
            }

            document.getElementById('pos-x').value = newItem.position.x;
        }

        const savedItem = await createSpatialItem(newItem);
        addItemToScene(savedItem, true);
        saveSessionItem(savedItem);
        document.getElementById('name').value = '';
        document.getElementById('pos-x').value = '0';
        document.getElementById('pos-y').value = '0.5';
        document.getElementById('pos-z').value = '0';
    } catch (err) {
        alert('Error al guardar el objeto en la API 3D');
    } finally {
        addItemButton.disabled = false;
    }
});

// Eliminar objeto seleccionado
async function removeSelectedObject() {
    if (!selectedMesh || !selectedMesh.userData?.id) return;

    try {
        await deleteSpatialItem(selectedMesh.userData.id);
        spatialScene.detachGizmo();
        spatialScene.scene.remove(selectedMesh);
        removeSessionItem(selectedMesh.userData.id);
        selectedMesh = null;
    } catch (err) {
        alert('Error al eliminar el objeto en el servidor');
    }
}

// Atajos de teclado
window.addEventListener('keydown', (event) => {
    const activeElement = document.activeElement;
    if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
        return;
    }

    const key = event.key.toLowerCase();

    switch (key) {
        case 'm':
            spatialScene.transform.setMode('translate');
            updateActiveKeyUI('translate');
            break;
        case 'r':
            spatialScene.transform.setMode('rotate');
            updateActiveKeyUI('rotate');
            break;
        case 's':
            spatialScene.transform.setMode('scale');
            updateActiveKeyUI('scale');
            break;
        case 'z':
            removeSelectedObject();
            break;
        case 'delete':
        case 'backspace':
            removeSelectedObject();
            break;
        case 'escape':
            spatialScene.detachGizmo();
            selectedMesh = null;
            updateActiveKeyUI('translate');
            break;
    }
});

// Eventos de clic táctil en la barra HUD superior
document.getElementById('key-m')?.addEventListener('click', () => {
    spatialScene.transform.setMode('translate');
    updateActiveKeyUI('translate');
});
document.getElementById('key-r')?.addEventListener('click', () => {
    spatialScene.transform.setMode('rotate');
    updateActiveKeyUI('rotate');
});
document.getElementById('key-s')?.addEventListener('click', () => {
    spatialScene.transform.setMode('scale');
    updateActiveKeyUI('scale');
});
document.getElementById('key-z')?.addEventListener('click', removeSelectedObject);
document.getElementById('key-esc')?.addEventListener('click', () => {
    spatialScene.detachGizmo();
    selectedMesh = null;
    updateActiveKeyUI('translate');
});

// Redimensionado de pantalla responsive
window.addEventListener('resize', () => {
    spatialScene.camera.aspect = window.innerWidth / window.innerHeight;
    spatialScene.camera.updateProjectionMatrix();
    spatialScene.renderer.setSize(window.innerWidth, window.innerHeight);
});

