 // Three.js und OrbitControls importieren
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.120.1/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.120.1/examples/jsm/controls/OrbitControls.js';
import { HelperClass } from './HelperClass.js';

//Daten abrufen und vorbereiten#
// Daten laden (Testdaten1)
 fetch('./data/daten_richtig.json')
    .then(response => response.json())  // Parsen der JSON-Daten
    .then(data => {
        init(data);  // Funktion zur Initialisierung der Szene
    })
   .catch(error => console.error('Fehler beim Laden der Daten:', error));

//fetch('http://localhost:8080/src_python/daten.json')  // URL des Endpunkts auf Ihrem lokalen Server
//    .then(response => {
//        if (!response.ok) {
//            throw new Error(`HTTP-Fehler! Status: ${response.status}`);
//        }
//        return response.json();  // Parsen der JSON-Daten
//    })
//    .then(data => {
//        init(data);  // Funktion zur Initialisierung der Szene
//    })
//    .catch(error => console.error('Fehler beim Abrufen der Daten:', error));


function init(data) {


    //setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 500);
    const renderer = new THREE.WebGLRenderer();
    scene.background = new THREE.Color(0, 0, 0); 
    const container = document.getElementById('3d-container'); // Korrekte ID referenzieren
    renderer.setSize(container.offsetWidth, container.offsetHeight); // Größe des Renderers
    container.innerHTML = ""; // Sicherstellen, dass der Container leer ist
    container.appendChild(renderer.domElement);
    //ende setup

    //Konstanten
    const CONST_MAX_VALUES = HelperClass.getMax(data);
    const CONST_MIN_VALUES = HelperClass.getMin(data);

    const CONST_SCALE_FACTOR = 1;


    const CONST_MAX_X = CONST_MAX_VALUES.x;
    const CONST_MIN_X = CONST_MIN_VALUES.x;
    const CONST_NAME_X = 'X' //lila

    const CONST_MAX_Y = CONST_MAX_VALUES.y;
    const CONST_MIN_Y = CONST_MIN_VALUES.y;
    const CONST_NAME_Y = 'Y'; //blau

    const CONST_MAX_Z = CONST_MAX_VALUES.z;
    const CONST_MIN_Z = CONST_MIN_VALUES.z;
    const CONST_NAME_Z = 'Z' //gelb
    console.log(CONST_MAX_VALUES);
    console.log(CONST_MIN_VALUES);
 
    const CONST_ABSTAND_LINIEN = 10


    // OrbitControls für Interaktivität
    const controls = new OrbitControls(camera, renderer.domElement);
    //controls.enableDamping = true;
    //controls.dampingFactor = 0.25;

    //controls.zoomSpeed = 1;
    //controls.enablePan = true;
    controls.enableZoom = true;
    camera.position.z = 20;


    //Achsen: x und y und z
    scene.add(HelperClass.createAxis(0xd26bff, new THREE.Vector3(CONST_MIN_X * CONST_SCALE_FACTOR, 0, 0), new THREE.Vector3(CONST_MAX_X * CONST_SCALE_FACTOR, 0, 0)));
    scene.add(HelperClass.createAxis(0x6bfffb, new THREE.Vector3(0, CONST_MIN_Y * CONST_SCALE_FACTOR, 0), new THREE.Vector3(0, CONST_MAX_Y * CONST_SCALE_FACTOR, 0)));
    scene.add(HelperClass.createAxis(0xcccc00, new THREE.Vector3(0, 0, CONST_MIN_Z * CONST_SCALE_FACTOR), new THREE.Vector3(0, 0, CONST_MAX_Z * CONST_SCALE_FACTOR)));


    //Hilfslinien erstellen
    //HelperClass.createHelpLines(scene, CONST_ABSTAND_LINIEN * CONST_SCALE_FACTOR, CONST_MAX_X * CONST_SCALE_FACTOR, CONST_MAX_Y * CONST_SCALE_FACTOR, CONST_MAX_Z * CONST_SCALE_FACTOR, CONST_ABSTAND_LINIEN * CONST_SCALE_FACTOR);


    //Beschriftung x und y Achsen
    HelperClass.createLabel(scene, 0xd26bff, CONST_NAME_X, new THREE.Vector3(CONST_MAX_X * CONST_SCALE_FACTOR, 0, 0));
    HelperClass.createLabel(scene, 0x6bfffb, CONST_NAME_Y, new THREE.Vector3(0, CONST_MAX_Y * CONST_SCALE_FACTOR, 0));
    HelperClass.createLabel(scene, 0xcccc00, CONST_NAME_Z, new THREE.Vector3(0, 0, CONST_MAX_Z * CONST_SCALE_FACTOR));

    const points = [];
    
    data.forEach((item) => {
        const normalizedX = item.x * CONST_SCALE_FACTOR;
        const normalizedY = item.y * CONST_SCALE_FACTOR;
        const normalizedZ = item.z * CONST_SCALE_FACTOR;

        points.push(new THREE.Vector3(normalizedX, normalizedY, normalizedZ));
    });


     // Linie erstellen
     const geometry = new THREE.BufferGeometry().setFromPoints(points);
     const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
     const line = new THREE.Line(geometry, material);
     scene.add(line);

    //scene.add(new THREE.GridHelper(20,20));



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
}