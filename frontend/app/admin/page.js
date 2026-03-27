'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useRouter } from 'next/navigation';

export default function AdminPortal() {
  const { user, loading } = useAuth();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push('/login');
      } else if (user.role !== 'admin') {
        setError('ACCESS DENIED: Insufficient Security Clearance (Admin Only)');
      } else {
        fetchUsers();
      }
    }
  }, [user, loading, router]);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const res = await fetch('http://localhost:8000/api/admin/users', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setUsers(data);
      } else {
        setError('Failed to fetch user data. Clearance revoked.');
      }
    } catch (err) {
      setError('Communication with the backend server failed.');
    }
  };

  if (loading) return <div className="loading-indicator text-center" style={{ marginTop: '5rem', color: 'var(--accent-neon)' }}>Decrypting Admin Core...</div>;

  if (error) {
    return (
      <div className="container" style={{ marginTop: '5rem', textAlign: 'center' }}>
        <div className="glass-panel" style={{ border: '1px solid var(--accent-pink)', display: 'inline-block' }}>
          <h1 style={{ color: 'var(--accent-pink)', fontSize: '3rem', marginBottom: '1rem' }}>SYSTEM LOCKDOWN</h1>
          <p style={{ color: 'var(--text-dim)', fontSize: '1.2rem' }}>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={{ marginTop: '2rem' }}>
      <header className="mb-2">
        <h1 style={{ color: 'var(--accent-neon)' }}>Admin Core Terminal</h1>
        <p style={{ color: 'var(--text-dim)' }}>Global Overlook — Registered User Database</p>
      </header>
      
      <div className="glass-panel" style={{ padding: '2rem', borderRadius: '16px' }}>
        <h3 style={{ borderBottom: '1px solid var(--surface-border)', paddingBottom: '1rem' }}>Operator Identity Registry</h3>
        <div style={{ overflowX: 'auto' }}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>System ID</th>
                <th>Operator Name</th>
                <th>Security Level</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id}>
                  <td style={{ color: 'var(--text-dim)' }}>#{u.id.toString().padStart(4, '0')}</td>
                  <td style={{ fontWeight: 600 }}>{u.username}</td>
                  <td>
                    <span className={`badge ${u.role}`}>{u.role}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
