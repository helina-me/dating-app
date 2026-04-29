import React, { useState, useEffect } from 'react';
import MatchCard from './MatchCard';

function MatchRecommendations({ token, user }) {
  const [matches, setMatches] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
        const token = localStorage.getItem('token');
        const res = await fetch('http://localhost:5000/api/matches/recommendations', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`HTTP ${res.status}: ${errorText}`);
        }
        const data = await res.json();
        if (Array.isArray(data)) {
            setMatches(data);
        } else {
            console.error('Expected array, got:', data);
            setMatches([]);
        }
        setLoading(false);
    } catch (error) {
        console.error('Fetch error:', error);
        setMatches([]);
        setLoading(false);
    }
};

  const handleInteraction = async (targetUserId, action) => {
    try {
      await fetch('http://localhost:5000/api/matches/interact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ target_user_id: targetUserId, action })
      });
      setMatches(matches.filter(m => m.user_id !== targetUserId));
    } catch (error) {
      console.error(error);
    }
  };

  const filteredMatches = matches.filter(match => {
    if (filter === 'high') return match.compatibility_score >= 80;
    if (filter === 'medium') return match.compatibility_score >= 60 && match.compatibility_score < 80;
    if (filter === 'low') return match.compatibility_score < 60;
    return true;
  });

  if (loading) return <div style={{ textAlign: 'center', color: 'white', fontSize: '24px' }}>Finding your matches...</div>;

  return (
    <div>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button onClick={() => setFilter('all')} style={{ background: filter === 'all' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'white', color: filter === 'all' ? 'white' : '#333', padding: '8px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>All</button>
        <button onClick={() => setFilter('high')} style={{ background: filter === 'high' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'white', color: filter === 'high' ? 'white' : '#333', padding: '8px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>High (&gt;80%)</button>
        <button onClick={() => setFilter('medium')} style={{ background: filter === 'medium' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'white', color: filter === 'medium' ? 'white' : '#333', padding: '8px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Medium (60-80%)</button>
        <button onClick={() => setFilter('low')} style={{ background: filter === 'low' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'white', color: filter === 'low' ? 'white' : '#333', padding: '8px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Low (&lt;60%)</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '20px' }}>
        {filteredMatches.map(match => (
          <MatchCard key={match.user_id} match={match} onLike={() => handleInteraction(match.user_id, 'like')} onDislike={() => handleInteraction(match.user_id, 'dislike')} />
        ))}
      </div>
    </div>
  );
}

export default MatchRecommendations;