from app import create_app
from models import db, Transaction

app = create_app()
with app.app_context():
    # Test POST /add_transaction
    client = app.test_client()
    data = {
        'amount': 150.50,
        'description': 'Testowa transakcja',
        'date': '2023-11-01',
        'type': 'wydatek',
        'user_id': 1
    }
    response = client.post('/add_transaction', json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Check database
    txn = Transaction.query.filter_by(description='Testowa transakcja').first()
    if txn:
        print(f"Transakcja zapisana w bazie: {txn.amount} ({txn.date})")
    else:
        print("Błąd: Transakcji nie ma w bazie danych.")
