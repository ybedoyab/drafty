export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 text-center py-6 text-sm text-gray-500 mt-12 shadow-inner">
      <div className="flex flex-col items-center gap-2">
        <span>© 2025 <span className="font-semibold text-indigo-600">Drafty</span> · DeepPunkAI Hackathon</span>
        <a
          href="https://github.com/ybedoyab/drafty"
          target="_blank"
          rel="noopener noreferrer"
          className="text-indigo-500 hover:underline hover:text-indigo-700 transition"
        >
          Ver proyecto en GitHub
        </a>
      </div>
    </footer>
  );
} 