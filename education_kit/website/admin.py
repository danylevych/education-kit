from django.contrib import admin
from .models import Classes, Meetings, Requests, Students, Subjects, Teachers, TeachersClasses, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Classes)
admin.site.register(Meetings)
admin.site.register(Requests)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Teachers)
admin.site.register(TeachersClasses)
