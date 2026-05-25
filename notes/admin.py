from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_archived', 'created_at', 'updated_at']
    list_filter = ['is_archived', 'created_at', 'user']
    search_fields = ['title', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
