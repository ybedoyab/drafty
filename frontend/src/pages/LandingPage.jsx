import { Link } from 'react-router-dom';
import Logo from '../assets/Logo.png';

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] py-12">
      <div className="bg-white/80 backdrop-blur-md rounded-3xl shadow-2xl px-8 py-12 flex flex-col items-center max-w-2xl w-full border border-indigo-100">
        <img src={Logo} alt="Drafty Logo" className="h-20 w-auto mb-4 drop-shadow-lg" />
        <p className="text-lg text-gray-700 mb-8">
          Convierte <span className="font-semibold text-indigo-600">imágenes 3D</span> en
          <span className="font-semibold text-indigo-600"> código OpenSCAD</span> con ayuda de inteligencia artificial.
        </p>
        <Link
          to="/generate"
          className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold py-3 px-8 rounded-xl shadow-lg hover:scale-105 hover:shadow-xl transition-all text-lg">
          <span className="text-2xl">🚀</span> Generar CAD
        </Link>
      </div>
    </div>
  );
} 