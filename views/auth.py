from flask import Blueprint, request, jsonify
from models import User, db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth_bp", __name__)

# register

# user registration
@auth_bp.route("/register", methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing fields"}), 400

    # Check if user already exists
    current_user = User.query.filter_by(email=email).first()
    if current_user:
        return jsonify({"message": "User with this email already exists"}), 400

    hashed_password = check_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# login

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    # Log the provided email and password for debugging
    print(f"Login attempt with email: {email}, password: {password}")

    # Look for user by email
    user = User.query.filter_by(email=email).first()

    if user:
        print(f"User found: {user.username}, stored password hash: {user.password}")
    else:
        print("No user found with this email")

    if not user:
        return jsonify({"error": "Email not found"}), 401  

    # Log the password check
    if not check_password_hash(user.password, password):
        print("Password mismatch!")
        return jsonify({"error": "Incorrect password"}), 401 
    
    # If user is found and password matches, generate JWT token
    access_token = create_access_token(identity=user.id)

    # Log the access token for debugging purposes
    print(f"Generated Access Token: {access_token}")  

    # Return success message with token and user data
    return jsonify({
        "message": "Login successful",
        "user": {
            "email": user.email,
            "username": user.username
        },
        "access_token": access_token  # Include the JWT token in the response
    }), 200


# current user

@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    try:
        current_user_id = get_jwt_identity()  # Get the user ID from JWT
        print(f"Decoded User ID from JWT: {current_user_id}")  # Log the user ID for debugging
        
        user = User.query.get(current_user_id)

        if user:
            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        # Log the exception to help debug
        print(f"Error during token decoding or user lookup: {str(e)}")
        return jsonify({"message": str(e)}), 500
    

    # logout
    
# Logout (not implementing token blacklisting here)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Successfully logged out"}), 200

# Update User Profile
@auth_bp.route("/user/update", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()  # Get the user ID from JWT token
    data = request.get_json()

    # Fetch the current user from the database
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get the new profile data or keep the old values
    username = data.get('username', user.username)
    email = data.get('email', user.email)

    # Check if username or email already exists (excluding current user's data)
    if username != user.username:
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({"message": "Username already exists"}), 400

    if email != user.email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({"message": "Email already exists"}), 400

    # Update user fields
    user.username = username
    user.email = email

    db.session.commit()

    return jsonify({
        "message": "User profile updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200


# Update User Password
@auth_bp.route("/user/updatepassword", methods=["PUT"])
@jwt_required()
def update_password():
    current_user_id = get_jwt_identity()  
    data = request.get_json()

    # Fetch the current user from the database
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get the old password and new password from the request
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({"message": "Old and new passwords are required"}), 400

    # Check if the old password matches
    if not check_password_hash(user.password, old_password):
        return jsonify({"message": "Incorrect old password"}), 400

    # Hash the new password
    user.password = check_password_hash(new_password)
    
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200


# Delete User Account (Self-deletion Only)
@auth_bp.route("/user/delete_account", methods=["DELETE"])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()  

    # Fetch the current user from the database
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User account deleted successfully"}), 200


