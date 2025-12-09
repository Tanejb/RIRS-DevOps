from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
# Look for .env in backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'todoapp')

client = MongoClient(MONGODB_URI)
db_instance = client[DATABASE_NAME]

# Collections
users_collection = db_instance.users
todos_collection = db_instance.todos

class Database:
    def __init__(self):
        self.users = users_collection
        self.todos = todos_collection
    
    def find_user(self, username):
        """Find a user by username"""
        return self.users.find_one({'username': username})
    
    def create_user(self, username, hashed_password):
        """Create a new user"""
        user = {
            'username': username,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }
        return self.users.insert_one(user)
    
    def get_user_todos(self, username):
        """Get all todos for a user"""
        return list(self.todos.find({'username': username}).sort('created_at', -1))
    
    def create_todo(self, username, title, description=''):
        """Create a new todo"""
        todo = {
            'username': username,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.todos.insert_one(todo)
    
    def update_todo(self, todo_id, username, update_data):
        """Update a todo"""
        update_data['updated_at'] = datetime.utcnow()
        return self.todos.update_one(
            {'_id': todo_id, 'username': username},
            {'$set': update_data}
        )
    
    def delete_todo(self, todo_id, username):
        """Delete a todo"""
        return self.todos.delete_one({'_id': todo_id, 'username': username})
    
    def toggle_todo(self, todo_id, username):
        """Toggle the completed status of a todo"""
        todo = self.todos.find_one({'_id': todo_id, 'username': username})
        if not todo:
            return None
        
        new_status = not todo.get('completed', False)
        result = self.todos.update_one(
            {'_id': todo_id, 'username': username},
            {'$set': {'completed': new_status, 'updated_at': datetime.utcnow()}}
        )
        return result if result.matched_count > 0 else None

# Create a singleton instance
db = Database()

