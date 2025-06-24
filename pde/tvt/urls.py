from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_table_view, name='document_table'),
    path('traces/', views.hello_world, name='traces'),
]
