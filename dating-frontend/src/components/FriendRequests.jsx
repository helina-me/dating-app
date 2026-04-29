import React, { useState, useEffect } from 'react';

function FriendRequests({ token }) {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRequests = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/friend-requests/received', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setRequests(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const respond = async (requestId, action) => {
    try {
      const res = await fetch('http://localhost:5000/api/friend-request/respond', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ request_id: requestId, action })
      });
      if (res.ok) fetchRequests(); // refresh list
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  if (loading) return <div className="form-container">Loading...</div>;

  return (
    <div className="form-container">
      <h2>💌 Friend Requests</h2>
      {requests.length === 0 ? (
        <p>No pending friend requests.</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {requests.map(req => (
            <li key={req.id} style={{ marginBottom: '20px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                <img src={req.from_user_photo || `https://api.dicebear.com/9.x/avataaars/svg?seed=${req.from_user_id}`} alt="" style={{ width: '50px', height: '50px', borderRadius: '50%' }} />
                <div style={{ flex: 1 }}><strong>{req.from_user_name}</strong> sent you a friend request.</div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button onClick={() => respond(req.id, 'accept')} style={{ background: '#4CAF50' }}>Accept</button>
                  <button onClick={() => respond(req.id, 'reject')} style={{ background: '#f44336' }}>Reject</button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default FriendRequests;