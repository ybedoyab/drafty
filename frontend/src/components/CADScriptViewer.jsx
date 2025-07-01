import { FaCode, FaCopy } from 'react-icons/fa';
import { useState } from 'react';

export default function CADScriptViewer({ cadScript, className = "" }) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(cadScript);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

  if (!cadScript) {
    return (
      <div className={`bg-gray-100 rounded-lg p-8 text-center ${className}`}>
        <p className="text-gray-500">No hay script CAD para mostrar</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md ${className}`}>
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center space-x-2">
          <FaCode className="text-indigo-600" />
          <h3 className="text-lg font-medium text-gray-900">Script CAD Generado</h3>
        </div>
        <button
          onClick={copyToClipboard}
          className="flex items-center space-x-2 px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
        >
          <FaCopy size={14} />
          <span>{copied ? 'Copiado!' : 'Copiar'}</span>
        </button>
      </div>
      <div className="p-4">
        <pre className="bg-gray-50 rounded-lg p-4 text-sm text-gray-800 overflow-x-auto whitespace-pre-wrap">
          {cadScript}
        </pre>
      </div>
    </div>
  );
} 