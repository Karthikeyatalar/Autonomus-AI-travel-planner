'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../context/AuthContext';
import Link from 'next/link';

export default function Login() {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const router = useRouter();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const formBody = new URLSearchParams();
    formBody.append('username', formData.username);
    formBody.append('password', formData.password);

    try {
      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody.toString()
      });
      
      const data = await res.json();
      if (res.ok) {
        // Fetch user context
        const userRes = await fetch('http://localhost:8000/api/auth/me', {
          headers: { 'Authorization': `Bearer ${data.access_token}` }
        });
        const userData = await userRes.json();
        login(data.access_token, userData);
        router.push(userData.role === 'admin' ? '/admin' : '/');
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Check if backend is running');
    }
  };

  return (
    <div className="container" style={{ display: 'flex', justifyContent: 'center', marginTop: '4rem' }}>
      <form className="glass-panel" style={{ width: '100%', maxWidth: '450px' }} onSubmit={handleSubmit}>
        <h2 className="text-center" style={{ marginBottom: '2rem', color: 'var(--accent-neon)' }}>Access Terminal</h2>
        {error && <div style={{ background: 'rgba(255,0,85,0.1)', color: 'var(--accent-pink)', padding: '1rem', borderRadius: '8px', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        <div className="input-group">
          <label>Operator ID (Username)</label>
          <input type="text" name="username" required value={formData.username} onChange={handleChange} />
        </div>
        <div className="input-group">
          <label>Passcode</label>
          <input type="password" name="password" required value={formData.password} onChange={handleChange} />
        </div>
        <button type="submit" className="primary-btn mt-2">Initialize Link</button>
        <p className="text-center mt-2" style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>
          No access credentials? <Link href="/register" style={{ color: 'var(--accent-neon)' }}>Register Here</Link>
        </p>
      </form>
    </div>
  );
}
