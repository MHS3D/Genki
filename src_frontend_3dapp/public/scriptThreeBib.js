// Three.js und OrbitControls importieren
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.120.1/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.120.1/examples/jsm/controls/OrbitControls.js';
import { HelperClass } from './HelperClass.js';

//Daten abrufen und vorbereiten#



//setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
scene.background = new THREE.Color(0, 0, 0);
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
//ende setup

//Konstanten
const CONST_MAX_X = 31
const CONST_MIN_X = 0
const CONST_NAME_X = 'X'

const CONST_MAX_Y = 31
const CONST_MIN_Y = 0
const CONST_NAME_Y = 'Y'

const CONST_MAX_Z = 20;
const CONST_MIN_Z = 0
const CONST_NAME_Z = 'Z'

const CONST_ABSTAND_LINIEN = 10

// OrbitControls für Interaktivität
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.25;

controls.zoomSpeed = 2;
controls.enablePan = true;
camera.position.z = 20;


//Achsen: x und y und z
scene.add(HelperClass.createAxis(0xd26bff, new THREE.Vector3(CONST_MIN_X, 0, 0), new THREE.Vector3(CONST_MAX_X, 0, 0)));
scene.add(HelperClass.createAxis(0x6bfffb, new THREE.Vector3(0, CONST_MIN_Y, 0), new THREE.Vector3(0, CONST_MAX_Y, 0)));
scene.add(HelperClass.createAxis(0xcccc00, new THREE.Vector3(0, 0, CONST_MIN_Z), new THREE.Vector3(0, 0, CONST_MAX_Z)));


//Hilfslinien erstellen
//HelperClass.createHelpLines(scene, CONST_ABSTAND_LINIEN, CONST_MAX_X, CONST_MAX_Y, CONST_MAX_Z, CONST_ABSTAND_LINIEN);


//Beschriftung x und y Achsen
HelperClass.createLabel(scene, 0xd26bff, CONST_NAME_X, new THREE.Vector3(CONST_MAX_X, 0, 0));
HelperClass.createLabel(scene, 0x6bfffb, CONST_NAME_Y, new THREE.Vector3(0, CONST_MAX_Y, 0));
HelperClass.createLabel(scene, 0xcccc00, CONST_NAME_Z, new THREE.Vector3(0, 0, CONST_MAX_Z));

//scene.add(new THREE.GridHelper(20,20));


const dummyData = [
    { x: 2.45, y: 12.35, z: 19.87 },
    { x: 3.14, y: 18.22, z: 5.67 },
    { x: 7.89, y: 10.50, z: 16.34 },
    { x: 18.72, y: 5.23, z: 13.98 },
    { x: 6.45, y: 11.21, z: 9.56 },
    { x: 1.23, y: 19.67, z: 4.11 },
    { x: 16.78, y: 14.12, z: 3.88 },
    { x: 11.56, y: 7.92, z: 15.34 },
    { x: 9.34, y: 8.61, z: 17.29 },
    { x: 13.24, y: 16.81, z: 6.54 },
    { x: 5.12, y: 3.54, z: 12.77 },
    { x: 14.58, y: 9.31, z: 8.99 },
    { x: 3.67, y: 17.42, z: 10.12 },
    { x: 10.14, y: 6.87, z: 4.45 },
    { x: 8.99, y: 13.67, z: 11.89 },
    { x: 7.21, y: 18.34, z: 19.05 },
    { x: 2.76, y: 5.13, z: 7.89 },
    { x: 15.45, y: 12.11, z: 18.23 },
    { x: 4.67, y: 10.98, z: 6.44 },
    { x: 19.32, y: 8.76, z: 14.91 }
];

// Erstellen der Linienpunkte basierend auf den Dummy-Daten
const points = [];
dummyData.forEach((data) => {
    points.push(new THREE.Vector3(data.x, data.y, data.z));
});

// optional: Ausgabe der Punkte in der Konsole
console.log(points);

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
