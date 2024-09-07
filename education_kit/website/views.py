from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

from django.http import JsonResponse
from .models import Subject, Teacher, Student
import base64
from django.core.files.base import ContentFile

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
            if user.type == User.STUDENT:
                return redirect('main', {'user_type': 'student'})
            else:
                return redirect('main', {'user_type': 'teacher'})
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
    return render(request, 'main.html')

@custom_login_required
def student_lessons(request):
    user = User.objects.get(id=request.session['user_id'])

    if user.type == 'student':
        student = Student.objects.get(user=user)
        subjects = Subject.objects.filter(teachersclassessubject__class_id=student.class_id)
        lessons_data = [{"name": subject.name, "description": subject.description or "", "id": subject.id} for subject in subjects]
        print(lessons_data)
        return JsonResponse({"lessons": lessons_data})

    return JsonResponse({"error": "Unauthorized"}, status=401)

@custom_login_required
def get_student_teachers(request):
    user = User.objects.get(id=request.session['user_id'])
    student = Student.objects.get(user=user)

    student_class = student.class_id

    teachers = Teacher.objects.filter(teachersclassessubject__class_id=student_class).distinct()

    teachers_list = [
        {
            'name': f"{teacher.user.first_name} {teacher.user.last_name}",
            'photo': base64.b64encode(teacher.user.photo).decode('utf-8') if teacher.user.photo else None,
            'email': teacher.email,
            'phone': teacher.phone,
        }
        for teacher in teachers
    ]

    return JsonResponse({'teachers': teachers_list})


@custom_login_required
def settings(request):
    return render(request, 'settings.html')



@custom_login_required
def lesson_detail(request, id):
    subject = Subject.objects.get(id=id)
    context = {
        'subject': subject,
    }
    return render(request, 'connect_to_meeting.html', context)


@custom_login_required
def requests_view(request):
    user = User.objects.get(id=request.session['user_id'])

    if user.type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=user)
            class_obj = Class.objects.get(supervisor=teacher)
            requests = Request.objects.filter(class_id=class_obj.id)
        except Teacher.DoesNotExist:
            return HttpResponse('Teacher not found', status=404)
        except Class.DoesNotExist:
            return HttpResponse('Class not found', status=404)

        return render(request, 'requests.html', {'requests': requests})

    return HttpResponse('Unauthorized', status=401)


def logout_view(reauest):
    del reauest.session['user_id']
    return redirect('home')
