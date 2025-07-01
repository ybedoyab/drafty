import { Link } from 'react-router-dom';
import { FaCube, FaDraftingCompass } from 'react-icons/fa';

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-600 to-purple-700 text-white p-8">
      <div className="text-center space-y-6 max-w-2xl">
        <div className="mx-auto flex items-center justify-center w-24 h-24 bg-white/20 rounded-full">
          <FaDraftingCompass size={48} />
        </div>
        <h1 className="text-5xl font-bold tracking-tight">Drafty</h1>
        <p className="text-xl opacity-90">
          Convierte <span className="font-semibold">imágenes 3D</span> en
          <span className="font-semibold"> planos de ingeniería</span> con ayuda de
          inteligencia artificial.
        </p>
        <Link
          to="/generate"
          className="inline-flex items-center gap-2 bg-white text-indigo-600 font-semibold py-3 px-6 rounded-lg shadow-lg hover:bg-slate-100 transition">
          <FaCube /> Generar Plano
        </Link>
      </div>
    </div>
  );
} 