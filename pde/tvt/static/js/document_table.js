document.addEventListener('DOMContentLoaded', function () {
	const rows = Array.from(document.querySelectorAll('tbody tr')).map(tr => {
		return Array.from(tr.querySelectorAll('td')).slice(0, 5).map(td => td.textContent.trim());
	});
	localStorage.setItem('simple_table_data', JSON.stringify(rows));
	console.log("Saved table to localStorage:", rows);
});

function removeRequired(button) {
	const row = button.closest('tr');
	row.querySelectorAll('input, select').forEach(el => el.removeAttribute('required'));
}

function clearRow(button) {
	const row = button.closest('tr');
	row.querySelectorAll('input, select').forEach(el => el.value = '');
}