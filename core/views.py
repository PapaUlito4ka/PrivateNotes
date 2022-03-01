from django.contrib.auth import authenticate, login as login_
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from core.forms import LoginForm, RegisterForm, NoteForm
import core.services as services
from core.exceptions import handle_error


def home(request: HttpRequest):
    context = {}
    return render(request, 'home.html', context=context)


def login(request: HttpRequest):
    context = dict()

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context=context)

    if request.method == 'POST':
        context['form'] = LoginForm(request.POST, request.FILES)
        if context['form'].is_valid():
            raw_user = request.POST
            user = authenticate(
                request,
                username=raw_user['email'],
                password=raw_user['password']
            )
            if user is None:
                context['errors'] = 'Wrong email or password was passed'
                return render(request, 'login.html', context)
            login_(request, user)
            return redirect(reverse('list_notes'))
        return render(request, 'login.html', context)


def register(request: HttpRequest):
    context = dict()

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('profile', kwargs={'id': request.user.id}))
        context['form'] = RegisterForm()
        return render(request, 'register.html', context=context)

    if request.method == 'POST':
        context['form'] = RegisterForm(request.POST, request.FILES)
        if context['form'].is_valid():
            try:
                created_user = services.UserService.create(request.POST)
            except Exception as e:
                handle_error(context, e)
                return render(request, 'register.html', context)
            user = authenticate(
                request,
                username=created_user.username,
                password=request.POST['password']
            )
            login_(request, user)
            return redirect(reverse('list_notes'))
        return render(request, 'register.html', context=context)


@login_required(login_url='/login')
def list_notes(request: HttpRequest):
    context = {
        'page': request.GET.get('page', 1)
    }

    if request.method == 'GET':
        context['notes'] = services.NoteService.list(request.user.id, context['page'])
        return render(request, 'list_notes.html', context=context)


@login_required(login_url='/login')
def create_note(request: HttpRequest):
    context = dict()

    if request.method == 'GET':
        context['form'] = NoteForm()
        return render(request, 'create_note.html', context=context)

    if request.method == 'POST':
        context['form'] = NoteForm(request.POST, request.FILES)
        if context['form'].is_valid():
            try:
                services.NoteService.create(request.POST, request.user.id)
            except Exception as e:
                handle_error(context, e)
                return render(request, 'create_note.html', context=context)
            return redirect(reverse('list_notes'))
        return render(request, 'create_note.html', context=context)

