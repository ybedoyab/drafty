import { TEXT } from '../constants';

export default function BackendStatus({ status }) {
  if (status === 'checking') {
    return (
      <div className="flex items-center space-x-1 text-gray-500">
        <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
        <span className="text-xs font-medium">Checking...</span>
      </div>
    );
  }

  if (status === 'unhealthy') {
    return (
      <div className="flex items-center space-x-1 text-red-600">
        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
        <span className="text-xs font-medium">Not Working</span>
      </div>
    );
  }

  if (status === 'healthy') {
    return (
      <div className="flex items-center space-x-1 text-green-600">
        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
        <span className="text-xs font-medium">Working</span>
      </div>
    );
  }

  return null;
}
