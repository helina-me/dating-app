from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Demographics
    age = db.Column(db.Integer)
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Float)
    gender = db.Column(db.String(20))
    
    # Professional
    education = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    income = db.Column(db.String(50))
    
    # Lifestyle
    smoking = db.Column(db.String(20))
    drinking = db.Column(db.String(20))
    exercise = db.Column(db.String(30))
    interests = db.Column(db.String(500))
    
    # Values
    religion = db.Column(db.String(50))
    politics = db.Column(db.String(30))
    wants_kids = db.Column(db.String(10))
    
    # Preferences
    min_age_pref = db.Column(db.Integer, default=18)
    max_age_pref = db.Column(db.Integer, default=100)
    min_height_pref = db.Column(db.Integer, default=140)
    max_height_pref = db.Column(db.Integer, default=210)
    relationship_goal = db.Column(db.String(30))
    
    # Bio
    bio = db.Column(db.Text)
    perfect_match_desc = db.Column(db.Text)
    
    # Photo
    photo_url = db.Column(db.String(500), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    
    def get_interests_list(self):
        if self.interests:
            return [i.strip() for i in self.interests.split(',')]
        return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'age': self.age,
            'height_cm': self.height_cm,
            'gender': self.gender,
            'education': self.education,
            'occupation': self.occupation,
            'income': self.income,
            'smoking': self.smoking,
            'drinking': self.drinking,
            'exercise': self.exercise,
            'interests': self.get_interests_list(),
            'religion': self.religion,
            'politics': self.politics,
            'wants_kids': self.wants_kids,
            'min_age_pref': self.min_age_pref,
            'max_age_pref': self.max_age_pref,
            'min_height_pref': self.min_height_pref,
            'max_height_pref': self.max_height_pref,
            'relationship_goal': self.relationship_goal,
            'bio': self.bio,
            'perfect_match_desc': self.perfect_match_desc,
            'photo_url': self.photo_url
        }

class Interaction(db.Model):
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(20))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)