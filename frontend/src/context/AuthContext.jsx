import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService, leaderboardService } from '../services/api';

const AuthContext = createContext(null);

const DEFAULT_GUEST_USER = {
  id: 1,
  username: "guest_coder",
  full_name: "Python Coder",
  email: "guest@pythonquest.dev",
  role: "student",
  level: 1,
  xp: 0,
  current_streak: 1
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(DEFAULT_GUEST_USER);
  const [loading, setLoading] = useState(true);
  const [progressSummary, setProgressSummary] = useState(null);

  const fetchUser = async () => {
    try {
      const res = await authService.getMe();
      setUser(res.data);
      const progRes = await leaderboardService.getProgressSummary();
      setProgressSummary(progRes.data);
    } catch (err) {
      console.warn('Backend unavailable, using default guest session', err);
      setUser(DEFAULT_GUEST_USER);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const reloadProgress = async () => {
    try {
      const res = await authService.getMe();
      setUser(res.data);
      const progRes = await leaderboardService.getProgressSummary();
      setProgressSummary(progRes.data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, progressSummary, reloadProgress }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
