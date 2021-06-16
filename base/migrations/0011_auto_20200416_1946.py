# Generated by Django 3.0.3 on 2020-04-16 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20200416_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duty',
            name='sex',
            field=models.IntegerField(choices=[(0, '女'), (1, '男')], default=0, verbose_name='性别(0:男/1:女)'),
        ),
    ]
