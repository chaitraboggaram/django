from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ["agile_pn", "agile_rev", "title", "doc_type", "doc_id"]
		widgets = {
			"agile_pn": forms.TextInput(attrs={"placeholder": "Agile PN"}),
			"agile_rev": forms.TextInput(attrs={"placeholder": "Agile Rev"}),
			"title": forms.TextInput(attrs={"placeholder": "Document Title"}),
			"doc_type": forms.TextInput(attrs={"placeholder": "Document Type"}),
			"doc_id": forms.TextInput(attrs={"placeholder": "Document ID"}),
		}
