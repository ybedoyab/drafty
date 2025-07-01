import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-indigo-600">
          Drafty
        </Link>
        <nav className="space-x-4">
          <Link
            to="/"
            className="text-gray-600 hover:text-indigo-600 transition duration-150">
            Inicio
          </Link>
          <Link
            to="/generate"
            className="text-gray-600 hover:text-indigo-600 transition duration-150">
            Generar
          </Link>
        </nav>
      </div>
    </header>
  );
} 