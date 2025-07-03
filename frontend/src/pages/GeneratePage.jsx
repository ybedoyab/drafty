import { useState } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import ProcessSteps from '../components/ProcessSteps';
import CADScriptViewer from '../components/CADScriptViewer';

export default function GeneratePage() {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [cadScript, setCadScript] = useState('');
  const [error, setError] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);

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
      // Simulate step progression
      setTimeout(() => setCurrentStep(2), 1000);
      setTimeout(() => setCurrentStep(3), 2000);
      setTimeout(() => setCurrentStep(4), 3000);
      
      const apiUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`;
      const { data } = await axios.post(`${apiUrl}/generate`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setCadScript(data.cad_script || '');
      setCompletedSteps([1, 2, 3, 4]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al procesar la imagen');
      setCurrentStep(0);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 py-12 px-4">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-2">Generar CAD</h2>
          <p className="text-gray-600">
            Sube una imagen de un objeto 3D y obtén su código OpenSCAD
          </p>
        </div>

        <ErrorAlert message={error} onClose={() => setError('')} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Upload and Process */}
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
                {loading ? 'Procesando imagen...' : 'Generar CAD'}
              </button>
            </form>

            <ProcessSteps 
              currentStep={currentStep} 
              completedSteps={completedSteps} 
            />
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">
            {cadScript && (
              <CADScriptViewer cadScript={cadScript} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 