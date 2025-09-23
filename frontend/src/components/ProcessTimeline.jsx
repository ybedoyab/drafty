import { FaImage, FaEye, FaCog, FaCode } from 'react-icons/fa';
import { TEXT } from '../constants';

const steps = TEXT.steps.items.map((s) => ({
  ...s,
  icon: s.id === 1 ? FaImage : s.id === 2 ? FaEye : s.id === 3 ? FaCog : FaCode,
}));

export default function ProcessTimeline({ currentStep = 0, completedSteps = [] }) {
  return (
    <div className="flex items-center space-x-4">
      {steps.map((step, index) => {
        const isCompleted = completedSteps.includes(step.id);
        const isCurrent = currentStep === step.id;
        const isPending = !isCompleted && !isCurrent;
        
        return (
          <div key={step.id} className="flex items-center">
            <div className={`flex items-center justify-center w-8 h-8 rounded-full text-xs font-medium ${
              isCompleted 
                ? 'bg-green-500 text-white' 
                : isCurrent 
                  ? 'bg-indigo-500 text-white' 
                  : 'bg-gray-200 text-gray-500'
            }`}>
              <step.icon size={12} />
            </div>
            <div className="ml-2 hidden lg:block">
              <p className={`text-xs font-medium ${
                isCompleted 
                  ? 'text-green-600' 
                  : isCurrent 
                    ? 'text-indigo-600' 
                    : 'text-gray-500'
              }`}>
                {step.name}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div className="hidden md:block mx-3">
                <div className={`w-8 h-0.5 ${
                  isCompleted ? 'bg-green-500' : 'bg-gray-300'
                }`} />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
