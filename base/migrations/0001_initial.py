# Generated by Django 3.0.3 on 2020-03-11 20:43

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.TextField(default='', max_length=20, verbose_name='姓名')),
                ('introduce', models.TextField(default='什么都没留下...', verbose_name='简介')),
                ('photo', models.ImageField(blank=True, upload_to='images/user/', verbose_name='头像')),
                ('user_type', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)], default=2, verbose_name='身份标识(0:学生/1:老师/2:管理员)')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Banji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banji_name', models.TextField(default='', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.TextField(default='', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.TextField(default='', unique=True)),
            ],
            options={
                'verbose_name': '实验室',
                'verbose_name_plural': '实验室',
            },
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_name', models.TextField(default='', unique=True)),
                ('major_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
            ],
        ),
        migrations.CreateModel(
            name='DateAndLab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_week', models.IntegerField(verbose_name='开始周数')),
                ('end_week', models.IntegerField(verbose_name='结束周数')),
                ('start_day', models.IntegerField(verbose_name='开始星期')),
                ('end_day', models.IntegerField(verbose_name='结束星期')),
                ('start', models.IntegerField(verbose_name='开始节数')),
                ('end', models.IntegerField(verbose_name='结束节数')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Lab')),
            ],
            options={
                'verbose_name': '会议时间地点',
                'verbose_name_plural': '会议时间地点',
            },
        ),
    ]
