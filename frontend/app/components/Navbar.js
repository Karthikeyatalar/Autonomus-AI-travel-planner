'use client';

import Link from 'next/link';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar glass-panel">
      <div className="navbar-brand">
        <Link href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          <h2>✨ AI Travel</h2>
        </Link>
      </div>
      <div className="navbar-links">
        {user ? (
          <>
            <span className="welcome-text">Hi, {user.username}</span>
            {user.role === 'admin' && (
              <Link href="/admin">
                <button className="nav-button admin-button">Admin Portal</button>
              </Link>
            )}
            <button className="nav-button outline-button" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link href="/login">
              <button className="nav-button outline-button">Login</button>
            </Link>
            <Link href="/register">
              <button className="nav-button active-button">Register</button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
