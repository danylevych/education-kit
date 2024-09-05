from django.db import models

class Classes(models.Model):
    name = models.CharField(max_length=35)
    supervisor = models.ForeignKey('Teachers', models.DO_NOTHING, blank=True, null=True, related_name='supervised_classes')

    class Meta:
        managed = False
        db_table = 'Classes'

class Meetings(models.Model):
    reference = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    subject = models.ForeignKey('Subjects', models.DO_NOTHING, blank=True, null=True, related_name='meetings')

    class Meta:
        managed = False
        db_table = 'Meetings'

class Requests(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    login = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, db_column='class_id', blank=True, null=True, related_name='requests')

    class Meta:
        managed = False
        db_table = 'Requests'

class Students(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='students')
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, db_column='class_id', blank=True, null=True, related_name='students')

    class Meta:
        managed = False
        db_table = 'Students'

class Subjects(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING, blank=True, null=True, related_name='subjects')

    class Meta:
        managed = False
        db_table = 'Subjects'

class Teachers(models.Model):
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='teacher_profile')

    class Meta:
        managed = False
        db_table = 'Teachers'

class TeachersClasses(models.Model):
    teacher = models.ForeignKey(Teachers, models.DO_NOTHING, blank=True, null=True, related_name='teacher_classes')
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, db_column='class_id', blank=True, null=True, related_name='teachers_classes')

    class Meta:
        managed = False
        db_table = 'TeachersClasses'

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    login = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=7)
    photo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'
