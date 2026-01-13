from flask import Flask, jsonify
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

# Load environment variables
# Look for .env in backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret:
        raise ValueError('JWT_SECRET_KEY environment variable must be set')
    app.config['JWT_SECRET_KEY'] = jwt_secret
    # Set token expiration to 24 hours for security
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours in seconds
    
    # Initialize extensions
    # CORS configuration - restrict to specific origins in production
    allowed_origins_env = os.getenv('ALLOWED_ORIGINS', '')
    if allowed_origins_env:
        allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()]
    else:
        # Default to localhost for development only
        allowed_origins = ['http://localhost:3000', 'http://localhost:80']
    
    CORS(app, 
         resources={r"/api/*": {"origins": allowed_origins}},
         supports_credentials=True)
    JWTManager(app)
    
    # Register blueprints
    # In Docker, files are in /app, not /app/backend
    try:
        from backend.routes.auth import auth_bp
        from backend.routes.todos import todos_bp
    except ImportError:
        # Fallback for Docker environment where files are directly in /app
        from routes.auth import auth_bp
        from routes.todos import todos_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos_bp, url_prefix='/api/todos')
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'Backend is running'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
