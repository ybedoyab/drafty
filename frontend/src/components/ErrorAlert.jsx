import { FaExclamationTriangle } from 'react-icons/fa';

export default function ErrorAlert({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <FaExclamationTriangle className="text-red-500" size={20} />
          <p className="text-red-800 font-medium">{message}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-red-400 hover:text-red-600 transition-colors"
          >
            ×
          </button>
        )}
      </div>
    </div>
  );
} 