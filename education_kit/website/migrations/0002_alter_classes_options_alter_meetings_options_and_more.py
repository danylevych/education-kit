# Generated by Django 5.1.1 on 2024-09-05 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classes',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='meetings',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='requests',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='students',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='subjects',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='teachers',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='teachersclasses',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'managed': False},
        ),
    ]
