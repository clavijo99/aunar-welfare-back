from django.db import models
from users.models import User
from activities import utils




class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity.title}'

class Activity(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    site = models.CharField(max_length=225)
    hour = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    points = models.IntegerField()
    dias_semana = models.CharField(
        max_length=20,
        choices= utils.DIAS_SEMANA_CHOICES,
        blank=True,
        null=True,
        help_text="Selecciona los días de la semana",
    )
    students = models.ManyToManyField(User, related_name='activities')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE , related_name='activitity')
    participants = models.ManyToManyField(User, related_name='activities_participated', through='Participation')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Actividades'
        verbose_name = 'Actividad'

class ActivitySchedule(models.Model):
    DAY_CHOICES = [
        ('monday', 'Lunes'),
        ('tuesday', 'Martes'),
        ('wednesday', 'Miércoles'),
        ('thursday', 'Jueves'),
        ('friday', 'Viernes'),
        ('saturday', 'Sábado'),
        ('sunday', 'Domingo'),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE ,related_name='activities_schedule', null=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    hour = models.TimeField()

    def __str__(self):
        return f"{self.activity.title} - {self.get_day_display()} {self.hour}"

    class Meta:
        unique_together = ['activity', 'day', 'hour']
