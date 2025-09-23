// GeneratePage: handles image upload, calls backend, and displays generated OpenSCAD code
import { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import ProcessSteps from '../components/ProcessSteps';
import ProcessTimeline from '../components/ProcessTimeline';
import BackendStatus from '../components/BackendStatus';
import CADScriptViewer from '../components/CADScriptViewer';
import GLTFViewer from '../components/GLTFViewer';
import { TEXT } from '../constants';

export default function GeneratePage() {
  const [file, setFile] = useState(null);
  const [selectedExample, setSelectedExample] = useState(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [cadScript, setCadScript] = useState('');
  const [glbUrl, setGlbUrl] = useState('');
  const [error, setError] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [showCode, setShowCode] = useState(false);

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const apiUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`;
        const response = await axios.get(`${apiUrl}/health`);
        setBackendStatus('healthy');
        console.log('Backend health:', response.data);
      } catch (err) {
        setBackendStatus('unhealthy');
        console.error('Backend health check failed:', err);
      }
    };

    checkBackendHealth();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file && !selectedExample) return;
    
    const formData = new FormData();
    if (file) {
      formData.append('file', file);
    } else if (selectedExample) {
      const response = await fetch(selectedExample.src);
      const blob = await response.blob();
      const exampleFile = new File([blob], `${selectedExample.id}.jpg`, { type: 'image/jpeg' });
      formData.append('file', exampleFile);
    }
    
    if (description.trim()) {
      formData.append('description', description.trim());
    }
    
    setLoading(true);
    setError('');
    setCurrentStep(1);
    setCompletedSteps([]);
    setShowCode(false);
    
    try {
      setTimeout(() => setCurrentStep(2), 1000);
      setTimeout(() => setCurrentStep(3), 2000);
      setTimeout(() => setCurrentStep(4), 3000);
      
      const apiUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`;
      const { data } = await axios.post(`${apiUrl}/generate`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setCadScript(data.cad_script || '');
      setGlbUrl(data.glb_url || '');
      setCompletedSteps([1, 2, 3, 4]);
    } catch (err) {
      console.error('Error details:', err);
      let errorMessage = TEXT.errors.processing;
      
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.code === 'NETWORK_ERROR' || err.message?.includes('Network Error')) {
        errorMessage = TEXT.errors.network;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setCurrentStep(0);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="h-screen flex flex-col">
        <div className="py-4 px-6 border-b border-gray-200 bg-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{TEXT.generatePage.title}</h2>
              <p className="text-sm text-gray-600 mt-1">
                {TEXT.generatePage.subtitle}
              </p>
            </div>
            <div className="flex items-center space-x-6">
              <BackendStatus status={backendStatus} />
              <ProcessTimeline 
                currentStep={currentStep} 
                completedSteps={completedSteps} 
              />
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-hidden">
          <div className="h-full flex">
            <div className="w-1/3 border-r border-gray-200 bg-white overflow-y-auto">
              <div className="p-4 space-y-4">
                <ErrorAlert message={error} onClose={() => setError('')} />

                <form onSubmit={handleSubmit} className="space-y-4">
                  <FileUpload 
                    onFileSelect={setFile} 
                    selectedFile={file}
                    selectedExample={selectedExample}
                    onExampleSelect={setSelectedExample}
                    onDescriptionChange={setDescription}
                    description={description}
                  />
                  
                  <button
                    type="submit"
                    disabled={loading || (!file && !selectedExample)}
                    className="w-full flex justify-center items-center gap-2 py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
                  >
                    {loading ? (
                      <>
                        <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        <span>Processing image...</span>
                      </>
                    ) : (
                      <span>{TEXT.generatePage.buttonIdle}</span>
                    )}
                  </button>
                </form>
              </div>
            </div>

            <div className="flex-1 overflow-hidden bg-gray-50">
              <div className="h-full flex flex-col">
                {/* CAD Viewer (3D Model) - Always on top */}
                {glbUrl && (
                  <div className="flex-1">
                    <div className="h-full flex flex-col">
                      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
                        <h3 className="text-lg font-medium text-gray-900">{TEXT.gltfViewer.title}</h3>
                        <a
                          href={glbUrl}
                          download
                          className="inline-flex items-center space-x-1 px-2 py-1 text-xs bg-indigo-600 text-white hover:bg-indigo-700 rounded transition-colors"
                        >
                          <span>{TEXT.gltfViewer.download}</span>
                        </a>
                      </div>
                      <div className="flex-1">
                        <GLTFViewer url={glbUrl} />
                      </div>
                    </div>
                  </div>
                )}

                {/* OpenSCAD Code - Collapsible section below */}
                {cadScript && (
                  <div className="border-t border-gray-200 bg-white">
                    <div
                      className="flex items-center justify-between p-3 cursor-pointer hover:bg-gray-50 transition-colors"
                      onClick={() => setShowCode(!showCode)}
                    >
                      <h3 className="text-base font-medium text-gray-900">{TEXT.cadViewer.title}</h3>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-600">
                          {showCode ? TEXT.cadViewer.hideCode : TEXT.cadViewer.showCode}
                        </span>
                        <svg
                          className={`w-4 h-4 text-gray-600 transition-transform duration-200 ${
                            showCode ? 'rotate-180' : ''
                          }`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                    </div>
                    {showCode && (
                      <div className="border-t border-gray-100">
                        <CADScriptViewer cadScript={cadScript} />
                      </div>
                    )}
                  </div>
                )}

                {/* Empty state or Loading state */}
                {!cadScript && !glbUrl && (
                  <div className="flex-1 flex items-center justify-center">
                    {loading ? (
                      <div className="text-center text-gray-600">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                        <h3 className="text-xl font-medium mb-2">Processing image...</h3>
                        <p>AI is analyzing your image and generating the CAD model</p>
                      </div>
                    ) : (
                      <div className="text-center text-gray-500">
                        <div className="text-6xl mb-4">🎯</div>
                        <h3 className="text-xl font-medium mb-2">Ready to generate?</h3>
                        <p>Upload an image or select an example to get started</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 