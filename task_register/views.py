from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *


def registration(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if username and password:
            User.objects.create_user(
                username=username,
                password=password
            )
            return redirect('login')
    return render(request, 'registration.html')


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(
            request,username=data.get('username'),password=data.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def home_page(request):
    task = Task.objects.filter(user=request.user)
    return render(request, 'home.html', {'task': task})


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def create_task(request):
    if request.method == 'POST':
        data = request.POST
        Task.objects.create(
            title=data['title'],
            caption=data['caption'],
            user=request.user
        )
        return redirect('my_task')
    return render(request, 'create_task.html')


@login_required
def show_task(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(user=request.user)
    if query:
        tasks = tasks.filter(Q(title__icontains=query)
        )
    return render(request, 'show_task.html', {'tasks': tasks,'query':query})


@login_required
def update_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.caption = request.POST['caption']
        task.save()
        return redirect('my_task')
    return render(request, 'update_task.html', {'task': task})


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    task.delete()
    return redirect('my_task')
