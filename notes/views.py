from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note
from .forms import NoteForm, RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account was created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    query = request.GET.get('q', '').strip()
    notes = Note.objects.filter(user=request.user, is_archived=False)
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'notes/home.html', {'notes': notes, 'query': query})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully.')
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})


@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully.')
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')
        return redirect('home')
    return render(request, 'notes/delete_note.html', {'note': note})


@login_required
def toggle_archive(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_archived = not note.is_archived
    note.save()
    status = 'archived' if note.is_archived else 'restored'
    messages.success(request, f'Note {status} successfully.')
    return redirect(request.GET.get('next', 'home'))


@login_required
def archived_notes(request):
    query = request.GET.get('q', '').strip()
    notes = Note.objects.filter(user=request.user, is_archived=True)
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'notes/archived.html', {'notes': notes, 'query': query})
