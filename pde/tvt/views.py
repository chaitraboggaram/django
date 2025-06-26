from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm
from bokeh.embed import server_document
from django.shortcuts import render

def home(request):
    show_input_row = False

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.method == "POST":
        if "add" in request.POST:
            form = DocumentForm(request.POST)
            if form.is_valid() and any(request.POST.get(field) for field in form.fields):
                doc = form.save(commit=False)
                doc.session_key = session_key
                doc.save()
                show_input_row = False
                return redirect("home")
            else:
                show_input_row = True

        elif "delete" in request.POST:
            doc_id = request.POST.get("delete")
            Document.objects.filter(id=doc_id, session_key=session_key).delete()
            return redirect("home")

        elif "cancel" in request.POST:
            show_input_row = False
            return redirect("home")

    else:
        form = DocumentForm()

    documents = Document.objects.filter(session_key=session_key)

    headers = [
        ("Agile PN", 150),
        ("Agile Rev", 150),
        ("Document Title", 350),
        ("Document Type", 200),
        ("Polarion ID", 150),
        ("", 200),
    ]

    table_placeholder = [
        ("Agile PN", 150, "agile_pn", "center"),
        ("Agile Rev", 150, "agile_rev", "center"),
        ("Document Title", 350, "title", "left"),
        ("Document Type", 200, "doc_type", "left"),
        ("Polarion ID", 150, "polarion_id", "center"),
    ]

    context = {
        "form": form,
        "documents": documents,
        "headers": headers,
        "table_placeholder": table_placeholder,
        "show_input_row": show_input_row,
    }

    return render(request, "home.html", context)

def traces(request):
    show_input_row = False

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.method == "POST":
        if "add" in request.POST:
            form = DocumentForm(request.POST)
            if form.is_valid() and any(request.POST.get(field) for field in form.fields):
                doc = form.save(commit=False)
                doc.session_key = session_key
                doc.save()
                show_input_row = False
                return redirect("traces")
            else:
                show_input_row = True

        elif "delete" in request.POST:
            doc_id = request.POST.get("delete")
            Document.objects.filter(id=doc_id, session_key=session_key).delete()
            return redirect("traces")

        elif "cancel" in request.POST:
            show_input_row = False
            return redirect("traces")

    else:
        form = DocumentForm()

    documents = Document.objects.filter(session_key=session_key)

    headers = [
        ("Agile PN", 150),
        ("Agile Rev", 150),
        ("Document Title", 350),
        ("Document Type", 200),
        ("Polarion ID", 150),
        ("", 200),
    ]

    table_placeholder = [
        ("Agile PN", 150, "agile_pn", "center"),
        ("Agile Rev", 150, "agile_rev", "center"),
        ("Document Title", 350, "title", "left"),
        ("Document Type", 200, "doc_type", "left"),
        ("Polarion ID", 150, "polarion_id", "center"),
    ]

    documents_data = list(documents.values())
    script = server_document(f"/traces/", arguments={"documents": documents_data})
    context = {
        "form": form,
        "documents": documents,
        "headers": headers,
        "table_placeholder": table_placeholder,
        "show_input_row": show_input_row,
        "script": script
    }

    return render(request, "traces.html", context)
