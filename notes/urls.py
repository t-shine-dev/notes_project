from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_note, name='create_note'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('<int:pk>/delete/', views.delete_note, name='delete_note'),
    path('<int:pk>/archive/', views.toggle_archive, name='toggle_archive'),
    path('archived/', views.archived_notes, name='archived_notes'),
]
