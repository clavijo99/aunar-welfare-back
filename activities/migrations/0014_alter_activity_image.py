# Generated by Django 4.0.4 on 2024-02-24 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0013_activity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='activities'),
        ),
    ]
