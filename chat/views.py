from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
# Create your views here.


# Auth

class Signup(View):
    def get(self, request):
        form = NewUserForm()
        return render(request, 'auth/signup.html', {'form': form})

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('index'))
        return render(request, 'auth/signup.html', {'form': form})


class UserLogin(View):
    def get(self, request):
        form = AuthenticationForm(request)
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect(reverse_lazy('index'))
        return render(request, 'auth/login.html', {'form': form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('logins'))


# Chat

@method_decorator(login_required(login_url='/login'), name='dispatch')
class Index(View):
    def get(self, request):
        return render(request, 'chat/index.html')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class Room(View):
    def get(self, request, room_name):
        return render(request, 'chat/room.html', {'room_name': room_name})
