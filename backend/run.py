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
    # Auto-initialize database if needed
    with app.app_context():
        try:
            from app import db
            from sqlalchemy import inspect
            from init_db import init_database
            
            inspector = inspect(db.engine)
            if not inspector.get_table_names():
                print("Database tables not found. Initializing...")
                init_database()
                print("Database initialized successfully.")
        except Exception as e:
            print(f"Database check/initialization failed: {e}")

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
