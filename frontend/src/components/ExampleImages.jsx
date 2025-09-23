import { useState } from 'react';
import { TEXT } from '../constants';

import cubeImg from '../assets/examples/cube.jpg';
import cylinderImg from '../assets/examples/cilinder.jpg';
import pyramidImg from '../assets/examples/pyramid.jpg';
import rampImg from '../assets/examples/ramp.jpg';

const exampleImages = [
  {
    id: 'cube',
    name: 'Cube',
    src: cubeImg,
    description: 'Simple geometric cube shape'
  },
  {
    id: 'cylinder',
    name: 'Cylinder',
    src: cylinderImg,
    description: 'Cylindrical object with rounded edges'
  },
  {
    id: 'pyramid',
    name: 'Pyramid',
    src: pyramidImg,
    description: 'Triangular pyramid structure'
  },
  {
    id: 'ramp',
    name: 'Ramp',
    src: rampImg,
    description: 'Inclined plane or ramp design'
  }
];

export default function ExampleImages({ onImageSelect, selectedExample }) {
  const [hoveredExample, setHoveredExample] = useState(null);

  return (
    <div className="space-y-4">
      <div className="text-center">
        <h3 className="text-base font-semibold text-gray-900 mb-1">
          {TEXT.examples.title}
        </h3>
        <p className="text-xs text-gray-600 mb-3">
          {TEXT.examples.subtitle}
        </p>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        {exampleImages.map((example) => (
          <div
            key={example.id}
            className={`relative cursor-pointer rounded-lg border-2 transition-all duration-200 ${
              selectedExample === example.id
                ? 'border-indigo-500 ring-2 ring-indigo-200'
                : 'border-gray-200 hover:border-indigo-300'
            }`}
            onClick={() => onImageSelect(example)}
            onMouseEnter={() => setHoveredExample(example.id)}
            onMouseLeave={() => setHoveredExample(null)}
          >
            <div className="aspect-square overflow-hidden rounded-t-lg">
              <img
                src={example.src}
                alt={example.name}
                className="w-full h-full object-cover transition-transform duration-200 hover:scale-105"
              />
            </div>
            <div className="p-2 bg-white rounded-b-lg">
              <h4 className="font-medium text-gray-900 text-xs">{example.name}</h4>
              <p className="text-xs text-gray-500 mt-0.5">{example.description}</p>
            </div>
            {selectedExample === example.id && (
              <div className="absolute top-1 right-1 w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center">
                <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            )}
          </div>
        ))}
      </div>
      
      {selectedExample && (
        <div className="text-center">
          <button
            onClick={() => onImageSelect(null)}
            className="text-xs text-indigo-600 hover:text-indigo-700 font-medium px-2 py-1 rounded hover:bg-indigo-50 transition-colors"
          >
            {TEXT.examples.clearSelection}
          </button>
        </div>
      )}
    </div>
  );
}
