from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

from models import db

# Import blueprints from the views folder
from views.user import user_bp  
from views.event import event_bp  
from views.auth import auth_bp  

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

# Initialize migrations and database
migrate = Migrate(app, db)
db.init_app(app)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "user" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
jwt = JWTManager(app)
jwt.init_app(app)

# Register blueprints
app.register_blueprint(user_bp) 
app.register_blueprint(event_bp)  
app.register_blueprint(auth_bp)  




if __name__ == '__main__':
    app.run(debug=True)









# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from sqlalchemy import MetaData






# # Initialize metadata and Flask app
# metadata = MetaData()
# app = Flask(__name__)

# # App configuration for SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # SQLite for simplicity
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database and migrate
# db = SQLAlchemy(app, metadata=metadata)
# migrate = Migrate(app, db)

# # ---------------------- User Model ----------------------

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), nullable=False, unique=True)
#     email = db.Column(db.String(128), nullable=False, unique=True)
#     password = db.Column(db.String(128), nullable=False)

#     # Relationship with Event Model
#     events = db.relationship('Event', backref='user', lazy=True)

# # ---------------------- Event Model ----------------------

# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(128), nullable=False)
#     description = db.Column(db.String(256), nullable=False)
#     event_date = db.Column(db.String(20), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# # ---------------------- CRUD for User ----------------------

# # CREATE User
# @app.route('/user', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     # Validate required fields
#     if not username or not email or not password:
#         return jsonify({"message": "Missing fields"}), 400

#     new_user = User(username=username, email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({"message": "User created", "user": {
#         "id": new_user.id,
#         "username": new_user.username,
#         "email": new_user.email
#     }}), 201

# # READ User by ID
# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"message": "User not found"}), 404
#     return jsonify({
#         "id": user.id,
#         "username": user.username,
#         "email": user.email
#     }), 200

# # UPDATE User by ID
# @app.route('/user/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.get_json()
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     if username:
#         user.username = username
#     if email:
#         user.email = email
#     if password:
#         user.password = password

#     db.session.commit()

#     return jsonify({"message": "User updated", "user": {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email
#     }}), 200

# # DELETE User by ID
# @app.route('/user/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({"message": "User deleted"}), 200

# # ---------------------- CRUD for Event ----------------------

# # CREATE Event
# @app.route('/event', methods=['POST'])
# def create_event():
#     data = request.get_json()
#     title = data.get('title')
#     description = data.get('description')
#     event_date = data.get('event_date')
#     user_id = data.get('user_id')

#     # Validate required fields
#     if not title or not description or not event_date or not user_id:
#         return jsonify({"message": "Missing fields"}), 400

#     new_event = Event(
#         title=title,
#         description=description,
#         event_date=event_date,
#         user_id=user_id
#     )

#     db.session.add(new_event)
#     db.session.commit()

#     return jsonify({"message": "Event created", "event": {
#         "id": new_event.id,
#         "title": new_event.title,
#         "description": new_event.description,
#         "event_date": new_event.event_date,
#         "user_id": new_event.user_id
#     }}), 201

# # READ Event by ID
# @app.route('/event/<int:event_id>', methods=['GET'])
# def get_event(event_id):
#     event = Event.query.get(event_id)

#     if not event:
#         return jsonify({"message": "Event not found"}), 404

#     return jsonify({
#         "id": event.id,
#         "title": event.title,
#         "description": event.description,
#         "event_date": event.event_date,
#         "user_id": event.user_id
#     }), 200

# # READ all Events for a specific User
# @app.route('/user/<int:user_id>/events', methods=['GET'])
# def get_user_events(user_id):
#     events = Event.query.filter_by(user_id=user_id).all()

#     if not events:
#         return jsonify({"message": "No events found for this user"}), 404

#     return jsonify([{
#         "id": event.id,
#         "title": event.title,
#         "description": event.description,
#         "event_date": event.event_date
#     } for event in events]), 200

# # UPDATE Event by ID
# @app.route('/event/<int:event_id>', methods=['PUT'])
# def update_event(event_id):
#     data = request.get_json()
#     event = Event.query.get(event_id)

#     if not event:
#         return jsonify({"message": "Event not found"}), 404

#     title = data.get('title')
#     description = data.get('description')
#     event_date = data.get('event_date')

#     if title:
#         event.title = title
#     if description:
#         event.description = description
#     if event_date:
#         event.event_date = event_date

#     db.session.commit()

#     return jsonify({"message": "Event updated", "event": {
#         "id": event.id,
#         "title": event.title,
#         "description": event.description,
#         "event_date": event.event_date,
#         "user_id": event.user_id
#     }}), 200

# # DELETE Event by ID
# @app.route('/event/<int:event_id>', methods=['DELETE'])
# def delete_event(event_id):
#     event = Event.query.get(event_id)

#     if not event:
#         return jsonify({"message": "Event not found"}), 404

#     db.session.delete(event)
#     db.session.commit()

#     return jsonify({"message": "Event deleted"}), 200

# # ---------------------- Run the Flask app ----------------------
# if __name__ == '__main__':
#     app.run(debug=True)
