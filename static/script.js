document.addEventListener('DOMContentLoaded', () => {
    fetchTransactions();
    
    const form = document.getElementById('addTransactionForm');
    if (form) {
        form.addEventListener('submit', handleAddTransaction);
    }
});

async function handleAddTransaction(e) {
    e.preventDefault();
    
    const data = {
        amount: parseFloat(document.getElementById('transactionAmount').value),
        type: document.getElementById('transactionType').value,
        description: document.getElementById('transactionDescription').value,
        date: document.getElementById('transactionDate').value
    };

    try {
        const response = await fetch('/add_transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            alert('Błąd dodawania transakcji: ' + (result.error || 'Nieznany błąd'));
            return;
        }

        // Sukces - resetuj formularz
        document.getElementById('addTransactionForm').reset();

        // Zamknij okno modalne
        const modalEl = document.getElementById('addTransactionModal');
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.hide();

        // Odśwież dane
        fetchTransactions();

    } catch (error) {
        console.error('Błąd podczas zapisywania transakcji:', error);
        alert('Wystąpił błąd podczas komunikacji z serwerem.');
    }
}

async function fetchTransactions() {
    try {
        const response = await fetch('/api/transactions');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        
        // Update balance
        const balanceEl = document.getElementById('balanceAmount');
        if (balanceEl && data.balance !== undefined) {
            balanceEl.innerHTML = `${data.balance.toFixed(2)} <span class="fs-2 fw-normal opacity-75">PLN</span>`;
        }
        
        // Update table
        const tbody = document.getElementById('transactionsTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (!data.transactions || data.transactions.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-muted py-4">Brak ostatnich transakcji w historii.</td>
                </tr>
            `;
            return;
        }
        
        data.transactions.forEach(t => {
            const tr = document.createElement('tr');
            
            let typeBadge = '';
            let amountClass = '';
            let prefix = '';
            
            if (t.type === 'wydatek') {
                typeBadge = '<span class="badge bg-secondary opacity-75">wydatek</span>';
                amountClass = 'text-danger';
                prefix = '-';
            } else {
                typeBadge = '<span class="badge bg-info bg-opacity-75 text-dark">przychód</span>';
                amountClass = 'text-success';
                prefix = '+';
            }
            
            // Opcjonalne formatowanie daty
            const dateStr = t.date;
            const amountStr = t.amount.toFixed(2);
            
            tr.innerHTML = `
                <td>${dateStr}</td>
                <td class="fw-medium">${t.description}</td>
                <td>${typeBadge}</td>
                <td class="text-end ${amountClass} fw-bold">${prefix}${amountStr} PLN</td>
            `;
            
            tbody.appendChild(tr);
        });
        
    } catch (error) {
        console.error('Błąd podczas pobierania transakcji:', error);
        
        const tbody = document.getElementById('transactionsTableBody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-danger py-4">Błąd ładowania danych z serwera.</td>
                </tr>
            `;
        }
    }
}
