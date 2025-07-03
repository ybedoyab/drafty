import { FaCode, FaCopy, FaDownload } from 'react-icons/fa';
import { useState } from 'react';

function cleanCadScript(cadScript) {
  // Remove leading/trailing triple backticks and optional language
  let code = cadScript
    .replace(/^```[a-zA-Z]*\s*/, '')
    .replace(/```\s*$/, '')
    .trim();
  // If there is a second block of triple backticks, cut everything after the first
  const secondBacktick = code.indexOf('```');
  if (secondBacktick !== -1) {
    code = code.substring(0, secondBacktick).trim();
  }
  return code;
}

export default function CADScriptViewer({ cadScript, className = "" }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(cleanCadScript(cadScript));
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const downloadScript = () => {
    const blob = new Blob([cleanCadScript(cadScript)], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated_cad_script.scad';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
          <h3 className="text-lg font-medium text-gray-900">Código OpenSCAD Generado</h3>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={downloadScript}
            className="flex items-center space-x-2 px-3 py-1 text-sm bg-green-600 text-white hover:bg-green-700 rounded-md transition-colors"
          >
            <FaDownload size={14} />
            <span>Descargar</span>
          </button>
          <button
            onClick={handleCopy}
            className="flex items-center space-x-2 px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
          >
            <FaCopy size={14} />
            <span>{copied ? '¡Copiado!' : 'Copiar'}</span>
          </button>
        </div>
      </div>
      <div className="p-4">
        <pre className="bg-gray-50 rounded-lg p-4 text-sm text-gray-800 overflow-x-auto whitespace-pre-wrap max-h-96 overflow-y-auto">
          {cleanCadScript(cadScript)}
        </pre>
      </div>
    </div>
  );
} 