import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import GeneratePage from './pages/GeneratePage';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-50 via-white to-purple-100">
      <Header />
      <main className="flex-1 flex flex-col items-center px-2 sm:px-0 py-6">
        <div className="w-full max-w-5xl">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/generate" element={<GeneratePage />} />
          </Routes>
        </div>
      </main>
      <Footer />
    </div>
  );
} 