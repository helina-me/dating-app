def calculate_compatibility(user_a, user_b):
    scores = []
    weights = []
    
    # Age compatibility (weight: 0.15)
    if user_a.min_age_pref <= user_b.age <= user_a.max_age_pref:
        age_score = 100
    else:
        age_diff = abs(user_a.age - user_b.age)
        age_score = max(0, 100 - age_diff * 5)
    scores.append(age_score)
    weights.append(0.15)
    
    # Height compatibility (weight: 0.10)
    if user_a.min_height_pref <= user_b.height_cm <= user_a.max_height_pref:
        height_score = 100
    else:
        height_diff = abs(user_a.height_cm - user_b.height_cm)
        height_score = max(0, 100 - height_diff * 2)
    scores.append(height_score)
    weights.append(0.10)
    
    # Interest similarity (weight: 0.25)
    interests_a = set(user_a.get_interests_list())
    interests_b = set(user_b.get_interests_list())
    if interests_a and interests_b:
        intersection = len(interests_a & interests_b)
        union = len(interests_a | interests_b)
        interest_score = (intersection / union) * 100 if union > 0 else 0
    else:
        interest_score = 0
    scores.append(interest_score)
    weights.append(0.25)
    
    # Lifestyle match (weight: 0.20)
    lifestyle_score = 0
    if user_a.smoking == user_b.smoking:
        lifestyle_score += 25
    if user_a.drinking == user_b.drinking:
        lifestyle_score += 25
    if user_a.exercise == user_b.exercise:
        lifestyle_score += 25
    if user_a.wants_kids == user_b.wants_kids:
        lifestyle_score += 25
    scores.append(lifestyle_score)
    weights.append(0.20)
    
    # Values alignment (weight: 0.15)
    values_score = 0
    if user_a.religion == user_b.religion:
        values_score += 50
    if user_a.politics == user_b.politics:
        values_score += 50
    scores.append(values_score)
    weights.append(0.15)
    
    # Goal alignment (weight: 0.15)
    if user_a.relationship_goal == user_b.relationship_goal:
        goal_score = 100
    else:
        goal_score = 50
    scores.append(goal_score)
    weights.append(0.15)
    
    total = sum(s * w for s, w in zip(scores, weights))
    return round(total, 1)

def get_shared_interests(user_a, user_b):
    return list(set(user_a.get_interests_list()) & set(user_b.get_interests_list()))