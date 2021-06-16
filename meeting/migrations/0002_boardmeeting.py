# Generated by Django 3.0.3 on 2020-03-12 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardMeeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=100, verbose_name='会议留言的主题')),
                ('content', models.TextField(default='', verbose_name='会议留言内容')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='会议留言时间')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meeting.Meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '信息反馈',
                'verbose_name_plural': '信息反馈',
            },
        ),
    ]