import { FaSpinner } from 'react-icons/fa';

export default function LoadingSpinner({ size = 20, className = "" }) {
  return (
    <FaSpinner 
      className={`animate-spin ${className}`} 
      size={size}
    />
  );
} 