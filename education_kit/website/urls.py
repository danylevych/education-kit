from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('main/', views.main_view, name='main'),
    path('lessons/', views.student_lessons, name='student_lessons'),
    path('get_student_teachers/', views.get_student_teachers, name='teachers'),
    path('settings_partial/', views.settings_partial, name='settings_partial'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('requests_partial/', views.requests_partial, name='requests_partial'),
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),


    path('logout/', views.logout_view, name='logout'),
]
