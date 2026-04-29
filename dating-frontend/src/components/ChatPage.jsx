import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';

function ChatPage({ token }) {
  const [searchParams] = useSearchParams();
  const preselectedUserId = searchParams.get('userId');

  const [conversations, setConversations] = useState([]);
  const [selectedConv, setSelectedConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  // Fetch conversations
  const fetchConversations = async () => {
    const res = await fetch('http://localhost:5000/api/conversations', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    setConversations(data);
    setLoading(false);

    // If preselectedUserId, find or create conversation
    if (preselectedUserId && !selectedConv) {
      const existing = data.find(c => c.other_user.id == preselectedUserId);
      if (existing) {
        setSelectedConv(existing);
        fetchMessages(existing.conversation_id);
      } else {
        // need to create a conversation by sending a dummy message? No, just select a new conversation object
        // We'll create it when user sends first message, but for UI we can create a placeholder
        setSelectedConv({
          conversation_id: null,
          other_user: { id: parseInt(preselectedUserId), full_name: 'Loading...' }
        });
      }
    }
  };

  const fetchMessages = async (convId) => {
    if (!convId) return;
    const res = await fetch(`http://localhost:5000/api/messages/${convId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    setMessages(data);
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;
    let toUserId;
    let convId = selectedConv?.conversation_id;
    if (!convId) {
      // new conversation: need toUserId
      toUserId = selectedConv.other_user.id;
    } else {
      // existing conversation: get other user id from selectedConv
      toUserId = selectedConv.other_user.id;
    }
    const res = await fetch('http://localhost:5000/api/send-message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ to_user_id: toUserId, content: newMessage })
    });
    if (res.ok) {
      const data = await res.json();
      setNewMessage('');
      // refresh conversations list and messages
      fetchConversations();
      if (data.conversation_id) {
        fetchMessages(data.conversation_id);
        setSelectedConv(prev => ({ ...prev, conversation_id: data.conversation_id }));
      }
    }
  };

  useEffect(() => {
    fetchConversations();
    const interval = setInterval(() => {
      if (selectedConv?.conversation_id) fetchMessages(selectedConv.conversation_id);
      fetchConversations();
    }, 3000);
    return () => clearInterval(interval);
  }, [selectedConv]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (loading) return <div className="form-container">Loading chats...</div>;

  return (
    <div style={{ display: 'flex', height: '80vh', maxWidth: '1200px', margin: '20px auto', background: 'white', borderRadius: '10px', overflow: 'hidden' }}>
      {/* Conversations list */}
      <div style={{ width: '300px', borderRight: '1px solid #ddd', overflowY: 'auto' }}>
        <h3 style={{ padding: '15px', margin: 0, borderBottom: '1px solid #ddd' }}>💬 Chats</h3>
        {conversations.map(conv => (
          <div key={conv.conversation_id} onClick={() => { setSelectedConv(conv); fetchMessages(conv.conversation_id); }} style={{ padding: '15px', borderBottom: '1px solid #eee', cursor: 'pointer', background: selectedConv?.conversation_id === conv.conversation_id ? '#f0f0f0' : 'white' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <img src={conv.other_user.photo_url || `https://api.dicebear.com/9.x/avataaars/svg?seed=${conv.other_user.id}`} alt="" style={{ width: '40px', height: '40px', borderRadius: '50%' }} />
              <div style={{ flex: 1 }}>
                <strong>{conv.other_user.full_name}</strong>
                <div style={{ fontSize: '12px', color: '#666' }}>{conv.last_message || 'No messages yet'}</div>
              </div>
              {conv.unread_count > 0 && <span style={{ background: '#f44336', color: 'white', borderRadius: '50%', padding: '2px 6px', fontSize: '12px' }}>{conv.unread_count}</span>}
            </div>
          </div>
        ))}
      </div>

      {/* Chat area */}
      {selectedConv ? (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ padding: '15px', borderBottom: '1px solid #ddd', background: '#f5f5f5' }}>
            <strong>{selectedConv.other_user.full_name}</strong>
          </div>
          <div style={{ flex: 1, overflowY: 'auto', padding: '15px' }}>
            {messages.map(msg => (
              <div key={msg.id} style={{ textAlign: msg.sender_id === parseInt(localStorage.getItem('userId')) ? 'right' : 'left', marginBottom: '10px' }}>
                <div style={{ display: 'inline-block', background: msg.sender_id === parseInt(localStorage.getItem('userId')) ? '#667eea' : '#e0e0e0', color: msg.sender_id === parseInt(localStorage.getItem('userId')) ? 'white' : 'black', padding: '8px 12px', borderRadius: '15px', maxWidth: '70%' }}>
                  {msg.content}
                </div>
                <div style={{ fontSize: '10px', marginTop: '3px', color: '#999' }}>{new Date(msg.created_at).toLocaleTimeString()}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div style={{ padding: '15px', borderTop: '1px solid #ddd', display: 'flex', gap: '10px' }}>
            <input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} placeholder="Type a message..." style={{ flex: 1, padding: '10px', borderRadius: '20px', border: '1px solid #ccc' }} />
            <button onClick={sendMessage} style={{ width: 'auto', padding: '10px 20px' }}>Send</button>
          </div>
        </div>
      ) : (
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#999' }}>Select a conversation or friend to start chatting</div>
      )}
    </div>
  );
}

export default ChatPage;