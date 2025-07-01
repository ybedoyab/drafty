import { useState } from 'react';
import { FaUpload, FaTimes, FaInfoCircle } from 'react-icons/fa';

export default function FileUpload({ onFileSelect, selectedFile, onDescriptionChange, description }) {
  const [dragActive, setDragActive] = useState(false);
  const [showDescription, setShowDescription] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  const removeFile = () => {
    onFileSelect(null);
  };

  return (
    <div className="space-y-4">
      {!selectedFile ? (
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-indigo-400 bg-indigo-50'
              : 'border-gray-300 hover:border-indigo-300'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <FaUpload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            Sube una imagen 3D
          </p>
          <p className="text-gray-500 mb-4">
            Arrastra y suelta aquí, o haz clic para seleccionar
          </p>
          <input
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors"
          >
            Seleccionar archivo
          </label>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="border rounded-lg p-4 bg-white">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                Imagen seleccionada
              </h3>
              <button
                onClick={removeFile}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <FaTimes size={20} />
              </button>
            </div>
            <div className="flex items-center space-x-4">
              <img
                src={URL.createObjectURL(selectedFile)}
                alt="Preview"
                className="w-24 h-24 object-cover rounded-lg border"
              />
              <div>
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>

          {/* Optional Description Toggle */}
          <div className="border rounded-lg p-4 bg-white">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700">
                  Agregar descripción opcional
                </label>
                <div className="relative group">
                  <FaInfoCircle className="text-gray-400 cursor-help" size={16} />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-10">
                    Proporciona detalles adicionales como dimensiones, materiales o características específicas para mejorar la precisión del plano generado
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowDescription(!showDescription)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  showDescription ? 'bg-indigo-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    showDescription ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {showDescription && (
              <div className="mt-3">
                <textarea
                  value={description}
                  onChange={(e) => onDescriptionChange(e.target.value)}
                  placeholder="Ej: Rampa de 1 metro de alto y 3 metros de ancho, con inclinación de 15 grados..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                  rows={3}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Describe dimensiones, materiales, ángulos o características específicas del objeto
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 