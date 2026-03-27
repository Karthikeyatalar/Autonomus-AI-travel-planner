'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Register() {
  const [formData, setFormData] = useState({ username: '', password: '', role: 'user' });
  const [error, setError] = useState('');
  const router = useRouter();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      const data = await res.json();
      if (res.ok) {
        router.push('/login');
      } else {
        setError(data.detail || 'Registration failed');
      }
    } catch (err) {
      setError('Check if backend is running');
    }
  };

  return (
    <div className="container" style={{ display: 'flex', justifyContent: 'center', marginTop: '4rem' }}>
      <form className="glass-panel" style={{ width: '100%', maxWidth: '450px' }} onSubmit={handleSubmit}>
        <h2 className="text-center" style={{ marginBottom: '2rem', color: 'var(--accent-pink)' }}>New Designation</h2>
        {error && <div style={{ background: 'rgba(255,0,85,0.1)', color: 'var(--accent-pink)', padding: '1rem', borderRadius: '8px', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        <div className="input-group">
          <label>Operator ID (Username)</label>
          <input type="text" name="username" required value={formData.username} onChange={handleChange} />
        </div>
        <div className="input-group">
          <label>Passcode</label>
          <input type="password" name="password" required value={formData.password} onChange={handleChange} />
        </div>
        <div className="input-group">
          <label>Security Clearance (Role)</label>
          <select name="role" required value={formData.role} onChange={handleChange}>
            <option value="user">Standard User</option>
            <option value="admin">System Admin</option>
          </select>
        </div>
        <button type="submit" className="primary-btn mt-2" style={{ background: 'linear-gradient(135deg, var(--accent-pink) 0%, var(--accent-neon) 100%)'}}>Register</button>
        <p className="text-center mt-2" style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>
          Already have credentials? <Link href="/login" style={{ color: 'var(--accent-pink)' }}>Login Here</Link>
        </p>
      </form>
    </div>
  );
}
