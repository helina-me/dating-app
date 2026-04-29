import React, { useState, useEffect } from 'react';

function ProfileForm({ token, user }) {
  const [formData, setFormData] = useState({
    bio: '',
    perfect_match_desc: '',
    relationship_goal: 'Long-term',
    min_age_pref: 18,
    max_age_pref: 100,
    min_height_pref: 140,
    max_height_pref: 210,
    smoking: 'Never',
    drinking: 'Never',
    exercise: 'Never',
    religion: '',
    politics: 'Moderate',
    wants_kids: 'Maybe',
    education: '',
    occupation: '',
    income: '',
    photo_url: ''
  });

  const [photoPreview, setPhotoPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        bio: user.bio || '',
        perfect_match_desc: user.perfect_match_desc || '',
        relationship_goal: user.relationship_goal || 'Long-term',
        min_age_pref: user.min_age_pref || 18,
        max_age_pref: user.max_age_pref || 100,
        min_height_pref: user.min_height_pref || 140,
        max_height_pref: user.max_height_pref || 210,
        smoking: user.smoking || 'Never',
        drinking: user.drinking || 'Never',
        exercise: user.exercise || 'Never',
        religion: user.religion || '',
        politics: user.politics || 'Moderate',
        wants_kids: user.wants_kids || 'Maybe',
        education: user.education || '',
        occupation: user.occupation || '',
        income: user.income || '',
        photo_url: user.photo_url || ''
      });
      setPhotoPreview(user.photo_url || null);
    }
  }, [user]);

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const dataUrl = reader.result;
        setPhotoPreview(dataUrl);
        setFormData(prev => ({ ...prev, photo_url: dataUrl }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/users/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (res.ok) {
        alert('Profile updated successfully!');
        // Update local user object if needed
        if (data.photo_url) setPhotoPreview(data.photo_url);
      } else {
        alert('Update failed: ' + JSON.stringify(data));
      }
    } catch (error) {
      alert('Update failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>✨ Complete Your Profile</h2>
      
      {/* Photo Upload */}
      <div className="photo-upload">
        <img 
          src={photoPreview || "https://api.dicebear.com/9.x/avataaars/svg?seed=default"} 
          alt="Profile" 
          className="photo-preview"
        />
        <label className="photo-label">
          📸 Upload Photo
          <input 
            type="file" 
            className="photo-input"
            accept="image/*"
            onChange={handlePhotoUpload}
          />
        </label>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Bio Section */}
        <div className="form-group">
          <label>📝 About Me</label>
          <textarea rows="4" value={formData.bio} onChange={(e) => setFormData({ ...formData, bio: e.target.value })} />
        </div>
        <div className="form-group">
          <label>💕 My Perfect Match</label>
          <textarea rows="4" value={formData.perfect_match_desc} onChange={(e) => setFormData({ ...formData, perfect_match_desc: e.target.value })} />
        </div>
        {/* Work & Education */}
        <div className="form-group">
          <label>💼 Occupation</label>
          <input type="text" value={formData.occupation} onChange={(e) => setFormData({ ...formData, occupation: e.target.value })} />
        </div>
        <div className="form-group">
          <label>🎓 Education</label>
          <select value={formData.education} onChange={(e) => setFormData({ ...formData, education: e.target.value })}>
            <option value="">Select</option>
            <option>High School</option>
            <option>Bachelor's Degree</option>
            <option>Master's Degree</option>
            <option>PhD</option>
          </select>
        </div>
        <div className="form-group">
          <label>💰 Income</label>
          <select value={formData.income} onChange={(e) => setFormData({ ...formData, income: e.target.value })}>
            <option value="">Select</option>
            <option>Under 50k ETB</option>
            <option>50k - 150k ETB</option>
            <option>150k - 300k ETB</option>
            <option>300k - 500k ETB</option>
            <option>500k+ ETB</option>
          </select>
        </div>
        {/* Lifestyle */}
        <div className="form-group">
          <label>🚬 Smoking</label>
          <select value={formData.smoking} onChange={(e) => setFormData({ ...formData, smoking: e.target.value })}>
            <option>Never</option><option>Occasionally</option><option>Regularly</option>
          </select>
        </div>
        <div className="form-group">
          <label>🍷 Drinking</label>
          <select value={formData.drinking} onChange={(e) => setFormData({ ...formData, drinking: e.target.value })}>
            <option>Never</option><option>Socially</option><option>Regularly</option>
          </select>
        </div>
        <div className="form-group">
          <label>🏃 Exercise</label>
          <select value={formData.exercise} onChange={(e) => setFormData({ ...formData, exercise: e.target.value })}>
            <option>Never</option><option>1-2x/week</option><option>3-4x/week</option><option>5+ x/week</option>
          </select>
        </div>
        {/* Values */}
        <div className="form-group">
          <label>⛪ Religion</label>
          <input type="text" value={formData.religion} onChange={(e) => setFormData({ ...formData, religion: e.target.value })} />
        </div>
        <div className="form-group">
          <label>🗳️ Politics</label>
          <select value={formData.politics} onChange={(e) => setFormData({ ...formData, politics: e.target.value })}>
            <option>Liberal</option><option>Moderate</option><option>Conservative</option><option>Apolitical</option>
          </select>
        </div>
        <div className="form-group">
          <label>👶 Want Children?</label>
          <select value={formData.wants_kids} onChange={(e) => setFormData({ ...formData, wants_kids: e.target.value })}>
            <option>Yes</option><option>No</option><option>Maybe</option>
          </select>
        </div>
        <div className="form-group">
          <label>💍 Relationship Goal</label>
          <select value={formData.relationship_goal} onChange={(e) => setFormData({ ...formData, relationship_goal: e.target.value })}>
            <option>Long-term</option><option>Marriage</option><option>Casual</option><option>Friendship</option>
          </select>
        </div>
        {/* Preferences */}
        <div className="form-group">
          <label>📅 Preferred Age Range</label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input type="number" value={formData.min_age_pref} onChange={(e) => setFormData({ ...formData, min_age_pref: parseInt(e.target.value) })} min="18" max="100" />
            <span>to</span>
            <input type="number" value={formData.max_age_pref} onChange={(e) => setFormData({ ...formData, max_age_pref: parseInt(e.target.value) })} min="18" max="100" />
          </div>
        </div>
        <div className="form-group">
          <label>📏 Preferred Height (cm)</label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input type="number" value={formData.min_height_pref} onChange={(e) => setFormData({ ...formData, min_height_pref: parseInt(e.target.value) })} min="140" max="210" />
            <span>to</span>
            <input type="number" value={formData.max_height_pref} onChange={(e) => setFormData({ ...formData, max_height_pref: parseInt(e.target.value) })} min="140" max="210" />
          </div>
        </div>
        <button type="submit" disabled={loading}>{loading ? 'Saving...' : '💾 Save Profile'}</button>
      </form>
    </div>
  );
}

export default ProfileForm;