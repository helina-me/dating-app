import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def prepare_features(df):
    """Prepare features for ML model"""
    features = []
    labels = []
    
    # Create pairs of users (simulating likes/dislikes)
    users = df.to_dict('records')
    
    for i, user1 in enumerate(users):
        for j, user2 in enumerate(users):
            if i >= j:
                continue
            
            # Calculate feature differences
            feature_vector = []
            
            # Age difference
            age_diff = abs(user1['age'] - user2['age']) / 50
            feature_vector.append(age_diff)
            
            # Height difference
            height_diff = abs(user1['height_cm'] - user2['height_cm']) / 50
            feature_vector.append(height_diff)
            
            # Age preference match
            age_pref_match = 1 if (user1['min_age_pref'] <= user2['age'] <= user1['max_age_pref']) else 0
            feature_vector.append(age_pref_match)
            
            # Height preference match
            height_pref_match = 1 if (user1['min_height_pref'] <= user2['height_cm'] <= user1['max_height_pref']) else 0
            feature_vector.append(height_pref_match)
            
            # Same education
            same_education = 1 if user1['education'] == user2['education'] else 0
            feature_vector.append(same_education)
            
            # Same smoking
            same_smoking = 1 if user1['smoking'] == user2['smoking'] else 0
            feature_vector.append(same_smoking)
            
            # Same drinking
            same_drinking = 1 if user1['drinking'] == user2['drinking'] else 0
            feature_vector.append(same_drinking)
            
            # Same exercise
            same_exercise = 1 if user1['exercise'] == user2['exercise'] else 0
            feature_vector.append(same_exercise)
            
            # Same politics
            same_politics = 1 if user1['politics'] == user2['politics'] else 0
            feature_vector.append(same_politics)
            
            # Same wants_kids
            same_kids = 1 if user1['wants_kids'] == user2['wants_kids'] else 0
            feature_vector.append(same_kids)
            
            # Interest similarity (Jaccard)
            interests1 = set(user1['interests'].split(',')) if isinstance(user1['interests'], str) else set()
            interests2 = set(user2['interests'].split(',')) if isinstance(user2['interests'], str) else set()
            if interests1 and interests2:
                intersection = len(interests1 & interests2)
                union = len(interests1 | interests2)
                interest_sim = intersection / union if union > 0 else 0
            else:
                interest_sim = 0
            feature_vector.append(interest_sim)
            
            # Create label (1 = compatible, 0 = not)
            # Rule-based: compatible if interest_sim > 0.3 AND age_diff < 0.3
            label = 1 if (interest_sim > 0.3 and age_diff < 0.3) else 0
            labels.append(label)
            features.append(feature_vector)
    
    return np.array(features), np.array(labels)

def train_model():
    """Train the compatibility model"""
    print("Loading data...")
    df = pd.read_csv('users_data.csv')
    print(f"Loaded {len(df)} users")
    
    print("Preparing features...")
    X, y = prepare_features(df)
    print(f"Created {len(X)} user pairs")
    print(f"Positive samples: {sum(y)}")
    print(f"Negative samples: {len(y) - sum(y)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV accuracy: {cv_scores.mean():.3f}")
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_names = [
        'age_diff', 'height_diff', 'age_pref_match', 'height_pref_match',
        'same_education', 'same_smoking', 'same_drinking', 'same_exercise',
        'same_politics', 'same_kids', 'interest_similarity'
    ]
    importance = model.feature_importances_
    print("\nFeature Importance:")
    for name, imp in sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {imp:.3f}")
    
    # Save model and scaler
    os.makedirs('ml/models', exist_ok=True)
    joblib.dump(model, 'ml/models/compatibility_model.pkl')
    joblib.dump(scaler, 'ml/models/scaler.pkl')
    print("\nModel saved to ml/models/compatibility_model.pkl")
    
    return model, scaler

if __name__ == '__main__':
    train_model()