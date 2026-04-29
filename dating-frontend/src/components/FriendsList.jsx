import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function FriendsList({ token }) {
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchFriends();
  }, []);

  const fetchFriends = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/friends', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setFriends(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const startChat = (friendId) => {
    navigate(`/chat?userId=${friendId}`);
  };

  if (loading) return <div className="form-container">Loading friends...</div>;

  return (
    <div className="form-container">
      <h2>👥 My Friends</h2>
      {friends.length === 0 ? (
        <p>No friends yet. Send some friend requests!</p>
      ) : (
        <div style={{ display: 'grid', gap: '15px' }}>
          {friends.map(friend => (
            <div key={friend.id} style={{ display: 'flex', alignItems: 'center', gap: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
              <img src={friend.photo_url || `https://api.dicebear.com/9.x/avataaars/svg?seed=${friend.id}`} alt="" style={{ width: '50px', height: '50px', borderRadius: '50%' }} />
              <div style={{ flex: 1 }}>
                <strong>{friend.full_name}</strong><br />
                {friend.age} years old
              </div>
              <button onClick={() => startChat(friend.id)} style={{ background: '#667eea', width: 'auto', padding: '8px 15px' }}>
                💬 Message
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FriendsList;