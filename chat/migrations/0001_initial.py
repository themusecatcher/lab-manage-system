# Generated by Django 3.0.3 on 2020-03-15 09:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meeting', '0006_auto_20200313_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_name', models.CharField(max_length=100, unique=True, verbose_name='聊天室名称')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='聊天室创建时间')),
                ('meeting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meeting.Meeting')),
            ],
            options={
                'verbose_name': '聊天室',
                'verbose_name_plural': '聊天室',
            },
        ),
    ]