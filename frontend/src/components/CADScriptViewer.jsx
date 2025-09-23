// CADScriptViewer: shows generated OpenSCAD code with copy and download actions
import { FaCode, FaCopy, FaDownload } from 'react-icons/fa';
import { useState } from 'react';
import { TEXT } from '../constants';

function cleanCadScript(cadScript) {
  let code = cadScript
    .replace(/^```[a-zA-Z]*\s*/, '')
    .replace(/```\s*$/, '')
    .trim();
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
        <p className="text-gray-500">{TEXT.cadViewer.empty}</p>
      </div>
    );
  }

  return (
    <div className={`h-full flex flex-col bg-white ${className}`}>
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center space-x-2">
          <FaCode className="text-indigo-600" />
          <h3 className="text-lg font-medium text-gray-900">{TEXT.cadViewer.title}</h3>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={downloadScript}
            className="flex items-center space-x-1 px-2 py-1 text-xs bg-green-600 text-white hover:bg-green-700 rounded transition-colors"
          >
            <FaDownload size={12} />
            <span>{TEXT.cadViewer.download}</span>
          </button>
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1 px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
          >
            <FaCopy size={12} />
            <span>{copied ? TEXT.cadViewer.copied : TEXT.cadViewer.copy}</span>
          </button>
        </div>
      </div>
      <div className="flex-1 p-4 overflow-hidden">
        <pre className="h-full bg-gray-50 rounded-lg p-4 text-sm text-gray-800 overflow-auto whitespace-pre-wrap">
          {cleanCadScript(cadScript)}
        </pre>
      </div>
    </div>
  );
} 