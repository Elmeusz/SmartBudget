from datetime import datetime
from app import create_app
from models import db, Transaction
from logic import calculate_balance

app = create_app()
with app.app_context():
    # Clear existing transactions for clean test
    Transaction.query.delete()
    db.session.commit()
    
    # Add an income
    income = Transaction(amount=1000, description='Pensja', date=datetime.strptime('2023-10-01', '%Y-%m-%d').date(), type='przychód', user_id=1)
    db.session.add(income)
    
    # Add an expense
    expense = Transaction(amount=400, description='Czynsz', date=datetime.strptime('2023-10-05', '%Y-%m-%d').date(), type='wydatek', user_id=1)
    db.session.add(expense)
    
    db.session.commit()
    
    # Calculate balance
    balance = calculate_balance()
    print(f"Obliczony balans: {balance}")
    
    if balance == 600.0:
        print("Test zakończony sukcesem!")
    else:
        print(f"Błąd! Oczekiwano 600.0, otrzymano {balance}")
