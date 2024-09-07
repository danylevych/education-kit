from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('example/', views.example_view, name='example'),
    path('main/', views.main_view, name='main'),
    path('lessons/', views.student_lessons, name='student_lessons'),
    path('get_student_teachers/', views.get_student_teachers, name='teachers'),
    path('sttings/', views.settings, name='settings'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
]
