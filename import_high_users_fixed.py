# import_high_users_fixed.py
import pandas as pd
from app import app
from models import db, User
import bcrypt
import random

df = pd.read_csv('high_match_users.csv')  # your 30‑user CSV

with app.app_context():
    for _, row in df.iterrows():
        existing = User.query.filter_by(email=row['email']).first()
        if existing:
            continue
        
        # Assign gender‑appropriate photo
        if row['gender'] == 'Male':
            photo = f"https://randomuser.me/api/portraits/men/{random.randint(1,99)}.jpg"
        else:
            photo = f"https://randomuser.me/api/portraits/women/{random.randint(1,99)}.jpg"
        
        user = User(
            email=row['email'],
            password=bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode(),
            full_name=row['full_name'],
            age=row['age'],
            height_cm=row['height_cm'],
            gender=row['gender'],
            education=row['education'],
            occupation=row['occupation'],
            income=row['income'],
            smoking=row['smoking'],
            drinking=row['drinking'],
            exercise=row['exercise'],
            interests=row['interests'],
            religion=row['religion'],
            politics=row['politics'],
            wants_kids=row['wants_kids'],
            min_age_pref=row['min_age_pref'],
            max_age_pref=row['max_age_pref'],
            min_height_pref=row['min_height_pref'],
            max_height_pref=row['max_height_pref'],
            relationship_goal=row['relationship_goal'],
            bio=row['bio'],
            photo_url=photo
        )
        db.session.add(user)
    db.session.commit()
    print("Imported users with correct gender photos")