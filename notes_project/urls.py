from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from notes import views as note_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', note_views.home, name='home'),
    path('register/', note_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('notes/', include('notes.urls')),
]
