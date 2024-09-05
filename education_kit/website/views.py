from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Request, Class


def home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        pass
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        father_name = request.POST['father_name']
        login = request.POST['login']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        class_id = request.POST['class_id']

        if password != confirm_password:
            return render(request, 'register.html', {'classes': Class.objects.all()})

        hashed_password = make_password(password)

        Request.objects.create(
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            login=login,
            password=hashed_password,
            class_id_id=class_id
        )

        return redirect('login')

    classes = Class.objects.all()
    return render(request, 'register.html', {'classes': classes})
