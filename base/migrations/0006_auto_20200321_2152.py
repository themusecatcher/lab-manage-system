# Generated by Django 3.0.3 on 2020-03-21 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0007_auto_20200315_2020'),
        ('base', '0005_auto_20200319_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banji',
            name='banji_major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Major', verbose_name='班级的专业'),
        ),
        migrations.AlterField(
            model_name='dateandlab',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Lab', verbose_name='实验室'),
        ),
        migrations.AlterField(
            model_name='dateandlab',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meeting.Meeting', verbose_name='会议'),
        ),
        migrations.AlterField(
            model_name='major',
            name='major_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Department', verbose_name='专业的学院'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_banji',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Banji', verbose_name='用户班级'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Major', verbose_name='用户专业'),
        ),
    ]
