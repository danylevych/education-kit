from django.contrib import admin
from .models import User, Class, Meeting, Request, Student, Subject, Teacher, TeachersClassesSubject

# Register your models here.
admin.site.register(User)
admin.site.register(Class)
admin.site.register(Meeting)
admin.site.register(Request)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TeachersClassesSubject)
