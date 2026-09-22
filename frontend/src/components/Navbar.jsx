import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Flame, Zap, Compass, Map, User, ShieldCheck, Menu, X, Sparkles, LogIn } from 'lucide-react';

export const Navbar = () => {
  const { user } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => {
    if (path === '/' || path === '/dashboard') {
      return location.pathname === '/' || location.pathname === '/dashboard';
    }
    return location.pathname === path;
  };

  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  return (
    <header className="sticky top-0 z-50 px-4 sm:px-8 py-3.5 backdrop-blur-2xl bg-[#05060f]/80 border-b border-[rgba(186,215,247,0.12)]">
      <div className="max-w-[1200px] mx-auto flex items-center justify-between">
        {/* Left: Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-full bg-[rgba(186,214,247,0.06)] border border-[rgba(186,215,247,0.14)] p-0.5 group-hover:border-[#663af3] transition-all duration-300 flex items-center justify-center text-[#F0F6FF]">
            <ShieldCheck className="w-4 h-4 text-[#F0F6FF]" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-heading font-semibold authkit-heading-gradient tracking-tight flex items-center gap-1.5">
              Python <span className="font-light text-[#8AA4C4]">Quest</span>
            </span>
            <span className="font-eyebrow text-[9px] text-[#526884] uppercase tracking-widest -mt-1">
              AUTHKIT ENGINE
            </span>
          </div>
        </Link>

        {/* Center: Frosted Navigation Pill (Desktop) */}
        <nav className="hidden md:flex items-center gap-1 p-1 rounded-full bg-[rgba(186,214,247,0.03)] border border-[rgba(186,215,247,0.12)] backdrop-blur-xl">
          <Link
            to="/"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all duration-300 flex items-center gap-2 ${
              isActive('/')
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'text-[#8AA4C4] hover:text-[#F0F6FF] hover:bg-[rgba(186,214,247,0.04)]'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-[#8AA4C4]" /> Dashboard
          </Link>
          <Link
            to="/path"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all duration-300 flex items-center gap-2 ${
              isActive('/path')
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'text-[#8AA4C4] hover:text-[#F0F6FF] hover:bg-[rgba(186,214,247,0.04)]'
            }`}
          >
            <Map className="w-3.5 h-3.5 text-[#8AA4C4]" /> Guided Path
          </Link>
          <Link
            to="/explore"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all duration-300 flex items-center gap-2 ${
              isActive('/explore')
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'text-[#8AA4C4] hover:text-[#F0F6FF] hover:bg-[rgba(186,214,247,0.04)]'
            }`}
          >
            <Compass className="w-3.5 h-3.5 text-[#8AA4C4]" /> Explore Topics
          </Link>
        </nav>

        {/* Right: Gamified Stats */}
        <div className="flex items-center gap-2 sm:gap-3">
          {user ? (
            <>
              {/* Streak Pill */}
              <div className="flex items-center gap-1.5 bg-[rgba(186,214,247,0.03)] border border-[rgba(186,215,247,0.12)] px-3 py-1.5 rounded-full text-[#F0F6FF] text-xs font-mono">
                <Flame className="w-3.5 h-3.5 text-[#663af3] fill-[#663af3]" />
                <span>{user?.current_streak || 1}d Streak</span>
              </div>

              {/* XP Pill */}
              <div className="flex items-center gap-1.5 bg-[rgba(186,214,247,0.03)] border border-[rgba(186,215,247,0.12)] px-3 py-1.5 rounded-full text-[#C8DCF5] text-xs font-mono">
                <Zap className="w-3.5 h-3.5 text-[#8AA4C4]" />
                <span>{user?.xp || 0} XP</span>
              </div>

              {/* Level Pill - Void Violet Badge */}
              <div className="hidden sm:flex items-center gap-1.5 bg-[#663af3] text-white px-3.5 py-1.5 rounded-md text-xs font-semibold shadow-[0_0_15px_rgba(102,58,243,0.4)]">
                <User className="w-3.5 h-3.5" />
                <span>Level {user?.level || 1}</span>
              </div>
            </>
          ) : (
            <Link
              to="/login"
              className="flex items-center gap-2 px-5 py-2 rounded-md bg-[#663af3] text-white text-xs font-semibold hover:bg-[#542be3] transition-all shadow-[0_0_20px_rgba(102,58,243,0.4)]"
            >
              <LogIn className="w-3.5 h-3.5" /> Sign In
            </Link>
          )}

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-md bg-[rgba(186,214,247,0.04)] border border-[rgba(186,215,247,0.12)] text-[#F0F6FF] hover:bg-[rgba(186,214,247,0.08)]"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Nav Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-3 pt-3 border-t border-[rgba(186,215,247,0.12)] space-y-2 animate-pq-fade-up">
          <Link
            to="/"
            className={`block px-4 py-2.5 rounded-md text-sm font-medium transition-colors ${
              isActive('/') ? 'bg-[#663af3] text-white' : 'text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.05)]'
            }`}
          >
            Dashboard
          </Link>
          <Link
            to="/path"
            className={`block px-4 py-2.5 rounded-md text-sm font-medium transition-colors ${
              isActive('/path') ? 'bg-[#663af3] text-white' : 'text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.05)]'
            }`}
          >
            Guided Path
          </Link>
          <Link
            to="/explore"
            className={`block px-4 py-2.5 rounded-md text-sm font-medium transition-colors ${
              isActive('/explore') ? 'bg-[#663af3] text-white' : 'text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.05)]'
            }`}
          >
            Explore Topics
          </Link>
        </div>
      )}
    </header>
  );
};

export default Navbar;
