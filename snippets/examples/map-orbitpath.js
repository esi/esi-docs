// THREE.js provides a built-in `from vector 0 onto vector 1` rotation constructor
function calculate_orbit_rotation(position_sun, position_planet) {
    return new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(-1, 0, 0), new THREE.Vector3().subVectors(position_planet, position_sun).normalize());
}

// Alternative full reimplementation:
function calculate_orbit_rotation2(position_sun, position_planet) {
    const v0 = new THREE.Vector3(-1.0, 0.0, 0.0);
    const v1 = position_planet.sub(position_sun).normalize();   // THREE.js mutates vectors, but we only use position_planet once here.
    const c = new THREE.Vector3().crossVectors(v0, v1);         // THREE.js mutates vectors, so create a new vector to place the cross product in.
    const d = v0.dot(v1);
    const s = Math.sqrt((d + 1.0) * 2.0);
    return new THREE.Quaternion(c.x / s, c.y / s, c.z / s, s / 2.0);
}

/* Example setup */

import * as THREE from 'three';
import {OrbitControls} from 'Orbit';

const CAMERA_NEAR = 5.0E10;
const CAMERA_FAR = 5.0E17;
const CAMERA_POS = [0, 2.0E12, 0];
const PLANET_SIZE = 0.5E10;

const sun_info = {name: "Jita", x: 0.0, y: 0.0, z: 0.0};
const planet_info = [
    {name: "Jita I", x: -35639949630.0, y: -6225947509.0, z: 20551935633.0},
    {name: "Jita II", x: 29476716044.0, y: 5149291420.0, z: -46417511315.0},
    {name: "Jita III", x: 124056083719.0, y: 21671373654.0, z: 16235707106.0},
    {name: "Jita IV", x: -107354576606.0, y: -18753785170.0, z: 436797007078.0},
    {name: "Jita V", x: -639929607985.0, y: -111789387758.0, z: -1118379774141.0},
    {name: "Jita VI", x: 2907924314427.0, y: 507985682645.0, z: -950946134275.0},
    {name: "Jita VII", x: -2275005926406.0, y: -397421085828.0, z: 3223734974754.0},
    {name: "Jita VIII", x: -4067664386091.0, y: -710580828973.0, z: -3956610895959.0}
]

// Initialize three.js scene
const map_container = document.getElementById("map_container");
const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer();
renderer.setSize(map_container.clientWidth, map_container.clientHeight, false);
map_container.appendChild(renderer.domElement);
const camera = new THREE.PerspectiveCamera(35, map_container.clientWidth / map_container.clientHeight, CAMERA_NEAR, CAMERA_FAR);
camera.position.set(...CAMERA_POS);
const controls = new OrbitControls(camera, renderer.domElement);
const light = new THREE.HemisphereLight(0xffffff, 0x888888, 3);
light.position.set(...CAMERA_POS);
scene.add(light);

// Create shared resources
const sphere_geometry = new THREE.SphereGeometry(PLANET_SIZE);
const sun_material = new THREE.MeshPhongMaterial({color: 0xffff00});
const planet_material = new THREE.MeshPhongMaterial({color: 0xffffff});

const sun_mesh = new THREE.Mesh(sphere_geometry, sun_material);
sun_mesh.position.set(sun_info.x, sun_info.y, sun_info.z);
scene.add(sun_mesh);

for (let planet of planet_info) {
    const planet_mesh = new THREE.Mesh(sphere_geometry, planet_material);
    planet_mesh.position.set(planet.x, planet.y, planet.z);
    scene.add(planet_mesh);

    const radius = new THREE.Vector3().subVectors(planet_mesh.position, sun_mesh.position).length();
    let orbitLine = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(
            new THREE.EllipseCurve(0, 0, radius, radius)            // EllipseCurve creates a 2D X-Y circle
                .getSpacedPoints(50)
                .map(vec2 => new THREE.Vector3(vec2.x, 0, vec2.y))  // Map into 3D XZ plane
        ),
        new THREE.LineBasicMaterial({color: "blue"})
    );
    orbitLine.applyQuaternion(calculate_orbit_rotation(sun_mesh.position, planet_mesh.position));
    scene.add(orbitLine);
}

// Setup renderer loop
renderer.setAnimationLoop(function () {
    controls.update();
    renderer.render(scene, camera);
});
window.addEventListener('resize', function () {
    camera.aspect = map_container.clientWidth / map_container.clientHeight
    renderer.setSize(map_container.clientWidth, map_container.clientHeight, false);
    camera.updateProjectionMatrix();
});