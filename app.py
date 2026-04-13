import os
from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    
    # Configuration
    # Ensure the instance folder exists for the database
    app.config['SECRET_KEY'] = 'dev_key_for_smart_budget'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'smartbudget.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
        db.create_all()

    @app.route('/')
    def index():
        return 'Aplikacja działa'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
