import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Terminal, Lock, User, Mail, ArrowRight } from 'lucide-react';

export const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register({
        username,
        email,
        full_name: fullName,
        password
      });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12 relative">
      {/* Background Hero Halo */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-[#663af3]/10 rounded-full blur-3xl pointer-events-none" />

      <div className="authkit-glass-card rounded-[16px] p-8 max-w-md w-full border border-[rgba(186,215,247,0.12)] bg-[rgba(186,214,247,0.03)] backdrop-blur-xl shadow-2xl relative z-10 space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-full bg-[rgba(102,58,243,0.15)] border border-[#663af3]/30 flex items-center justify-center text-[#663af3] shadow-[0_0_20px_rgba(102,58,243,0.3)] mx-auto mb-3">
            <Terminal className="w-6 h-6" />
          </div>
          <div className="font-mono text-[10px] tracking-[0.10em] text-[#8AA4C4] uppercase">
            BOOTCAMP REGISTRATION
          </div>
          <h2 className="text-2xl font-extrabold tracking-tight font-heading authkit-skywash-text">
            Join Python Quest
          </h2>
          <p className="text-xs text-[#8AA4C4] font-sans">
            Create your account to start earning XP & leveling up
          </p>
        </div>

        {error && (
          <div className="p-3 rounded-[6px] bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs text-center font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-[11px] font-mono tracking-[0.05em] uppercase text-[#8AA4C4] block">
              Username
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-[#8AA4C4] absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Choose a username"
                className="w-full bg-[#080917]/80 border border-[rgba(186,215,247,0.15)] rounded-[6px] pl-10 pr-4 py-2.5 text-xs text-[#F0F6FF] placeholder:text-[#5E7594] focus:outline-none focus:border-[#663af3] focus:ring-1 focus:ring-[#663af3] transition-all"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[11px] font-mono tracking-[0.05em] uppercase text-[#8AA4C4] block">
              Full Name
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-[#8AA4C4] absolute left-3.5 top-3" />
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Alex Mercer"
                className="w-full bg-[#080917]/80 border border-[rgba(186,215,247,0.15)] rounded-[6px] pl-10 pr-4 py-2.5 text-xs text-[#F0F6FF] placeholder:text-[#5E7594] focus:outline-none focus:border-[#663af3] focus:ring-1 focus:ring-[#663af3] transition-all"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[11px] font-mono tracking-[0.05em] uppercase text-[#8AA4C4] block">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-[#8AA4C4] absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex@bootcamp.com"
                className="w-full bg-[#080917]/80 border border-[rgba(186,215,247,0.15)] rounded-[6px] pl-10 pr-4 py-2.5 text-xs text-[#F0F6FF] placeholder:text-[#5E7594] focus:outline-none focus:border-[#663af3] focus:ring-1 focus:ring-[#663af3] transition-all"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[11px] font-mono tracking-[0.05em] uppercase text-[#8AA4C4] block">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#8AA4C4] absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#080917]/80 border border-[rgba(186,215,247,0.15)] rounded-[6px] pl-10 pr-4 py-2.5 text-xs text-[#F0F6FF] placeholder:text-[#5E7594] focus:outline-none focus:border-[#663af3] focus:ring-1 focus:ring-[#663af3] transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="authkit-btn-violet rounded-[6px] w-full py-3 text-xs font-semibold uppercase tracking-wider flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(102,58,243,0.4)] hover:shadow-[0_0_28px_rgba(102,58,243,0.6)] disabled:opacity-50 transition-all mt-2"
          >
            {loading ? 'Creating Account...' : <>Create Account <ArrowRight className="w-4 h-4" /></>}
          </button>
        </form>

        <p className="text-center text-xs text-[#8AA4C4] font-sans">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-[#C8DCF5] hover:text-[#F0F6FF] transition-colors underline underline-offset-2">
            Log In
          </Link>
        </p>
      </div>
    </div>
  );
};

