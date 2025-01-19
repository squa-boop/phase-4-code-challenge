# event.py
from flask import Blueprint, request, jsonify
from models import db, Event  # Import Event model
from werkzeug.security import generate_password_hash

event_bp = Blueprint("event_bp", __name__)

# CREATE Event
@event_bp.route("/event", methods=['POST'])
def create_event():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    event_date = data.get('event_date')
    user_id = data.get('user_id')

    # Validate required fields
    if not title or not description or not event_date or not user_id:
        return jsonify({"message": "Missing fields"}), 400

    new_event = Event(
        title=title,
        description=description,
        event_date=event_date,
        user_id=user_id
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify({"message": "Event created", "event": {
        "id": new_event.id,
        "title": new_event.title,
        "description": new_event.description,
        "event_date": new_event.event_date,
        "user_id": new_event.user_id
    }}), 201

# READ Event by ID
@event_bp.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    return jsonify({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_date": event.event_date,
        "user_id": event.user_id
    }), 200

# READ all Events for a specific User
@event_bp.route('/user/<int:user_id>/events', methods=['GET'])
def get_user_events(user_id):
    events = Event.query.filter_by(user_id=user_id).all()

    if not events:
        return jsonify({"message": "No events found for this user"}), 404

    return jsonify([{
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_date": event.event_date
    } for event in events]), 200

# UPDATE Event by ID
@event_bp.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    title = data.get('title')
    description = data.get('description')
    event_date = data.get('event_date')

    if title:
        event.title = title
    if description:
        event.description = description
    if event_date:
        event.event_date = event_date

    db.session.commit()

    return jsonify({"message": "Event updated", "event": {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_date": event.event_date,
        "user_id": event.user_id
    }}), 200

# DELETE Event by ID
@event_bp.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event deleted"}), 200
