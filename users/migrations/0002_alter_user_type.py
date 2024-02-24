# Generated by Django 4.0.4 on 2024-02-23 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('ADMINISTRATOR', 'Administrator'), ('STUDENT', 'Estudiante'), ('TEACHER', 'Maestro')], default='STUDENT', max_length=15),
        ),
    ]
