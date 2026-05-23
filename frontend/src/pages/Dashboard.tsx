import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';

export const Dashboard = () => {
  const { token, logout } = useAuth();
  const [user, setUser] = useState<{email: string} | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch('/api/users/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (res.ok) {
          const data = await res.json();
          setUser(data);
        } else {
          logout(); // Invalid token
        }
      } catch (err) {
        console.error('Failed to fetch user', err);
      }
    };
    
    if (token) {
      fetchUser();
    }
  }, [token, logout]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Dashboard Placeholder</h2>
      {user ? <p>Welcome, {user.email}!</p> : <p>Loading...</p>}
      <button onClick={logout}>Logout</button>
    </div>
  );
};
