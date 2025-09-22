// GLTFViewer: displays a GLB/GLTF asset using three.js
import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export default function GLTFViewer({ url, className = "", background = 0xf8fafc }) {
  const containerRef = useRef(null);
  const rendererRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const controlsRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = 400;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(background);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(50, width / height, 0.01, 1000);
    camera.position.set(2.5, 2.5, 2.5);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(width, height);
    rendererRef.current = renderer;
    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);

    const ambient = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambient);
    const dir = new THREE.DirectionalLight(0xffffff, 0.8);
    dir.position.set(5, 10, 7.5);
    scene.add(dir);

    const grid = new THREE.GridHelper(10, 10);
    scene.add(grid);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controlsRef.current = controls;

    let model = null;
    if (url) {
      const loader = new GLTFLoader();
      loader.load(
        url,
        (gltf) => {
          model = gltf.scene || gltf.scenes?.[0];
          if (model) {
            scene.add(model);
            // Center and frame the model
            const box = new THREE.Box3().setFromObject(model);
            const size = new THREE.Vector3();
            const center = new THREE.Vector3();
            box.getSize(size);
            box.getCenter(center);
            model.position.sub(center);
            const maxDim = Math.max(size.x, size.y, size.z);
            camera.position.set(maxDim * 1.5, maxDim * 1.2, maxDim * 1.5);
            camera.lookAt(0, 0, 0);
          }
        },
        undefined,
        (err) => {
          // eslint-disable-next-line no-console
          console.error('GLTF load error', err);
        }
      );
    }

    const onResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = 400;
      renderer.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    window.addEventListener('resize', onResize);

    let rafId;
    const animate = () => {
      rafId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      window.removeEventListener('resize', onResize);
      if (rafId) cancelAnimationFrame(rafId);
      if (renderer) {
        renderer.dispose();
      }
      if (scene) {
        scene.traverse((obj) => {
          if (obj.geometry) obj.geometry.dispose();
          if (obj.material) {
            if (Array.isArray(obj.material)) obj.material.forEach((m) => m.dispose());
            else obj.material.dispose();
          }
        });
      }
    };
  }, [url, background]);

  return (
    <div ref={containerRef} className={`bg-white rounded-lg shadow-md p-2 ${className}`}></div>
  );
}


