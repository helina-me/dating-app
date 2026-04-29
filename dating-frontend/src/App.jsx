import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import ProfileForm from './components/ProfileForm';
import MatchRecommendations from './components/MatchRecommendations';
import Navbar from './components/Navbar';
import FriendRequests from './components/FriendRequests';
import ChatPage from './components/ChatPage';
import FriendsList from './components/FriendsList.jsx';

// Error Boundary Component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="form-container" style={{ textAlign: 'center', marginTop: '50px' }}>
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap', marginTop: '20px', textAlign: 'left' }}>
            <summary>Error details</summary>
            {this.state.error && this.state.error.toString()}
          </details>
          <button onClick={() => window.location.reload()} style={{ marginTop: '20px' }}>
            Refresh Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      fetchUser();
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to fetch user');
      const data = await res.json();
      setUser(data);
      localStorage.setItem('userId', data.id);
    } catch (error) {
      console.error(error);
      localStorage.removeItem('token');
      setToken(null);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setToken(null);
    setUser(null);
  };

  return (
    <BrowserRouter>
      <Navbar user={user} onLogout={handleLogout} />
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
        <ErrorBoundary>
          <Routes>
            <Route path="/login" element={<Login setToken={setToken} />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={
              token ? <ProfileForm token={token} user={user} /> : <Navigate to="/login" />
            } />
            <Route path="/matches" element={
              token ? <MatchRecommendations token={token} user={user} /> : <Navigate to="/login" />
            } />
            <Route path="/friend-requests" element={
              token ? <FriendRequests token={token} /> : <Navigate to="/login" />
            } />
            <Route path="/chat" element={
              token ? <ChatPage token={token} /> : <Navigate to="/login" />
            } />
            <Route path="/friends" element={
  token ? <FriendsList token={token} /> : <Navigate to="/login" />
} />

            <Route path="/" element={<Navigate to="/matches" />} />
          </Routes>
        </ErrorBoundary>
      </div>
    </BrowserRouter>
  );
}

export default App;