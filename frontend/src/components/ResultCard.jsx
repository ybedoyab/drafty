// ResultCard: shows DXF download when available
import { FaFileDownload, FaCheckCircle } from 'react-icons/fa';
import { TEXT } from '../constants';

export default function ResultCard({ dxfPath }) {
  if (!dxfPath) return null;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
      <div className="flex items-center space-x-3 mb-4">
        <FaCheckCircle className="text-green-500" size={24} />
        <h3 className="text-lg font-medium text-gray-900">
          {TEXT.resultCard.successTitle}
        </h3>
      </div>
      <p className="text-gray-600 mb-4">
        {TEXT.resultCard.description}
      </p>
      <a
        href={dxfPath}
        download
        className="inline-flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
      >
        <FaFileDownload />
        <span>{TEXT.resultCard.downloadDXF}</span>
      </a>
    </div>
  );
} 