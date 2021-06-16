# Generated by Django 3.0.3 on 2020-03-15 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0006_auto_20200313_1011'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chat',
            name='meeting',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='meeting.Meeting'),
        ),
    ]
