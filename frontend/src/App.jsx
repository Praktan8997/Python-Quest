import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { GuidedPath } from './pages/GuidedPath';
import { ExploreTopics } from './pages/ExploreTopics';
import { TopicDetail } from './pages/TopicDetail';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

export const AppContent = () => {
  return (
    <div className="min-h-screen bg-[#05060f] text-[#C8DCF5] flex flex-col font-sans relative selection:bg-[#663af3]/40 selection:text-white">
      {/* AuthKit Conic Hero Halo Atmosphere */}
      <div className="authkit-hero-halo" />

      {/* Header Navigation */}
      <Navbar />

      {/* Main Content View */}
      <main className="flex-1 relative z-10">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/path" element={<GuidedPath />} />
          <Route path="/explore" element={<ExploreTopics />} />
          <Route path="/topic/:topicId" element={<TopicDetail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>

      {/* AuthKit Midnight Cathedral Footer */}
      <footer className="relative z-10 border-t border-[rgba(186,215,247,0.12)] bg-[#05060f]/80 py-10 text-center text-xs text-[#8AA4C4] backdrop-blur-2xl font-sans">
        <div className="max-w-[1200px] mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2.5 font-heading text-sm font-semibold text-[#F0F6FF]">
            <span className="w-2 h-2 rounded-full bg-[#663af3] shadow-[0_0_10px_#663af3]" />
            AuthKit Quest
          </div>
          <p className="font-eyebrow text-[11px] tracking-wider text-[#526884]">
            AUTHENTICATION & CURRICULUM ARCHITECTURE • MIDNIGHT LAUNCHPAD
          </p>
          <div className="flex items-center gap-5 text-xs font-medium text-[#8AA4C4]">
            <a href="#docs" className="hover:text-[#F0F6FF] transition-colors">Documentation</a>
            <a href="#api" className="hover:text-[#F0F6FF] transition-colors">API Reference</a>
            <a href="#security" className="hover:text-[#F0F6FF] transition-colors">Security</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
