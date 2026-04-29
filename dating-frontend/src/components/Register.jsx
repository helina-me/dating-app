import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SimpleRegister({ setToken }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    age: 25,
    height_cm: 170,
    gender: 'Male',
    interests: []
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (data.token) {
        localStorage.setItem('token', data.token);
        setToken(data.token);
        navigate('/profile');
      } else {
        alert('Registration failed: ' + JSON.stringify(data));
      }
    } catch (error) {
      alert('Registration failed: ' + error.message);
    }
  };

  return (
    <div style={{ background: 'white', borderRadius: '10px', padding: '30px', maxWidth: '500px', margin: '50px auto' }}>
      <h2>Simple Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" onChange={(e) => setFormData({...formData, email: e.target.value})} required style={{ width: '100%', padding: '10px', margin: '10px 0' }} />
        <input type="password" placeholder="Password" onChange={(e) => setFormData({...formData, password: e.target.value})} required style={{ width: '100%', padding: '10px', margin: '10px 0' }} />
        <input type="text" placeholder="Full Name" onChange={(e) => setFormData({...formData, full_name: e.target.value})} required style={{ width: '100%', padding: '10px', margin: '10px 0' }} />
        <input type="number" placeholder="Age" onChange={(e) => setFormData({...formData, age: parseInt(e.target.value)})} required style={{ width: '100%', padding: '10px', margin: '10px 0' }} />
        <input type="number" placeholder="Height cm" onChange={(e) => setFormData({...formData, height_cm: parseInt(e.target.value)})} required style={{ width: '100%', padding: '10px', margin: '10px 0' }} />
        <select onChange={(e) => setFormData({...formData, gender: e.target.value})} style={{ width: '100%', padding: '10px', margin: '10px 0' }}>
          <option>Male</option>
          <option>Female</option>
        </select>
        <button type="submit" style={{ width: '100%', padding: '12px', background: '#667eea', color: 'white', border: 'none', borderRadius: '5px' }}>Register</button>
      </form>
    </div>
  );
}

export default SimpleRegister;