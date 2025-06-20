document.addEventListener('DOMContentLoaded', function () {
    const rows = Array.from(document.querySelectorAll('tbody tr')).map(tr => {
        return Array.from(tr.querySelectorAll('td')).slice(0, 5).map(td => td.textContent.trim());
    });
    localStorage.setItem('simple_table_data', JSON.stringify(rows));
    console.log("Saved table to localStorage:", rows);
});

document.addEventListener('DOMContentLoaded', () => {
    const clearBtn = document.getElementById('clear-row-button');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const inputs = document.querySelectorAll('#empty-input-form input[type="text"]');
            inputs.forEach(input => input.value = '');
        });
    }

    const removeBtn = document.getElementById('remove-row-button');
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            const row = removeBtn.closest('tr');
            row.style.display = 'none';
        });
    }
});