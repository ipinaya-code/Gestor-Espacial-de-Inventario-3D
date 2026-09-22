import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';

export class SpatialScene {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.scene = new THREE.Scene();
        
        this.initCamera();
        this.initRenderer();
        this.initLights();
        this.initControls();
        
        // Cargar esquema de colores según el tema inicial
        this.updateThemeColors(document.documentElement.getAttribute('data-theme') === 'light');

        window.addEventListener('resize', () => this.onWindowResize());
    }

    initCamera() {
        this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(8, 6, 10);
    }

    initRenderer() {
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Habilitar renderizado de sombras PBR
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    }

    initLights() {
        this.ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        
        this.directionalLight = new THREE.DirectionalLight(0x00f3ff, 1.5);
        this.directionalLight.position.set(10, 15, 10);
        this.directionalLight.castShadow = true;
        
        // Configuración de resolución de sombras
        this.directionalLight.shadow.mapSize.width = 1024;
        this.directionalLight.shadow.mapSize.height = 1024;
        this.directionalLight.shadow.camera.near = 0.5;
        this.directionalLight.shadow.camera.far = 50;

        this.scene.add(this.ambientLight, this.directionalLight);
    }

    initGrid(isLight = false) {
        const color1 = isLight ? 0x0066ff : 0x00f3ff;
        const color2 = isLight ? 0xcbd5e1 : 0x334155;
        
        this.gridHelper = new THREE.GridHelper(20, 20, color1, color2);
        this.gridHelper.position.y = -0.01; // Evitar z-fighting con los objetos
        this.scene.add(this.gridHelper);
    }

    initControls() {
        // Control de cámara OrbitControls
        this.orbit = new OrbitControls(this.camera, this.renderer.domElement);
        this.orbit.enableDamping = true;
        this.orbit.dampingFactor = 0.05;
        
        // Restricciones ergonómicas para móviles y laptops
        this.orbit.maxPolarAngle = Math.PI / 2 - 0.02; // Evita atravesar la grilla por debajo
        this.orbit.minDistance = 2;
        this.orbit.maxDistance = 40;

        // Control Gizmo 3D TransformControls
        this.transform = new TransformControls(this.camera, this.renderer.domElement);
        this.scene.add(this.transform);

        // Desactivar OrbitControls durante el arrastre del Gizmo para evitar colisiones
        this.transform.addEventListener('dragging-changed', (event) => {
            this.orbit.enabled = !event.value;
        });
    }

    attachGizmo(mesh) {
        this.transform.attach(mesh);
    }

    detachGizmo() {
        this.transform.detach();
    }

    updateThemeColors(isLight) {
        const bgColor = isLight ? 0xf1f5f9 : 0x050811;
        this.scene.background = new THREE.Color(bgColor);
        
        // Ajustar color e intensidad de luces según el modo
        if (this.directionalLight) {
            this.directionalLight.color.setHex(isLight ? 0x0066ff : 0x00f3ff);
            this.directionalLight.intensity = isLight ? 1.2 : 1.5;
        }

        // Recrear grilla con los colores del tema
        if (this.gridHelper) {
            this.scene.remove(this.gridHelper);
        }
        this.initGrid(isLight);
    }

    addItem(mesh) {
        this.scene.add(mesh);
    }

    render() {
        requestAnimationFrame(() => this.render());
        this.orbit.update();
        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}