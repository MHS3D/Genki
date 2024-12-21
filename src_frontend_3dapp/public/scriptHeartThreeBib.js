// Three.js und OrbitControls importieren
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.120.1/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.120.1/examples/jsm/controls/OrbitControls.js';
import { HelperClass } from './HelperClass.js';

//setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
//ende setup


//Konstanten
const CONST_MAX_BPM = 31
const CONST_ANZAHL_INTERVALLE = 21
const CONST_INTERVALL = 'intervall'
const CONST_BPM = 'bpm'
const CONST_ABSTAND_LINIEN = 10


// OrbitControls für Interaktivität
const controls = new OrbitControls(camera, renderer.domElement);
controls.enablePan = true;
controls.enableDamping = false;
controls.enableRotate = false;
controls.enableZoom = false;
camera.position.z = 50;


//Achsen: x und y
scene.add(HelperClass.createAxis(0xd26bff, new THREE.Vector3(0, 0, 0), new THREE.Vector3(CONST_ANZAHL_INTERVALLE, 0, 0)));
scene.add(HelperClass.createAxis(0x6bfffb, new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, CONST_MAX_BPM, 0)));


//Hilfslinien erstellen
for (let i = 10; i <= CONST_MAX_BPM; i += CONST_ABSTAND_LINIEN) {
    const line = HelperClass.createAxis(
        0x888888,
        new THREE.Vector3(0, i, 0),
        new THREE.Vector3(CONST_ANZAHL_INTERVALLE, i, 0)
    );
    scene.add(line);
    HelperClass.createLabel(scene, 0x888888, i.toString(), new THREE.Vector3(-2, i, 0));
}


//Beschriftung x und y Achsen
HelperClass.createLabel(scene, 0xd26bff, CONST_INTERVALL, new THREE.Vector3(CONST_ANZAHL_INTERVALLE, 0, 0));
HelperClass.createLabel(scene, 0x6bfffb, CONST_BPM, new THREE.Vector3(0, CONST_MAX_BPM, 0));

//scene.add(new THREE.GridHelper(20,20));


// Beispielhafte Herzfrequenzdaten
const heartRateData = [
    5, 20, 14, 18, 12, 6, 12, 18, 18, 18, 9, 18, 20, 13, 12, 12, 11, 10, 9, 8, 11
];

// Erstellen der Linienpunkte basierend auf den Herzfrequenzdaten
const points = [];
heartRateData.forEach((value, index) => {
    points.push(new THREE.Vector3(index, value, 0));
});

// Linie erstellen
const geometry = new THREE.BufferGeometry().setFromPoints(points);
const material = new THREE.LineBasicMaterial({ color: 0xff0000 });  // Rot für Herzfrequenzlinie
const line = new THREE.Line(geometry, material);
scene.add(line);

// Animation
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

// Bei Fensteränderungen die Größenanpassung
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
