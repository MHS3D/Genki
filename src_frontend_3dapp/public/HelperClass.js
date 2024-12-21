import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.120.1/build/three.module.js';
export class HelperClass {

    //process data return points from json
    static processDataMeins(data){
        const points = [];
        data.forEach((elem) => {
            points.push(elem.x, elem.y, elem.z);
        });
        return points;
    }
   

    //create axes in the diagram
    static createAxis(color, startPoint, endPoint) {
        const material = new THREE.LineBasicMaterial({ color: color });
        const points = [startPoint, endPoint];
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, material);
        return line;
    }

    //create labels
    static createLabel(scene, color, text, position){
        const loader = new THREE.FontLoader();
            loader.load('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json', (font) => {
                const textGeometry = new THREE.TextGeometry(text, {
                    font: font,
                    size: 0.5,
                    height: 0.7,
                });
                const textMaterial = new THREE.MeshBasicMaterial({ color: color });
                const mesh = new THREE.Mesh(textGeometry, textMaterial);
                mesh.position.copy(position);
                scene.add(mesh);
            });
    }

    //create help lines
    static createHelpLines(scene, abstandLinien, max_x, max_y, max_z, min){
        for (let i = min; i <= max_x; i += abstandLinien) {
            const line = HelperClass.createAxis(
                0x888888,
                new THREE.Vector3(0, i, 0),
                new THREE.Vector3(max_x, i, 0)
            );
            scene.add(line);
            HelperClass.createLabel(scene, 0x888888, i.toString(), new THREE.Vector3(-2, i, 0));
        }
        for (let i = min; i <= max_y; i += abstandLinien) {
            const line = HelperClass.createAxis(
                0x888888,
                new THREE.Vector3(0, i, 0),
                new THREE.Vector3(0, i, max_z)
            );
            scene.add(line);
            HelperClass.createLabel(scene, 0x888888, i.toString(), new THREE.Vector3(-2, i, 0));
        }
        for (let i = min; i <= max_z; i += abstandLinien) {
            const line = HelperClass.createAxis(
                0x888888,
                new THREE.Vector3(0, 0, i),
                new THREE.Vector3(max_x, 0, i)
            );
            scene.add(line);
            HelperClass.createLabel(scene, 0x888888, i.toString(), new THREE.Vector3(-2, i, 0));
        }

    }

    static getMax(data){
        let maxX = -Infinity;
        let maxY = -Infinity;
        let maxZ = -Infinity;

        // Durchlaufe die Daten und finde das Maximum für x, y und z
        data.forEach(elem => {
            if (elem.x > maxX) maxX = elem.x;
            if (elem.y > maxY) maxY = elem.y;
            if (elem.z > maxZ) maxZ = elem.z;
        });

        // Rückgabe der maximalen Werte als Objekt
        return { x: maxX, y: maxY, z: maxZ };
    }

    static getMin(data){
        let minX = Infinity;
        let minY = Infinity;
        let minZ = Infinity;

        // Durchlaufe die Daten und finde das Maximum für x, y und z
        data.forEach(elem => {
            if (elem.x < minX) minX = elem.x;
            if (elem.y < minY) minY = elem.y;
            if (elem.z < minZ) minZ = elem.z;
        });

        // Rückgabe der maximalen Werte als Objekt
        return { x: minX, y: minY, z: minZ };
    }
    
}