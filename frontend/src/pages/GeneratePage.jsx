// GeneratePage: handles image upload, calls backend, and displays generated OpenSCAD code
import { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import ProcessSteps from '../components/ProcessSteps';
import CADScriptViewer from '../components/CADScriptViewer';
import GLTFViewer from '../components/GLTFViewer';
import { TEXT } from '../constants';

export default function GeneratePage() {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [cadScript, setCadScript] = useState('');
  const [glbUrl, setGlbUrl] = useState('');
  const [error, setError] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [backendStatus, setBackendStatus] = useState('checking');

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
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    if (description.trim()) {
      formData.append('description', description.trim());
    }
    
    setLoading(true);
    setError('');
    setCurrentStep(1);
    setCompletedSteps([]);
    
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
    <div className="min-h-screen bg-slate-100 py-12 px-4">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-2">{TEXT.generatePage.title}</h2>
          <p className="text-gray-600">
            {TEXT.generatePage.subtitle}
          </p>
        </div>

        <ErrorAlert message={error} onClose={() => setError('')} />
        
        {backendStatus === 'unhealthy' && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  {TEXT.backendStatus.unhealthyTitle}
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{TEXT.backendStatus.unhealthyDesc}</p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {backendStatus === 'healthy' && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">
                  {TEXT.backendStatus.healthyTitle}
                </h3>
                <div className="mt-2 text-sm text-green-700">
                  <p>{TEXT.backendStatus.healthyDesc}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <FileUpload 
                onFileSelect={setFile} 
                selectedFile={file}
                onDescriptionChange={setDescription}
                description={description}
              />
              
              <button
                type="submit"
                disabled={loading || !file}
                className="w-full flex justify-center items-center gap-2 py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading && <LoadingSpinner />}
                {loading ? TEXT.generatePage.buttonLoading : TEXT.generatePage.buttonIdle}
              </button>
            </form>

            <ProcessSteps 
              currentStep={currentStep} 
              completedSteps={completedSteps} 
            />
          </div>

          <div className="lg:col-span-2 space-y-6">
            {cadScript && (
              <CADScriptViewer cadScript={cadScript} />
            )}
            {glbUrl && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium text-gray-900">{TEXT.gltfViewer.title}</h3>
                  <a
                    href={glbUrl}
                    download
                    className="inline-flex items-center space-x-2 px-3 py-1 text-sm bg-indigo-600 text-white hover:bg-indigo-700 rounded-md transition-colors"
                  >
                    <span>{TEXT.gltfViewer.download}</span>
                  </a>
                </div>
                <GLTFViewer url={glbUrl} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 