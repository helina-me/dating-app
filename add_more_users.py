from app import app
from models import db, User
import bcrypt
import random

# Generate 30 realistic users (15 male, 15 female)
male_names = ['Abel', 'Bereket', 'Dawit', 'Ermias', 'Fikru', 'Girma', 'Henok', 'Kaleb', 'Mekonnen', 'Nahom', 'Samuel', 'Tekle', 'Yonas', 'Zerihun', 'Biruk']
female_names = ['Adanech', 'Betty', 'Chaltu', 'Desta', 'Eden', 'Frehiwot', 'Genet', 'Hiwot', 'Kidist', 'Liya', 'Mahlet', 'Selam', 'Tigist', 'Yordanos', 'Meron']

interests_pool = ['Technology', 'Music', 'Movies', 'Sports', 'Travel', 'Cooking', 'Gaming', 'Reading', 'Art', 'Fashion']

def create_user(email, name, age, height, gender, occupation, interests):
    return User(
        email=email,
        password=bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode(),
        full_name=name,
        age=age,
        height_cm=height,
        gender=gender,
        occupation=occupation,
        interests=interests,
        smoking=random.choice(['Never', 'Occasionally']),
        drinking=random.choice(['Never', 'Socially']),
        exercise=random.choice(['Never', '1-2x/week', '3-4x/week']),
        religion='Orthodox Christian',
        politics=random.choice(['Liberal', 'Moderate', 'Conservative']),
        wants_kids=random.choice(['Yes', 'Maybe']),
        min_age_pref=18,
        max_age_pref=45,
        min_height_pref=150,
        max_height_pref=200,
        relationship_goal=random.choice(['Long-term', 'Marriage', 'Friendship']),
        bio=f"Hi, I'm {name}. I love {random.choice(interests_pool)} and having good conversations.",
        is_active=True
    )

users = []

# Male users
for i, name in enumerate(male_names[:15]):
    email = f"male{i+1}@test.com"
    age = random.randint(22, 38)
    height = random.randint(168, 188)
    interests = ','.join(random.sample(interests_pool, 3))
    users.append(create_user(email, name, age, height, 'Male', 'Professional', interests))

# Female users
for i, name in enumerate(female_names[:15]):
    email = f"female{i+1}@test.com"
    age = random.randint(20, 35)
    height = random.randint(155, 175)
    interests = ','.join(random.sample(interests_pool, 3))
    users.append(create_user(email, name, age, height, 'Female', 'Professional', interests))

with app.app_context():
    for user in users:
        existing = User.query.filter_by(email=user.email).first()
        if not existing:
            db.session.add(user)
    db.session.commit()
    print(f"Added {len(users)} users. Total users: {User.query.count()}")