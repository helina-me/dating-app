import pandas as pd
import numpy as np
import joblib

class CompatibilityPredictor:
    def __init__(self, model_path='ml/models/compatibility_model.pkl', scaler_path='ml/models/scaler.pkl'):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
    
    def prepare_single_pair(self, user1, user2):
        """Prepare features for a single user pair"""
        features = []
        
        # Age difference
        age_diff = abs(user1['age'] - user2['age']) / 50
        features.append(age_diff)
        
        # Height difference
        height_diff = abs(user1['height_cm'] - user2['height_cm']) / 50
        features.append(height_diff)
        
        # Age preference match
        age_pref_match = 1 if (user1['min_age_pref'] <= user2['age'] <= user1['max_age_pref']) else 0
        features.append(age_pref_match)
        
        # Height preference match
        height_pref_match = 1 if (user1['min_height_pref'] <= user2['height_cm'] <= user1['max_height_pref']) else 0
        features.append(height_pref_match)
        
        # Same education
        same_education = 1 if user1['education'] == user2['education'] else 0
        features.append(same_education)
        
        # Same smoking
        same_smoking = 1 if user1['smoking'] == user2['smoking'] else 0
        features.append(same_smoking)
        
        # Same drinking
        same_drinking = 1 if user1['drinking'] == user2['drinking'] else 0
        features.append(same_drinking)
        
        # Same exercise
        same_exercise = 1 if user1['exercise'] == user2['exercise'] else 0
        features.append(same_exercise)
        
        # Same politics
        same_politics = 1 if user1['politics'] == user2['politics'] else 0
        features.append(same_politics)
        
        # Same wants_kids
        same_kids = 1 if user1['wants_kids'] == user2['wants_kids'] else 0
        features.append(same_kids)
        
        # Interest similarity
        interests1 = set(user1['interests'].split(',')) if isinstance(user1['interests'], str) else set(user1.get('interests', []))
        interests2 = set(user2['interests'].split(',')) if isinstance(user2['interests'], str) else set(user2.get('interests', []))
        if interests1 and interests2:
            intersection = len(interests1 & interests2)
            union = len(interests1 | interests2)
            interest_sim = intersection / union if union > 0 else 0
        else:
            interest_sim = 0
        features.append(interest_sim)
        
        return np.array(features).reshape(1, -1)
    
    def predict_compatibility(self, user1, user2):
        """Predict compatibility score (0-100)"""
        features = self.prepare_single_pair(user1, user2)
        features_scaled = self.scaler.transform(features)
        prob = self.model.predict_proba(features_scaled)[0, 1]
        return round(prob * 100, 1)
    
    def get_top_matches(self, current_user, candidate_users, top_n=10):
        """Get top N compatible users"""
        scores = []
        for user in candidate_users:
            if user.get('id') == current_user.get('id'):
                continue
            score = self.predict_compatibility(current_user, user)
            scores.append({'user': user, 'score': score})
        
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_n]

# Test the predictor
if __name__ == '__main__':
    import pandas as pd
    
    # Load data
    df = pd.read_csv('users_data.csv')
    users = df.to_dict('records')
    
    # Initialize predictor
    predictor = CompatibilityPredictor()
    
    # Test with first two users
    if len(users) >= 2:
        score = predictor.predict_compatibility(users[0], users[1])
        print(f"Compatibility between {users[0]['full_name']} and {users[1]['full_name']}: {score}%")
        
        # Get top matches for first user
        top_matches = predictor.get_top_matches(users[0], users[1:], top_n=5)
        print(f"\nTop matches for {users[0]['full_name']}:")
        for match in top_matches:
            print(f"  {match['user']['full_name']}: {match['score']}%")