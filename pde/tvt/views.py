from django.shortcuts import render
from .models import Document
from .forms import DocumentForm
from bokeh.embed import server_document


def get_session_key(request):
	if not request.session.session_key:
		request.session.create()
	return request.session.session_key


def process_form(request):
	session_key = get_session_key(request)
	show_input_row = False
	edit_id = None
	form = None

	if request.method == "POST":
		if "add" in request.POST:
			form = DocumentForm(request.POST)
			if form.is_valid() and any(
				request.POST.get(field) for field in form.fields
			):
				doc = form.save(commit=False)
				doc.session_key = session_key
				doc.save()
			else:
				show_input_row = True

		elif "edit" in request.POST:
			edit_id = request.POST.get("edit")
			doc_to_edit = Document.objects.get(id=edit_id, session_key=session_key)
			form = DocumentForm(instance=doc_to_edit)

		elif "save" in request.POST:
			edit_id = request.POST.get("edit_id")
			doc_to_edit = Document.objects.get(id=edit_id, session_key=session_key)
			form = DocumentForm(request.POST, instance=doc_to_edit)
			if form.is_valid():
				form.save()

		elif "clear" in request.POST:
			show_input_row = True
			form = DocumentForm()

		elif "delete" in request.POST:
			doc_id = request.POST.get("delete")
			Document.objects.filter(id=doc_id, session_key=session_key).delete()

	else:
		form = DocumentForm()

	return None, show_input_row, form, edit_id


def get_documents_and_headers(session_key):
	documents = Document.objects.filter(session_key=session_key)

	headers = [
		("Agile PN", 150),
		("Agile Rev", 150),
		("Document Title", 350),
		("Document Type", 200),
		("Document ID", 150),
		("", 200),
	]

	table_placeholder = [
		("Agile PN", 150, "agile_pn", "center"),
		("Agile Rev", 150, "agile_rev", "center"),
		("Document Title", 350, "title", "left"),
		("Document Type", 200, "doc_type", "left"),
		("Document ID", 150, "doc_id", "center"),
	]

	doc_type_options = [
		"Requirement",
		"Design",
		"Test",
		"Specification",
		"Task",
		"Development",
		"Risk",
	]

	return documents, headers, table_placeholder, doc_type_options


def home(request):
	session_key = get_session_key(request)

	response, show_input_row, form, edit_id = process_form(request)
	if response:
		return response

	documents, headers, table_placeholder, doc_type_options = get_documents_and_headers(
		session_key
	)

	context = {
		"form": form,
		"documents": documents,
		"headers": headers,
		"table_placeholder": table_placeholder,
		"show_input_row": show_input_row,
		"edit_id": edit_id,
		"edit_data": None,
		"doc_type_options": doc_type_options,
	}

	if edit_id:
		try:
			edit_data = documents.get(id=edit_id)
			context["edit_data"] = edit_data
		except Document.DoesNotExist:
			context["edit_data"] = None

	return render(request, "home.html", context)


def traces(request):
	session_key = get_session_key(request)

	response, show_input_row, form, edit_id = process_form(request)
	if response:
		return response

	documents, headers, table_placeholder, doc_type_options = get_documents_and_headers(
		session_key
	)

	documents_data = list(documents.values())

	generate_flag = request.POST.get('generateTracesFlag', 'false').lower()
	print("Flag in views", generate_flag)

	script = server_document(f"/traces/", arguments={"documents": documents_data, "generate_flag": generate_flag})

	context = {
		"form": form,
		"documents": documents,
		"headers": headers,
		"table_placeholder": table_placeholder,
		"show_input_row": show_input_row,
		"script": script,
		"edit_id": edit_id,
		"edit_data": None,
		"doc_type_options": doc_type_options,
	}

	if edit_id:
		try:
			edit_data = documents.get(id=edit_id)
			context["edit_data"] = edit_data
		except Document.DoesNotExist:
			context["edit_data"] = None

	return render(request, "traces.html", context)
