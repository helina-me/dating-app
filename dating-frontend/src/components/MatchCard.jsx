import React, { useState } from 'react';

function MatchCard({ match, onLike, onDislike }) {
  const [showDetails, setShowDetails] = useState(false);

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FFC107';
    return '#9E9E9E';
  };
  const sendFriendRequest = async () => {
    try {
        const res = await fetch('http://localhost:5000/api/friend-request/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ to_user_id: match.user_id })
        });
        const data = await res.json();
        alert(data.message || data.error);
    } catch (err) {
        alert('Failed to send request');
    }
};

  const handleFriendRequest = async () => {
    try {
        const res = await fetch('http://localhost:5000/api/friend-request/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ to_user_id: match.user_id })
        });
        const data = await res.json();
        alert(data.message || 'Friend request sent!');
    } catch (error) {
        alert('Error sending request');
    }
};


  // Generate a consistent avatar URL using DiceBear (free, no broken images)
  const avatarUrl = match.photo_url || `https://api.dicebear.com/9.x/avataaars/svg?seed=${match.user_id}`;

  return (
    <div
      className="match-card"
      onMouseEnter={() => setShowDetails(true)}
      onMouseLeave={() => setShowDetails(false)}
    >
      <div className="match-photo">
        <img
          src={avatarUrl}
          alt={match.full_name}
          className="match-photo-placeholder"
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = `https://api.dicebear.com/9.x/avataaars/svg?seed=${match.user_id}&background=667eea`;
          }}
        />
        <div className="match-score" style={{ backgroundColor: getScoreColor(match.compatibility_score) }}>
          {match.compatibility_score}%
        </div>
      </div>
      <div className="match-info">
        <h3>{match.full_name}, {match.age}</h3>
        <div className="match-details">
          {match.height_cm}cm • {match.gender}
        </div>
        <p>{match.bio?.substring(0, 100)}...</p>

        {showDetails && (
          <>
            <div className="match-interests">
              {match.shared_interests?.slice(0, 5).map(interest => (
                <span key={interest} className="interest-tag">#{interest}</span>
              ))}
            </div>
            <div className="action-buttons">
              <button className="dislike-btn" onClick={onDislike}>✗ Pass</button>
              <button className="like-btn" onClick={onLike}>❤ Like</button>
              
              <button className="friend-btn" onClick={sendFriendRequest}>👥 Friend Request</button>


            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default MatchCard;