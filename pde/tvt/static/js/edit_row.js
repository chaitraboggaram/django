document.addEventListener("DOMContentLoaded", () => {
	const docTypeOptions = [
		"Requirement",
		"Design",
		"Test",
		"Specification",
		"Task",
		"Development",
		"Risk"
	];

	if (typeof docData === "undefined") {
		console.warn("docData not defined.");
		return;
	}

	Object.keys(docData).forEach(docId => {
		const data = docData[docId];

		const select = document.querySelector(`.doc-type-select[data-id="${docId}"]`);
		if (select) {
			select.innerHTML = `<option value="" disabled>-- Select --</option>`;
			docTypeOptions.forEach(type => {
				const opt = document.createElement("option");
				opt.value = type;
				opt.textContent = type;
				if (type === data.doc_type) opt.selected = true;
				select.appendChild(opt);
			});
			if (!data.doc_type) {
				select.selectedIndex = 0;
			}
		}

		["agile_pn", "agile_rev", "title", "doc_id"].forEach(field => {
			const input = document.querySelector(`input[data-id="${docId}"][data-field="${field}"]`);
			if (input) {
				input.value = data[field] || "";
			}
		});
	});
});
