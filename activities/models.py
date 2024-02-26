from django.db import models
from users.models import User
from activities import utils
import qrcode
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO




class PointsUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'Puntos'
        verbose_name = 'Punto'


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE)
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(null=True, blank=True)
    validate = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.username} - {self.activity.title}'

class Activity(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/', null=True, blank=True)
    site = models.CharField(max_length=225)
    start_date = models.DateField()
    hour = models.CharField(max_length=10, choices=utils.CHOICES)
    points = models.IntegerField()
    students = models.ManyToManyField(User, related_name='activities')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE , related_name='activitity')
    participants = models.ManyToManyField(User, related_name='activities_participated', through='Participation')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Actividades'
        verbose_name = 'Actividad'



@receiver(post_save, sender=Activity)
def generate_qr_code(sender, instance, **kwargs):
    # Verificar si la propiedad qr está vacía antes de generar el código QR
    if not instance.qr_code:
        # Desconectar el manejador de señales para evitar recursión
        post_save.disconnect(generate_qr_code, sender=Activity)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(instance.pk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        filename = f"qr_{instance.title}.png"
        instance.qr_code.save(filename, SimpleUploadedFile(filename, buffer.getvalue()))

        # Reconectar el manejador de señales después de guardar
        post_save.connect(generate_qr_code, sender=Activity)
