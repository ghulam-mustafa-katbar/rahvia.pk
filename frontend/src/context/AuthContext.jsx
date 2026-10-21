import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, setAuthTokens, clearAuthTokens, getAuthToken } from '../api/client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('rahvia_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [studentId, setStudentId] = useState(() => localStorage.getItem('rahvia_student_id') || null);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState(() => localStorage.getItem('rahvia_lang') || 'en');

  const toggleLanguage = () => {
    const next = language === 'en' ? 'ur' : 'en';
    setLanguage(next);
    localStorage.setItem('rahvia_lang', next);
  };

  useEffect(() => {
    const checkAuth = async () => {
      const token = getAuthToken();
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const userData = await api.getCurrentUser();
        if (userData && userData.email) {
          setUser(userData);
          localStorage.setItem('rahvia_user', JSON.stringify(userData));
          if (userData.student_id) {
            setStudentId(userData.student_id);
            localStorage.setItem('rahvia_student_id', userData.student_id);
          }
        } else {
          clearAuthTokens();
          setUser(null);
        }
      } catch (err) {
        console.error('Auth verification error:', err);
        clearAuthTokens();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();

    const handleUnauthorized = () => {
      setUser(null);
      setStudentId(null);
    };

    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, []);

  const login = async (email, password) => {
    const res = await api.login({ email, password });
    if (res && res.tokens) {
      setAuthTokens(res.tokens.access, res.tokens.refresh);
      setUser(res.user);
      localStorage.setItem('rahvia_user', JSON.stringify(res.user));
      if (res.student_id) {
        setStudentId(res.student_id);
        localStorage.setItem('rahvia_student_id', res.student_id);
      }
      return { success: true, user: res.user };
    }
    return { success: false, error: res?.detail || res?.error || 'Login failed' };
  };

  const register = async (formData) => {
    const res = await api.register(formData);
    if (res && res.tokens) {
      setAuthTokens(res.tokens.access, res.tokens.refresh);
      setUser(res.user);
      localStorage.setItem('rahvia_user', JSON.stringify(res.user));
      // fetch student profile to get student_id
      try {
        const me = await api.getCurrentUser();
        if (me?.student_id) {
          setStudentId(me.student_id);
          localStorage.setItem('rahvia_student_id', me.student_id);
        }
      } catch (e) {}
      return { success: true, user: res.user };
    }
    return { success: false, error: res };
  };

  const logout = () => {
    clearAuthTokens();
    localStorage.removeItem('rahvia_student_id');
    setUser(null);
    setStudentId(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        studentId,
        loading,
        language,
        toggleLanguage,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        isStudent: user?.role === 'STUDENT',
        isCounselor: user?.role === 'COUNSELOR',
        isAdmin: user?.role === 'ADMIN' || user?.is_staff,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
