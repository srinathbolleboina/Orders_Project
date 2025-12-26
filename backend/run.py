"""
Application entry point
"""
import os
from app import create_app

# Get environment
env = os.getenv('FLASK_ENV', 'development')

# Create application
app = create_app(env)

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
