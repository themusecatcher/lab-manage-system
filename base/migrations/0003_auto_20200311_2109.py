# Generated by Django 3.0.3 on 2020-03-11 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20200311_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_department',
        ),
        migrations.AddField(
            model_name='user',
            name='user_major',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Major'),
        ),
    ]
