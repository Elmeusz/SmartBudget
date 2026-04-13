from datetime import datetime
from sqlalchemy import func
from models import db, Transaction

def validate_transaction(data):
    """
    Waliduje dane transakcji.
    Oczekuje słownika 'data' z kluczami: 'amount', 'description', 'date'.
    
    Zwraca: (bool, message)
    """
    amount = data.get('amount')
    description = data.get('description')
    date_str = data.get('date')

    # Walidacja kwoty
    try:
        if amount is None:
            return False, "Kwota jest wymagana."
        
        amount_val = float(amount)
        if amount_val <= 0:
            return False, "Kwota musi być większa od 0."
    except (ValueError, TypeError):
        return False, "Nieprawidłowy format kwoty."

    # Walidacja opisu
    if not description or not str(description).strip():
        return False, "Opis nie może być pusty."

    # Walidacja daty (RRRR-MM-DD)
    if not date_str:
        return False, "Data jest wymagana."
        
    try:
        datetime.strptime(str(date_str), '%Y-%m-%d')
    except ValueError:
        return False, "Data musi być w formacie RRRR-MM-DD."

    return True, None

def calculate_balance():
    """
    Oblicza aktualny stan konta na podstawie wszystkich transakcji.
    Suma przychodów - Suma wydatków.
    """
    # Suma przychodów
    income = db.session.query(func.sum(Transaction.amount)).filter(Transaction.type == 'przychód').scalar() or 0
    # Suma wydatków
    expense = db.session.query(func.sum(Transaction.amount)).filter(Transaction.type == 'wydatek').scalar() or 0
    
    return float(income - expense)

def get_all_transactions():
    """
    Pobiera listę wszystkich transakcji posortowanych od najnowszej do najstarszej.
    """
    return Transaction.query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()
