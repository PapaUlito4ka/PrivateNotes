from django.urls import path, include

import core.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('list_notes', views.list_notes, name='list_notes'),
    path('create_note', views.create_note, name='create_note'),
]