from django.contrib.auth.models import User
from django.db import models

class Document(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    agile_pn = models.CharField(max_length=100, blank=True)
    agile_rev = models.CharField(max_length=100, blank=True)
    title = models.CharField("Document Title", max_length=255, blank=True)
    doc_type = models.CharField("Document Type", max_length=100, blank=True)
    polarion_id = models.CharField(max_length=100, blank=True)

