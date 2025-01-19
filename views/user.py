from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users")
def fetch_users():
    users = User.query.all()

    # Initialize user_list before using it
    user_list = []  

    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'is_approved': user.is_approved,
            'is_admin': user.is_admin,
            'username': user.username,
            'events': [  
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "event_date": event.deadline 
                } for event in user.events  
            ]
        })

    return jsonify(user_list)  
# CREATE User
@user_bp.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not username or not email or not password:
        return jsonify({"message": "Missing fields"}), 400

    # Check if the username or email already exists
    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()
    
    if check_username:
        return jsonify({"message": "Username already exists"}), 400
    if check_email:
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

# READ User by ID
@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

# UPDATE User by ID
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Retrieve new values or keep old ones
    username = data.get('username', user.username)
    email = data.get('email', user.email)
    password = data.get('password', None)

    # Check if the new username or email already exists
    if username != user.username:  
        check_username = User.query.filter(User.username == username, User.id != user.id).first()
        if check_username:
            return jsonify({"message": "Username already exists"}), 400

    if email != user.email:  
        check_email = User.query.filter(User.email == email, User.id != user.id).first()
        if check_email:
            return jsonify({"message": "Email already exists"}), 400

    # Update fields if provided
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = generate_password_hash(password)

    db.session.commit()

    return jsonify({
        "message": "User updated",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200

# DELETE User by ID
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200
