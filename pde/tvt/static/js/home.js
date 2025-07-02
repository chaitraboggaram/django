document.getElementById('csvData').addEventListener('click', function () {
	var fileInput = document.getElementById('file-upload');
	var file = fileInput.files[0];
	if (!file) {
		alert('Please select a file to read.');
		return;
	}
	var reader = new FileReader();
	reader.onload = function (e) {
		var csvText = e.target.result;
		var lines = csvText.split('\n');
		lines.shift();
		var csvWithoutHeader = lines.join('\n');
		localStorage.setItem('simple_table_data', JSON.stringify(csvWithoutHeader));
		console.log("Saved CSV text without header to localStorage");
		document.getElementById('csv-data-input').value = csvWithoutHeader;
		document.getElementById('upload-form').submit();
	};
	reader.readAsText(file);
});