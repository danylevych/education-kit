from django.db import models

class User(models.Model):
    STUDENT = 'student'
    TEACHER = 'teacher'
    USER_TYPES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher')
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=7, choices=USER_TYPES)
    photo = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Class(models.Model):
    name = models.CharField(max_length=35)
    supervisor = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class Subject(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True, null=True)
    photo = models.BinaryField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Request(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.login

class Meeting(models.Model):
    reference = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.reference

class TeachersClassesSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'class_id', 'subject'], name='unique_teacher_class_subject')
        ]
