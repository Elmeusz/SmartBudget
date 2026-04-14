import unittest
from app import create_app
from models import db, Transaction, User
from logic import calculate_balance, validate_transaction
from datetime import datetime

class TestLogic(unittest.TestCase):
    def setUp(self):
        """Ustawienie środowiska testowego przed każdym testem."""
        self.app = create_app({
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'TESTING': True
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Inicjalizacja bazy
        db.create_all()
        
        # Upewniamy się, że użytkownik testowy istnieje (ID=1)
        if User.query.filter_by(id=1).first() is None:
            user = User(id=1, username='test', email='test@test.com', password_hash='hash')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """Czyszczenie po każdym teście."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_calculate_balance_multiple_transactions(self):
        """Testuje, czy saldo jest poprawne dla 2 przychodów i 1 wydatku."""
        # 2 przychody (1000 + 500 = 1500)
        db.session.add(Transaction(
            amount=1000.0, 
            type='przychód', 
            date=datetime.now().date(), 
            description='Przychód 1', 
            user_id=1
        ))
        db.session.add(Transaction(
            amount=500.0, 
            type='przychód', 
            date=datetime.now().date(), 
            description='Przychód 2', 
            user_id=1
        ))
        
        # 1 wydatek (300)
        db.session.add(Transaction(
            amount=300.0, 
            type='wydatek', 
            date=datetime.now().date(), 
            description='Wydatek 1', 
            user_id=1
        ))
        
        db.session.commit()
        
        # Oczekiwany wynik: 1500 - 300 = 1200
        balance = calculate_balance()
        self.assertEqual(balance, 1200.0)

    def test_validate_negative_amount(self):
        """Testuje, czy próba dodania transakcji z ujemną kwotą zwraca błąd."""
        data = {
            'amount': -50.0,
            'description': 'Test',
            'date': '2023-10-10'
        }
        is_valid, message = validate_transaction(data)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Kwota musi być większa od 0.")

    def test_validate_empty_description(self):
        """Testuje, czy próba dodania transakcji bez opisu zwraca błąd."""
        data = {
            'amount': 50.0,
            'description': '', # empty description
            'date': '2023-10-10'
        }
        is_valid, message = validate_transaction(data)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Opis nie może być pusty.")

if __name__ == '__main__':
    unittest.main()
