from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is on sys.path so `backend.*` imports work when running directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
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
    # In Docker, files are in /app, not /app/backend
    try:
        from backend.routes.auth import auth_bp
        from backend.routes.todos import todos_bp
    except ImportError:
        # Fallback for Docker environment where files are directly in /app
        import sys
        sys.path.insert(0, '/app')
        from routes.auth import auth_bp
        from routes.todos import todos_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos_bp, url_prefix='/api/todos')
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
