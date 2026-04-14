document.addEventListener('DOMContentLoaded', () => {
    fetchTransactions();
});

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
