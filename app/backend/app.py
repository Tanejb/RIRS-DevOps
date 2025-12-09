from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
# Look for .env in backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire for simplicity
    
    # Initialize extensions
    CORS(app)  # Enable CORS for frontend communication
    JWTManager(app)
    
    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.todos import todos_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos_bp, url_prefix='/api/todos')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
