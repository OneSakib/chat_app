from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.db.models import Exists, Subquery, OuterRef, Q
from .models import *
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
        return redirect(reverse_lazy('login'))


# Chat

@method_decorator(login_required(login_url='/login'), name='dispatch')
class Index(View):
    def get(self, request):
        conversions = Conversions.objects.filter(participants=request.user)
        context = {'conversions': conversions}
        return render(request, 'chat/index.html', context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class FindFriends(View):
    def get(self, request):
        users = User.objects.annotate(is_friend=Exists(
            Conversions.objects.filter(Q(participants__in=OuterRef('id')) & Q(participants__in=[request.user.id])))).exclude(id=request.user.id)
        context = {'users': users}
        return render(request, 'chat/find_friends.html', context)

    def post(self, request):
        user_id = request.POST.get('user_id')
        obj = Conversions.objects.create()
        other_user = User.objects.get(id=user_id)
        obj.participants.add(request.user)
        obj.participants.add(other_user)
        obj.save()
        return redirect(reverse_lazy('find_friends'))


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ManageProfile(View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {'u_form': u_form, 'p_form': p_form}
        return render(request, 'chat/manage_profile.html', context)

    def post(self, request):
        u_form = UserUpdateForm(data=request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            data=request.POST, files=request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect(reverse_lazy('index'))
        context = {'u_form': u_form, 'p_form': p_form}
        return render(request, 'chat/manage_profile.html', context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class Room(View):
    def get(self, request, room_id):
        return render(request, 'chat/room.html', {'room_id': room_id})
