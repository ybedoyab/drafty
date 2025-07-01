import { FaImage, FaEye, FaCog, FaFileAlt } from 'react-icons/fa';

const steps = [
  { id: 1, name: 'Subir imagen', icon: FaImage, description: 'Imagen 3D cargada' },
  { id: 2, name: 'Describir imagen', icon: FaEye, description: 'Análisis automático' },
  { id: 3, name: 'Crear CAD', icon: FaCog, description: 'Generación de modelo' },
  { id: 4, name: 'Crear plano', icon: FaFileAlt, description: 'Plano DXF generado' }
];

export default function ProcessSteps({ currentStep = 0, completedSteps = [] }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Progreso del proceso</h3>
      <div className="space-y-4">
        {steps.map((step, index) => {
          const isCompleted = completedSteps.includes(step.id);
          const isCurrent = currentStep === step.id;
          const isPending = !isCompleted && !isCurrent;
          
          return (
            <div key={step.id} className="flex items-center space-x-4">
              <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                isCompleted 
                  ? 'bg-green-500 text-white' 
                  : isCurrent 
                    ? 'bg-indigo-500 text-white' 
                    : 'bg-gray-200 text-gray-500'
              }`}>
                <step.icon size={20} />
              </div>
              <div className="flex-1">
                <p className={`font-medium ${
                  isCompleted 
                    ? 'text-green-600' 
                    : isCurrent 
                      ? 'text-indigo-600' 
                      : 'text-gray-500'
                }`}>
                  {step.name}
                </p>
                <p className="text-sm text-gray-500">{step.description}</p>
              </div>
              {isCompleted && (
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-xs">✓</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
} 