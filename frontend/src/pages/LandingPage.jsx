import { Link } from 'react-router-dom';
import Logo from '../assets/Logo.png';
import { TEXT } from '../constants';

export default function LandingPage() {
  return (
    <div className="w-full">
      <div className="flex flex-col items-center justify-center min-h-[60vh] py-12 px-4">
        <div className="bg-white/90 backdrop-blur-md rounded-3xl shadow-2xl px-8 py-12 flex flex-col items-center max-w-4xl w-full border border-indigo-100">
          <img src={Logo} alt="Drafty Logo" className="h-24 w-auto mb-6 drop-shadow-lg" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4 text-center">
            {TEXT.landing.taglinePrefix} <span className="text-indigo-600">{TEXT.landing.taglineHighlight1}</span> {TEXT.landing.taglineMiddle}
          </h1>
          <p className="text-xl text-gray-700 mb-2 text-center">
            <span className="text-purple-600 font-semibold">{TEXT.landing.taglineHighlight2}</span> {TEXT.landing.taglineSuffix}
          </p>
          <p className="text-lg text-gray-600 mb-8 text-center">
            {TEXT.landing.subtitle}
          </p>
          <Link
            to="/generate"
            className="inline-flex items-center gap-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold py-4 px-10 rounded-xl shadow-lg hover:scale-105 hover:shadow-xl transition-all text-lg">
            <span className="text-2xl">{TEXT.landing.rocket}</span> {TEXT.landing.cta}
          </Link>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          {TEXT.landing.processTitle}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {TEXT.landing.processSteps.map((step, index) => (
            <div key={index} className="bg-white rounded-2xl shadow-lg p-6 text-center hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">{step.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
              {index < TEXT.landing.processSteps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 text-indigo-400">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 