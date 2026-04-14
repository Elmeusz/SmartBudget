import os
from flask import Flask, request, jsonify, render_template
from models import db, Transaction, User
from logic import validate_transaction
from datetime import datetime

def create_app(config_overrides=None):
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev_key_for_smart_budget'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'smartbudget.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_overrides:
        app.config.update(config_overrides)

    # Initialize database
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
        db.create_all()
        
        # Tworzenie testowego użytkownika jeśli baza jest pusta
        if User.query.count() == 0:
            test_user = User(username='testuser', email='test@example.com', password_hash='hash')
            db.session.add(test_user)
            db.session.commit()
            print("Utworzono domyślnego użytkownika testowego (id=1)")

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/transactions', methods=['GET'])
    def get_transactions():
        from logic import get_all_transactions, calculate_balance
        transactions = get_all_transactions()
        balance = calculate_balance()
        data = [{
            'id': t.id,
            'amount': t.amount,
            'description': t.description,
            'date': t.date.isoformat(),
            'type': t.type
        } for t in transactions]
        return jsonify({
            'balance': balance,
            'transactions': data
        })

    @app.route('/add_transaction', methods=['POST'])
    def add_transaction():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Brak danych JSON'}), 400

        # Walidacja danych
        is_valid, message = validate_transaction(data)
        if not is_valid:
            return jsonify({'error': message}), 400

        # Dodatkowe pola wymagane przez model (tymczasowe przypisanie usera jeśli nie podano)
        user_id = data.get('user_id', 1)
        trans_type = data.get('type', 'wydatek') # Domyślnie wydatek

        try:
            new_transaction = Transaction(
                amount=data['amount'],
                description=data['description'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                type=trans_type,
                user_id=user_id
            )
            db.session.add(new_transaction)
            db.session.commit()
            return jsonify({'message': 'Transakcja dodana pomyślnie', 'id': new_transaction.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Błąd zapisu: {str(e)}'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
