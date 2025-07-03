import { Link } from 'react-router-dom';
import Logo from '../assets/Logo.png';

export default function Header() {
  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="flex items-center gap-3 group">
          <img src={Logo} alt="Drafty Logo" className="h-10 w-auto transition-transform group-hover:scale-105" />
        </Link>
        <nav className="space-x-4">
          <Link
            to="/"
            className="text-gray-600 hover:text-indigo-600 font-medium transition duration-150 px-2 py-1 rounded hover:bg-indigo-50">
            Inicio
          </Link>
          <Link
            to="/generate"
            className="text-gray-600 hover:text-indigo-600 font-medium transition duration-150 px-2 py-1 rounded hover:bg-indigo-50">
            Generar
          </Link>
        </nav>
      </div>
    </header>
  );
} 