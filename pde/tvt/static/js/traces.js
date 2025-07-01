const generateBtn = document.getElementById('generateBtn');
const flagInput = document.getElementById('generateTracesFlag');

generateBtn.addEventListener('click', function (event) {
	localStorage.setItem('generateTracesFlag', 'true');
	flagInput.value = 'true';
});
