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

    form = DocumentForm()
    documents = Document.objects.filter(session_key=session_key)
    return render(request, 'document_table.html', {'form': form, 'documents': documents})
