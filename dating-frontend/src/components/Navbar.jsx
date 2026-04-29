import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <h2>❤️ HeartMatch AI</h2>
      <div className="nav-links">
        {user ? (
          <>
            <Link to="/matches">✨ Matches</Link>
            <Link to="/profile">👤 Profile</Link>
            <Link to="/friend-requests">💌 Requests</Link>
<Link to="/chat">💬 Chat</Link>
<Link to="/friends">👥 Friends</Link>
            <button onClick={onLogout}>🚪 Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">🔐 Login</Link>
            <Link to="/register">📝 Register</Link>
            
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;