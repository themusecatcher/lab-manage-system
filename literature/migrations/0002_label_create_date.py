# Generated by Django 3.0.3 on 2020-03-17 13:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('literature', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='文献标签创建时间'),
        ),
    ]
