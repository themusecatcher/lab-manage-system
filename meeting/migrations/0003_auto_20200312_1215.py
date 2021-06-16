# Generated by Django 3.0.3 on 2020-03-12 12:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0002_boardmeeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardmeeting',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='会议留言时间'),
        ),
    ]
