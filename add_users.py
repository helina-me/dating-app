from app import app
from models import db, User
import bcrypt
import random

users_data = [
    # Male users
    ('john@test.com', 'John Doe', 28, 180, 'Male', 'Engineer', 'Technology,Sports'),
    ('mike@test.com', 'Mike Smith', 32, 175, 'Male', 'Developer', 'Gaming,Music'),
    ('alex@test.com', 'Alex Brown', 26, 178, 'Male', 'Designer', 'Art,Travel'),
    # Female users
    ('jane@test.com', 'Jane Doe', 25, 165, 'Female', 'Doctor', 'Reading,Yoga'),
    ('lisa@test.com', 'Lisa Wong', 27, 168, 'Female', 'Teacher', 'Music,Cooking'),
    ('anna@test.com', 'Anna Lee', 24, 162, 'Female', 'Student', 'Travel,Photography'),
]

with app.app_context():
    for email, name, age, height, gender, occ, interests in users_data:
        existing = User.query.filter_by(email=email).first()
        if existing:
            continue
        user = User(
            email=email,
            password=bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode(),
            full_name=name,
            age=age,
            height_cm=height,
            gender=gender,
            occupation=occ,
            interests=interests,
            min_age_pref=18,
            max_age_pref=40,
            min_height_pref=150,
            max_height_pref=200,
            relationship_goal='Long-term',
            bio=f"Hi, I'm {name}. Looking for meaningful connections.",
            is_active=True
        )
        db.session.add(user)
    db.session.commit()
    print(f"Added {len(users_data)} users. Total users: {User.query.count()}")