from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
try:
    from backend.models import db
except ImportError:
    from models import db

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/', methods=['GET'])
@jwt_required()
def get_todos():
    try:
        current_user = get_jwt_identity()
        user_todos = db.get_user_todos(current_user)
        
        # Convert ObjectId to string for JSON serialization
        for todo in user_todos:
            todo['_id'] = str(todo['_id'])
            todo['created_at'] = todo['created_at'].isoformat()
            todo['updated_at'] = todo['updated_at'].isoformat()
        
        return jsonify({'todos': user_todos}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@todos_bp.route('/', methods=['POST'])
@jwt_required()
def create_todo():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        # Input validation and sanitization
        title = data['title'].strip()
        description = data.get('description', '').strip()
        
        if not title or len(title) == 0:
            return jsonify({'error': 'Title cannot be empty'}), 400
        if len(title) > 200:
            return jsonify({'error': 'Title must be less than 200 characters'}), 400
        if len(description) > 1000:
            return jsonify({'error': 'Description must be less than 1000 characters'}), 400
        
        # Create new todo
        result = db.create_todo(
            current_user,
            title,
            description
        )
        
        # Get the created todo
        todo = db.todos.find_one({'_id': result.inserted_id})
        todo['_id'] = str(todo['_id'])
        todo['created_at'] = todo['created_at'].isoformat()
        todo['updated_at'] = todo['updated_at'].isoformat()
        
        return jsonify({'todo': todo}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@todos_bp.route('/<todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Convert string ID to ObjectId
        try:
            object_id = ObjectId(todo_id)
        except (ValueError, TypeError, InvalidId):
            return jsonify({'error': 'Invalid todo ID'}), 400
        
        # Prepare update data with validation
        update_data = {}
        if 'title' in data:
            title = data['title'].strip()
            if not title or len(title) == 0:
                return jsonify({'error': 'Title cannot be empty'}), 400
            if len(title) > 200:
                return jsonify({'error': 'Title must be less than 200 characters'}), 400
            update_data['title'] = title
        if 'description' in data:
            description = data['description'].strip()
            if len(description) > 1000:
                return jsonify({'error': 'Description must be less than 1000 characters'}), 400
            update_data['description'] = description
        if 'completed' in data:
            # Ensure completed is a boolean
            update_data['completed'] = bool(data['completed'])
        
        # Update todo
        result = db.update_todo(object_id, current_user, update_data)
        
        if result.matched_count == 0:
            return jsonify({'error': 'Todo not found'}), 404
        
        # Get updated todo
        todo = db.todos.find_one({'_id': object_id})
        todo['_id'] = str(todo['_id'])
        todo['created_at'] = todo['created_at'].isoformat()
        todo['updated_at'] = todo['updated_at'].isoformat()
        
        return jsonify({'todo': todo}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@todos_bp.route('/<todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    try:
        current_user = get_jwt_identity()
        
        # Convert string ID to ObjectId
        try:
            object_id = ObjectId(todo_id)
        except (ValueError, TypeError, InvalidId):
            return jsonify({'error': 'Invalid todo ID'}), 400
        
        # Delete todo
        result = db.delete_todo(object_id, current_user)
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Todo not found'}), 404
        
        return jsonify({'message': 'Todo deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@todos_bp.route('/<todo_id>/toggle', methods=['PATCH'])
@jwt_required()
def toggle_todo(todo_id):
    try:
        current_user = get_jwt_identity()
        
        # Convert string ID to ObjectId
        try:
            object_id = ObjectId(todo_id)
        except (ValueError, TypeError, InvalidId):
            return jsonify({'error': 'Invalid todo ID'}), 400
        
        # Toggle todo
        result = db.toggle_todo(object_id, current_user)
        
        if not result:
            return jsonify({'error': 'Todo not found'}), 404
        
        # Get updated todo
        todo = db.todos.find_one({'_id': object_id})
        todo['_id'] = str(todo['_id'])
        todo['created_at'] = todo['created_at'].isoformat()
        todo['updated_at'] = todo['updated_at'].isoformat()
        
        return jsonify({'todo': todo}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500