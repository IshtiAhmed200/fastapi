import { createContext, useState } from 'react';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    if (typeof window === 'undefined') return null;
    try {
      const stored = localStorage.getItem('user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      localStorage.removeItem('user');
      return null;
    }
  });

  const login = (userData, token) => {
    const userWithToken = { ...userData, token };
    setUser(userWithToken);
    localStorage.setItem('user', JSON.stringify(userWithToken));
    localStorage.setItem('token', token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  const register = (userData, token) => {
    const userWithToken = { ...userData, token };
    setUser(userWithToken);
    localStorage.setItem('user', JSON.stringify(userWithToken));
    localStorage.setItem('token', token);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}