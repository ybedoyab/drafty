import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Box, Cylinder, Sphere } from '@react-three/drei';
import * as THREE from 'three';

// Simple geometry parser for basic shapes
function parseCADScript(script) {
  const geometries = [];
  
  // Basic parsing for common shapes (simplified for demo)
  const lines = script.toLowerCase().split('\n');
  
  lines.forEach(line => {
    if (line.includes('cube') || line.includes('box')) {
      // Extract dimensions if available
      const sizeMatch = line.match(/(\d+(?:\.\d+)?)/g);
      const size = sizeMatch ? parseFloat(sizeMatch[0]) : 1;
      geometries.push({ type: 'box', size: [size, size, size] });
    } else if (line.includes('cylinder')) {
      const radiusMatch = line.match(/radius[:\s]*(\d+(?:\.\d+)?)/);
      const heightMatch = line.match(/height[:\s]*(\d+(?:\.\d+)?)/);
      const radius = radiusMatch ? parseFloat(radiusMatch[1]) : 0.5;
      const height = heightMatch ? parseFloat(heightMatch[1]) : 1;
      geometries.push({ type: 'cylinder', radius, height });
    } else if (line.includes('sphere')) {
      const radiusMatch = line.match(/radius[:\s]*(\d+(?:\.\d+)?)/);
      const radius = radiusMatch ? parseFloat(radiusMatch[1]) : 0.5;
      geometries.push({ type: 'sphere', radius });
    }
  });
  
  return geometries;
}

function CADGeometry({ geometries }) {
  const groupRef = useRef();
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.005;
    }
  });

  return (
    <group ref={groupRef}>
      {geometries.map((geo, index) => {
        const position = [index * 2, 0, 0];
        
        switch (geo.type) {
          case 'box':
            return (
              <Box
                key={index}
                args={geo.size}
                position={position}
                wireframe
              >
                <meshStandardMaterial color="#3b82f6" wireframe />
              </Box>
            );
          case 'cylinder':
            return (
              <Cylinder
                key={index}
                args={[geo.radius, geo.radius, geo.height, 32]}
                position={position}
                wireframe
              >
                <meshStandardMaterial color="#10b981" wireframe />
              </Cylinder>
            );
          case 'sphere':
            return (
              <Sphere
                key={index}
                args={[geo.radius, 32, 32]}
                position={position}
                wireframe
              >
                <meshStandardMaterial color="#f59e0b" wireframe />
              </Sphere>
            );
          default:
            return null;
        }
      })}
    </group>
  );
}

export default function CADViewer({ cadScript, className = "" }) {
  const [geometries, setGeometries] = useState([]);

  // Parse CAD script when it changes
  useEffect(() => {
    if (cadScript) {
      const parsed = parseCADScript(cadScript);
      setGeometries(parsed);
    }
  }, [cadScript]);

  if (!cadScript || geometries.length === 0) {
    return (
      <div className={`bg-gray-100 rounded-lg p-8 text-center ${className}`}>
        <p className="text-gray-500">No hay modelo CAD para mostrar</p>
      </div>
    );
  }

  return (
    <div className={`bg-gray-900 rounded-lg overflow-hidden ${className}`} style={{ height: '400px' }}>
      <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Grid args={[10, 10]} />
        <CADGeometry geometries={geometries} />
        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
      </Canvas>
    </div>
  );
} 