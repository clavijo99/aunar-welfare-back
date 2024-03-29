# Generated by Django 4.0.4 on 2024-02-25 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0016_alter_activity_day_alter_activity_hour'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityschedule',
            options={'verbose_name': 'Agendar por semana', 'verbose_name_plural': 'Agendar por semana'},
        ),
        migrations.AddField(
            model_name='activityschedule',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activa'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='activities/'),
        ),
        migrations.AlterField(
            model_name='activityschedule',
            name='day',
            field=models.CharField(choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Miércoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], max_length=10, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='activityschedule',
            name='hour_end',
            field=models.CharField(choices=[('06:00', '06:00'), ('06:30', '06:30'), ('07:00', '07:00'), ('07:30', '07:30'), ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30')], max_length=10, verbose_name='Hora final'),
        ),
        migrations.AlterField(
            model_name='activityschedule',
            name='hour_start',
            field=models.CharField(choices=[('06:00', '06:00'), ('06:30', '06:30'), ('07:00', '07:00'), ('07:30', '07:30'), ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30')], max_length=10, verbose_name='Hora de inicio'),
        ),
    ]
