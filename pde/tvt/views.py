from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm

def document_table_view(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.method == 'POST':
        if 'add' in request.POST:
            form = DocumentForm(request.POST)
            if form.is_valid():
                doc = form.save(commit=False)
                doc.session_key = session_key
                doc.save()
                return redirect('document_table')
        elif 'delete' in request.POST:
            doc_id = request.POST.get('delete')
            Document.objects.filter(id=doc_id, session_key=session_key).delete()
            return redirect('document_table')

    form = DocumentForm()
    documents = Document.objects.filter(session_key=session_key)

    headers = [
        ("Agile PN", 150),
        ("Agile Rev", 150),
        ("Document Title", 350),
        ("Document Type", 200),
        ("Polarion ID", 150),
        ("", 100),
    ]

    table_placeholder = [
        ("Agile PN", 150, "agile_pn"),
        ("Agile Rev", 150, "agile_rev"),
        ("Document Title", 350, "title"),
        ("Document Type", 200, "doc_type"),
        ("Polarion ID", 150, "polarion_id"),
    ]

    return render(request, 'document_table.html', {
        'form': form,
        'documents': documents,
        'headers': headers,
        'table_placeholder': table_placeholder,
    })