from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Interaction, FriendRequest, Conversation, Message
import jwt
import datetime
from functools import wraps
from config import Config
from ml.recommender import DatingRecommender
from ml.features import get_shared_interests

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"])
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user = User.query.get(current_user_id)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# ==================== AUTH ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'error': 'Email already registered'}), 400

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    interests_str = ','.join(data.get('interests', []))

    new_user = User(
        email=data['email'],
        password=hashed,
        full_name=data['full_name'],
        age=data['age'],
        height_cm=data['height_cm'],
        weight_kg=data.get('weight_kg', 0),
        gender=data['gender'],
        education=data.get('education', ''),
        occupation=data.get('occupation', ''),
        income=data.get('income', ''),
        smoking=data.get('smoking', 'Never'),
        drinking=data.get('drinking', 'Never'),
        exercise=data.get('exercise', 'Never'),
        interests=interests_str,
        religion=data.get('religion', ''),
        politics=data.get('politics', 'Moderate'),
        wants_kids=data.get('wants_kids', 'Maybe'),
        min_age_pref=data.get('min_age_pref', 18),
        max_age_pref=data.get('max_age_pref', 100),
        min_height_pref=data.get('min_height_pref', 140),
        max_height_pref=data.get('max_height_pref', 210),
        relationship_goal=data.get('relationship_goal', 'Long-term'),
        bio=data.get('bio', ''),
        perfect_match_desc=data.get('perfect_match_desc', '')
    )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({
        'user_id': new_user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['JWT_SECRET'], algorithm='HS256')

    return jsonify({
        'message': 'User created',
        'token': token,
        'user': new_user.to_dict()
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['JWT_SECRET'], algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    })

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logged out'})

# ==================== USER ROUTES ====================

@app.route('/api/users/me', methods=['GET'])
@token_required
def get_me(current_user):
    return jsonify(current_user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@app.route('/api/users/me', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    for key, value in data.items():
        if hasattr(current_user, key) and key not in ['id', 'email', 'password', 'created_at']:
            if key == 'interests' and isinstance(value, list):
                value = ','.join(value)
            setattr(current_user, key, value)
    db.session.commit()
    return jsonify(current_user.to_dict())

# ==================== MATCH ROUTES ====================

@app.route('/api/matches/recommendations', methods=['GET'])
@token_required
def get_recommendations(current_user):
    limit = request.args.get('limit', 20, type=int)
    recommender = DatingRecommender(db)
    matches = recommender.get_matches(current_user, limit)
    return jsonify(matches)

@app.route('/api/matches/percentage/<int:user_id>', methods=['GET'])
@token_required
def get_match_percentage(current_user, user_id):
    target = User.query.get(user_id)
    if not target:
        return jsonify({'error': 'User not found'}), 404
    recommender = DatingRecommender(db)
    score = recommender.get_match_percentage(current_user, target)
    shared = get_shared_interests(current_user, target)
    return jsonify({
        'user_id': user_id,
        'compatibility_percentage': score,
        'shared_interests': shared
    })

@app.route('/api/matches/interact', methods=['POST'])
@token_required
def interact(current_user):
    data = request.json
    target_user_id = data.get('target_user_id')
    action = data.get('action')
    rating = data.get('rating')
    interaction = Interaction(
        user_id=current_user.id,
        target_user_id=target_user_id,
        action=action,
        rating=rating
    )
    db.session.add(interaction)
    db.session.commit()
    if action == 'like':
        mutual = Interaction.query.filter_by(
            user_id=target_user_id,
            target_user_id=current_user.id,
            action='like'
        ).first()
        if mutual:
            return jsonify({'mutual': True, 'message': 'It\'s a match!'})
    return jsonify({'mutual': False, 'message': 'Interaction recorded'})

# ==================== FRIEND REQUESTS ====================

@app.route('/api/friend-request/send', methods=['POST'])
@token_required
def send_friend_request(current_user):
    data = request.json
    to_user_id = data.get('to_user_id')
    to_user = User.query.get(to_user_id)
    if not to_user:
        return jsonify({'error': 'User not found'}), 404
    existing = FriendRequest.query.filter_by(
        from_user_id=current_user.id,
        to_user_id=to_user_id,
        status='pending'
    ).first()
    if existing:
        return jsonify({'error': 'Request already sent'}), 400
    req = FriendRequest(from_user_id=current_user.id, to_user_id=to_user_id, status='pending')
    db.session.add(req)
    db.session.commit()
    return jsonify({'message': 'Friend request sent'}), 201

@app.route('/api/friend-requests/received', methods=['GET'])
@token_required
def get_received_requests(current_user):
    requests = FriendRequest.query.filter_by(to_user_id=current_user.id, status='pending').all()
    result = []
    for req in requests:
        from_user = User.query.get(req.from_user_id)
        result.append({
            'id': req.id,
            'from_user_id': from_user.id,
            'from_user_name': from_user.full_name,
            'from_user_photo': from_user.photo_url,
            'created_at': req.created_at.isoformat()
        })
    return jsonify(result)

@app.route('/api/friend-request/respond', methods=['POST'])
@token_required
def respond_friend_request(current_user):
    data = request.json
    request_id = data.get('request_id')
    action = data.get('action')
    req = FriendRequest.query.get(request_id)
    if not req or req.to_user_id != current_user.id:
        return jsonify({'error': 'Invalid request'}), 404
    req.status = 'accepted' if action == 'accept' else 'rejected'
    db.session.commit()
    return jsonify({'message': f'Request {action}ed'}), 200
@app.route('/api/friends', methods=['GET'])
@token_required
def get_friends(current_user):
    # Find all accepted friend requests where current user is either sender or receiver
    sent = db.session.query(FriendRequest).filter(
        FriendRequest.from_user_id == current_user.id,
        FriendRequest.status == 'accepted'
    ).all()
    received = db.session.query(FriendRequest).filter(
        FriendRequest.to_user_id == current_user.id,
        FriendRequest.status == 'accepted'
    ).all()
    
    friend_ids = set()
    for fr in sent:
        friend_ids.add(fr.to_user_id)
    for fr in received:
        friend_ids.add(fr.from_user_id)
    
    friends = User.query.filter(User.id.in_(friend_ids)).all()
    return jsonify([{
        'id': f.id,
        'full_name': f.full_name,
        'age': f.age,
        'photo_url': f.photo_url
    } for f in friends])

# ==================== CHAT ====================

@app.route('/api/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    convs = Conversation.query.filter(
        (Conversation.user1_id == current_user.id) | (Conversation.user2_id == current_user.id)
    ).order_by(Conversation.updated_at.desc()).all()
    result = []
    for conv in convs:
        other_id = conv.user2_id if conv.user1_id == current_user.id else conv.user1_id
        other = User.query.get(other_id)
        last_msg = Message.query.filter_by(conversation_id=conv.id).order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(conversation_id=conv.id, is_read=False).filter(Message.sender_id != current_user.id).count()
        result.append({
            'conversation_id': conv.id,
            'other_user': {
                'id': other.id,
                'full_name': other.full_name,
                'photo_url': other.photo_url
            },
            'last_message': last_msg.content[:50] if last_msg else '',
            'last_message_time': last_msg.created_at.isoformat() if last_msg else None,
            'unread_count': unread
        })
    return jsonify(result)

@app.route('/api/messages/<int:conversation_id>', methods=['GET'])
@token_required
def get_messages(current_user, conversation_id):
    conv = Conversation.query.get(conversation_id)
    if not conv or (conv.user1_id != current_user.id and conv.user2_id != current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    Message.query.filter_by(conversation_id=conversation_id, is_read=False).filter(Message.sender_id != current_user.id).update({'is_read': True})
    db.session.commit()
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at.asc()).all()
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'content': m.content,
        'created_at': m.created_at.isoformat(),
        'is_read': m.is_read
    } for m in messages])

@app.route('/api/send-message', methods=['POST'])
@token_required
def send_message(current_user):
    data = request.json
    to_user_id = data.get('to_user_id')
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Message empty'}), 400
    conv = Conversation.query.filter(
        ((Conversation.user1_id == current_user.id) & (Conversation.user2_id == to_user_id)) |
        ((Conversation.user1_id == to_user_id) & (Conversation.user2_id == current_user.id))
    ).first()
    if not conv:
        conv = Conversation(user1_id=current_user.id, user2_id=to_user_id)
        db.session.add(conv)
        db.session.commit()
    msg = Message(conversation_id=conv.id, sender_id=current_user.id, content=content)
    db.session.add(msg)
    conv.updated_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'sent', 'conversation_id': conv.id}), 200

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Dating App API Running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)