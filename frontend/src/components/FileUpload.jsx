// FileUpload: drag-and-drop uploader with optional description field
import { useState } from 'react';
import { FaUpload, FaTimes, FaInfoCircle } from 'react-icons/fa';
import { TEXT } from '../constants';
import ExampleImages from './ExampleImages';

export default function FileUpload({ onFileSelect, selectedFile, onDescriptionChange, description, selectedExample, onExampleSelect }) {
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
      onExampleSelect(null);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
      onExampleSelect(null);
    }
  };

  const removeFile = () => {
    onFileSelect(null);
  };

  const handleExampleSelect = (example) => {
    onExampleSelect(example);
    onFileSelect(null);
  };

  return (
    <div className="space-y-6">
      {!selectedFile && !selectedExample ? (
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
            dragActive
              ? 'border-indigo-400 bg-indigo-50'
              : 'border-gray-300 hover:border-indigo-300'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <FaUpload className="mx-auto h-10 w-10 text-gray-400 mb-3" />
          <p className="text-base font-medium text-gray-900 mb-2">
            {TEXT.upload.title}
          </p>
          <p className="text-sm text-gray-500 mb-3">
            {TEXT.upload.subtitle}
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
            className="cursor-pointer bg-indigo-600 text-white px-3 py-1.5 rounded-md hover:bg-indigo-700 transition-colors text-sm font-medium"
          >
            {TEXT.upload.selectFile}
          </label>
        </div>
      ) : selectedFile ? (
        <div className="space-y-4">
          <div className="border rounded-lg p-3 bg-white">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-base font-medium text-gray-900">
                {TEXT.upload.selectedImage}
              </h3>
              <button
                onClick={removeFile}
                className="text-gray-400 hover:text-gray-600 transition-colors p-1"
              >
                <FaTimes size={16} />
              </button>
            </div>
            <div className="flex items-center space-x-3">
              <img
                src={URL.createObjectURL(selectedFile)}
                alt="Preview"
                className="w-16 h-16 object-cover rounded-lg border"
              />
              <div>
                <p className="font-medium text-gray-900 text-sm">{selectedFile.name}</p>
                <p className="text-xs text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>

          <div className="border rounded-lg p-3 bg-white">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <label className="text-xs font-medium text-gray-700">
                  {TEXT.upload.optionalDescription}
                </label>
                <div className="relative group">
                  <FaInfoCircle className="text-gray-400 cursor-help" size={14} />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-10">
                    {TEXT.upload.optionalDescriptionHelp}
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowDescription(!showDescription)}
                className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                  showDescription ? 'bg-indigo-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                    showDescription ? 'translate-x-4' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {showDescription && (
              <div className="mt-3">
                <textarea
                  value={description}
                  onChange={(e) => onDescriptionChange(e.target.value)}
                  placeholder={TEXT.upload.textareaPlaceholder}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                  rows={3}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {TEXT.upload.textareaHelp}
                </p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="border rounded-lg p-4 bg-white">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                Selected Example
              </h3>
              <button
                onClick={() => onExampleSelect(null)}
                className="text-gray-400 hover:text-gray-600 transition-colors p-1"
              >
                <FaTimes size={16} />
              </button>
            </div>
            <div className="flex items-center space-x-3">
              <img
                src={selectedExample.src}
                alt={selectedExample.name}
                className="w-16 h-16 object-cover rounded-lg border"
              />
              <div>
                <p className="font-medium text-gray-900 text-sm">{selectedExample.name}</p>
                <p className="text-xs text-gray-500">{selectedExample.description}</p>
              </div>
            </div>
          </div>

          <div className="border rounded-lg p-3 bg-white">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <label className="text-xs font-medium text-gray-700">
                  {TEXT.upload.optionalDescription}
                </label>
                <div className="relative group">
                  <FaInfoCircle className="text-gray-400 cursor-help" size={14} />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-10">
                    {TEXT.upload.optionalDescriptionHelp}
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowDescription(!showDescription)}
                className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                  showDescription ? 'bg-indigo-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                    showDescription ? 'translate-x-4' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {showDescription && (
              <div className="mt-3">
                <textarea
                  value={description}
                  onChange={(e) => onDescriptionChange(e.target.value)}
                  placeholder={TEXT.upload.textareaPlaceholder}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                  rows={3}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {TEXT.upload.textareaHelp}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {!selectedFile && !selectedExample && (
        <ExampleImages 
          onImageSelect={handleExampleSelect}
          selectedExample={selectedExample}
        />
      )}
    </div>
  );
} 