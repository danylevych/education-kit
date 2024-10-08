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
from django.shortcuts import render, get_object_or_404, redirect

from .models import Request, Class, User, Teacher, Student, TeachersClassesSubject, Meeting

import random
import string
import uuid
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Subject, User, Teacher, Class, Meeting
import datetime



def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    return render(request, 'index.html')



def login_view(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        user = User.objects.filter(login=login).first()
        if user and user.password == password:
            update_session_data(request, user)
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
        class_id = request.POST.get('class_id')

        if password != confirm_password:
            return render(request, 'register.html', {'classes': Class.objects.all(), 'error': 'Паролі не співпадають'})

        try:
            class_instance = Class.objects.get(id=class_id)  # Отримайте об'єкт Class
        except Class.DoesNotExist:
            return render(request, 'register.html', {'classes': Class.objects.all(), 'error': 'Вказаний клас не існує'})

        request_obj = Request(
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            login=login,
            class_id=class_instance,
            password=password
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


def settings_partial(request):
    if request.method == 'POST':
        settings_post(request)
        return redirect('main')

    return render(request, 'settings_partial.html')


def settings_post(request):
    user = User.objects.get(id=request.session['user_id'])

    surname = request.POST.get('surname')
    name = request.POST.get('name')
    patronymic = request.POST.get('patronymic')
    login = request.POST.get('login')
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')

    if surname and surname != user.last_name:
        user.last_name = surname
    if name and name != user.first_name:
        user.first_name = name
    if patronymic and patronymic != user.father_name:
        user.father_name = patronymic
    if login and login != user.login:
        user.login = login

    if old_password and new_password:
        if old_password == user.password:
            user.password = new_password
        else:
            messages.error(request, 'Старий пароль неправильний!')
            return render(request, 'settings_partial.html')

    try:
        user.save()
        update_session_data(request, user)
        messages.success(request, 'Зміни успішно збережено!')
    except Exception as e:
        messages.error(request, f'Сталася помилка під час збереження: {str(e)}')


def update_session_data(request, user):
    request.session['user_id'] = user.id
    request.session['user_last_name'] = user.last_name
    request.session['user_first_name'] = user.first_name
    request.session['user_father_name'] = user.father_name
    request.session['user_login'] = user.login
    request.session['user_type'] = user.type
    request.session['user_full_name'] = f"{user.last_name} {user.first_name} {user.father_name}"


@custom_login_required
def lesson_detail(request, id):
    subject = Subject.objects.get(id=id)
    metting = Meeting.objects.filter(subject=subject).last()
    context = {
        'subject': subject,
        'meeting': metting
    }
    return render(request, 'connect_to_meeting.html', context)


@custom_login_required
def requests_partial(request):
    user = User.objects.get(id=request.session['user_id'])

    if user.type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=user)
            class_obj = Class.objects.get(supervisor=teacher)
            requests = Request.objects.filter(class_id=class_obj.id)
            return render(request, 'requests_partial.html', {'requests':requests})

        except Teacher.DoesNotExist:
            return HttpResponse('Teacher not found', status=404)
        except Class.DoesNotExist:
            return HttpResponse('Class not found', status=404)

    return HttpResponse('Unauthorized', status=401)


def logout_view(request):
    request.session.flush()
    return redirect('home')


def approve_request(request, request_id):
    if request.method == 'POST':
        request_obj = Request.objects.get(id=request_id)
        user = User(
            first_name=request_obj.first_name,
            last_name=request_obj.last_name,
            father_name=request_obj.father_name,
            login=request_obj.login,
            password=request_obj.password,
            type='student'
        )
        user.save()

        student = Student(user=user, class_id=request_obj.class_id)
        student.save()
        request_obj.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def reject_request(request, request_id):
    if request.method == 'POST':
        request_obj = Request.objects.get(id=request_id)
        request_obj.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def meetings_list_partial(request):
    user = User.objects.get(id=request.session['user_id'])

    if user.type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=user)
            subjects = TeachersClassesSubject.objects.filter(teacher=teacher).values_list('subject', flat=True)
            meetings = Meeting.objects.filter(subject__in=subjects)
            return render(request, 'meetings_list_partial.html', {'meetings': meetings})

        except Teacher.DoesNotExist:
            return HttpResponse('Teacher not found', status=404)

    return HttpResponse('Unauthorized', status=403)

def delete_meeting(request, meeting_id):
    if request.method == 'POST':
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            meeting.delete()
            return JsonResponse({'success': True})
        except Meeting.DoesNotExist:
            return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})


def meetings_view(request):
    user = User.objects.get(id=request.session['user_id'])

    if user.type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=user)
            subjects = Subject.objects.filter(teacher=teacher)

            return render(request, 'meetings.html', {'meetings_create': subjects})
        except Teacher.DoesNotExist:
            return HttpResponse('Teacher not found', status=404)

    return HttpResponse('Unauthorized', status=403)


def get_google_service_credential():
    credentials = service_account.Credentials.from_service_account_file(
        '/home/danylevych/Downloads/education-kit-435009-cef74098c49d.json',
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

def generate_meet_id():
    """Generate a Meet ID in the format xxx-xxxx-xxx."""
    letters = string.ascii_lowercase
    part1 = ''.join(random.choice(letters) for _ in range(3))
    part2 = ''.join(random.choice(letters) for _ in range(4))
    part3 = ''.join(random.choice(letters) for _ in range(3))
    return f"{part1}-{part2}-{part3}"

def create_meeting_view(request, id):
    subject = get_object_or_404(Subject, id=id)
    user = User.objects.get(id=request.session['user_id'])

    if user.type != 'teacher':
        return HttpResponse('Unauthorized', status=403)

    teacher = get_object_or_404(Teacher, user=user)

    if request.method == 'POST':
        meeting_name = request.POST.get('meeting_name')
        class_id = request.POST.get('class_id')

        if meeting_name and class_id:
            class_obj = get_object_or_404(Class, id=class_id)

            service = get_google_service_credential()

            meetURL = generate_meet_id()   # Generate a unique meeting URL

            event = {
                'summary': meeting_name,
                'description': 'Meeting for subject: ' + subject.name,
                'start': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(minutes=3)).isoformat(),
                    'timeZone': 'Europe/Kiev',
                },
                'end': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat(),
                    'timeZone': 'Europe/Kiev',
                },
                'conferenceData': {
                    'entryPoints': [
                        {
                            'entryPointType': 'video',
                            'uri': f'https://meet.google.com/{meetURL}',
                            'label': f'meet.google.com/{meetURL}'
                        }
                    ],
                    'conferenceId': meetURL,
                    'conferenceSolution': {
                        'key': {
                            'type': 'hangoutsMeet'
                        }
                    }
                },
            }

            try:
                # Create the event with Google Calendar API
                event_result = service.events().insert(
                    calendarId='58eb06efc1be0bf127853aa5d83dc7e87eb29883287e37576ff3bc437c8e6e3b@group.calendar.google.com',
                    body=event,
                    conferenceDataVersion=1
                ).execute()

                # Save the meeting info to your database
                meeting = Meeting(subject=subject, description=meeting_name, class_obj=class_obj, reference=f'https://meet.google.com/{meetURL}')
                meeting.save()

                return redirect('main')

            except Exception as e:
                print(f'Error creating event: {e}')
                return HttpResponse('Error creating meeting', status=500)

    classes = Class.objects.filter(
        id__in=TeachersClassesSubject.objects.filter(
            teacher=teacher, subject=subject
        ).values('class_id')
    )

    return render(request, 'create_meeting.html', {
        'subject': subject,
        'classes': classes
    })
