from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

from .models import Request, Class, User, Teacher, Student




def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    return render(request, 'index.html')


@custom_login_required
def example_view(request):
    return render(request, 'example.html')


def login_view(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        user = User.objects.filter(login=login).first()

        print(password)
        print(user.password)
        if user and user.password == password:
            request.session['user_id'] = user.id
            # if user.type == User.STUDENT:
            #     return redirect('main')
            # else:
            return redirect('main')
        else:
            messages.error(request, 'Неправильний логін або пароль!')
            return render(request, 'login.html')


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
            return render(request, 'register.html', {'classes': Class.objects.all(), 'error': 'Паролі не співпадають'})

        hashed_password = make_password(password)

        request_obj = Request(
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            login=login,
            class_id=class_id,
            password=hashed_password
        )
        request_obj.save()

        return redirect('home')

    classes = Class.objects.all()
    return render(request, 'register.html', {'classes': classes})


@custom_login_required
def main_view(request):
    return render(request, 'main.html', {'user_type' : 'student'})

from django.http import JsonResponse
from .models import Subject, Teacher, Student
import base64
from django.core.files.base import ContentFile

@custom_login_required
def student_lessons(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    print(user)

    if user.type == 'student':
        student = Student.objects.get(user=user)
        subjects = Subject.objects.filter(teachersclassessubject__class_id=student.class_id)
        lessons_data = [{"name": subject.name, "description": subject.description or "", "id": subject.id} for subject in subjects]
        print(lessons_data)
        return JsonResponse({"lessons": lessons_data})

    return JsonResponse({"error": "Unauthorized"}, status=401)


def get_student_teachers(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    student = Student.objects.get(user=user)

    # Отримуємо клас учня
    student_class = student.class_id

    # Знаходимо всіх вчителів, які викладають у цьому класі
    teachers = Teacher.objects.filter(teachersclassessubject__class_id=student_class).distinct()

    # Створюємо список з іменами та фото вчителів
    teachers_list = [
        {
            'name': f"{teacher.user.first_name} {teacher.user.last_name}",
            'photo': base64.b64encode(teacher.user.photo).decode('utf-8') if teacher.user.photo else None
        }
        for teacher in teachers
    ]

    return JsonResponse({'teachers': teachers_list})
