import * as THREE from 'three';

export function createItemMesh(itemData) {
    const { width, height, depth } = itemData.dimensions;
    const geometry = new THREE.BoxGeometry(width, height, depth);
    
    // 1. Material PBR con acabado Neón semi-transparente
    const material = new THREE.MeshStandardMaterial({
        color: new THREE.Color(itemData.color || '#00f3ff'),
        roughness: 0.2,
        metalness: 0.5,
        transparent: true,
        opacity: 0.85
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(itemData.position.x, itemData.position.y, itemData.position.z);
    
    // Habilitar sombras para mayor realismo gráfico
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    // 2. Bordes Neón Resaltados
    const edges = new THREE.EdgesGeometry(geometry);
    const lineMaterial = new THREE.LineBasicMaterial({ 
        color: 0xffffff, 
        transparent: true,
        opacity: 0.9 
    });
    const wireframe = new THREE.LineSegments(edges, lineMaterial);
    mesh.add(wireframe);

    // 3. Etiqueta Textual Flotante (Canvas 2D convertido a textura 3D)
    if (itemData.name) {
        const labelSprite = createTextSprite(itemData.name);
        // Posicionar la etiqueta sobre la parte superior del cubo
        labelSprite.position.set(0, (height / 2) + 0.3, 0);
        mesh.add(labelSprite);
    }

    // Guardar metadatos del backend
    mesh.userData = { 
        id: itemData.id, 
        name: itemData.name,
        color: itemData.color,
        dimensions: itemData.dimensions
    };

    return mesh;
}

// Función auxiliar para generar nombres flotantes sobre los objetos 3D
function createTextSprite(text) {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');

    // Fondo redondeado con transparencia
    ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
    ctx.strokeStyle = '#00f3ff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(10, 10, 236, 44, 10);
    ctx.fill();
    ctx.stroke();

    // Texto de la caja
    ctx.fillStyle = '#ffffff';
    ctx.font = 'Bold 20px system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 128, 32);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(spriteMaterial);
    
    // Escala del sprite dentro del espacio 3D
    sprite.scale.set(1.5, 0.375, 1);
    return sprite;
}