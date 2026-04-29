from ml.predict import CompatibilityPredictor
from ml.features import get_shared_interests
from models import User

class DatingRecommender:
    def __init__(self, db):
        self.db = db
        try:
            self.predictor = CompatibilityPredictor()
            print("ML model loaded successfully")
        except:
            print("ML model not found. Run ml/model_training.py first")
            self.predictor = None
    
    def get_matches(self, current_user, limit=20):
        # Gender-based filtering
        if current_user.gender == 'Male':
            opposite_gender = 'Female'
        elif current_user.gender == 'Female':
            opposite_gender = 'Male'
        else:
            opposite_gender = None  # Non-binary see all genders
        
        query = User.query.filter(
            User.id != current_user.id,
            User.is_active == True
        )
        if opposite_gender:
            query = query.filter(User.gender == opposite_gender)
        
        other_users = query.all()
        
        if self.predictor:
            current_dict = current_user.to_dict()
            candidates = [u.to_dict() for u in other_users]
            results = self.predictor.get_top_matches(current_dict, candidates, top_n=limit)
            
            matches = []
            for r in results:
                user = self.db.query(User).filter(User.id == r['user']['id']).first()
                shared = get_shared_interests(current_user, user)
                matches.append({
                    'user_id': user.id,
                    'full_name': user.full_name,
                    'age': user.age,
                    'height_cm': user.height_cm,
                    'gender': user.gender,
                    'education': user.education,
                    'occupation': user.occupation,
                    'compatibility_score': r['score'],
                    'shared_interests': shared,
                    'bio': user.bio[:200] if user.bio else ""
                })
            return matches
        else:
            from ml.features import calculate_compatibility
            results = []
            for user in other_users:
                score = calculate_compatibility(current_user, user)
                shared = get_shared_interests(current_user, user)
                results.append({
                    'user_id': user.id,
                    'full_name': user.full_name,
                    'age': user.age,
                    'height_cm': user.height_cm,
                    'gender': user.gender,
                    'education': user.education,
                    'occupation': user.occupation,
                    'compatibility_score': score,
                    'shared_interests': shared,
                    'bio': user.bio[:200] if user.bio else ""
                })
            results.sort(key=lambda x: x['compatibility_score'], reverse=True)
            return results[:limit]
    
    def get_match_percentage(self, user1, user2):
        if self.predictor:
            return self.predictor.predict_compatibility(user1.to_dict(), user2.to_dict())
        else:
            from ml.features import calculate_compatibility
            return calculate_compatibility(user1, user2)