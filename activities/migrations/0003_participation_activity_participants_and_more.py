# Generated by Django 4.0.4 on 2024-02-24 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0002_rename_activities_activity_alter_activity_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='participants',
            field=models.ManyToManyField(related_name='activities_participated', through='activities.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participation',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activity'),
        ),
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
