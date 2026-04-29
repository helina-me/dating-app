import pandas as pd
from app import app
from models import db, User
import bcrypt

df = pd.read_csv('high_match_users.csv')

with app.app_context():
    count = 0
    for _, row in df.iterrows():
        existing = User.query.filter_by(email=row['email']).first()
        if existing:
            continue
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
            bio=row['bio']
        )
        db.session.add(user)
        count += 1
    db.session.commit()
    print(f"Imported {count} high-compatibility users")