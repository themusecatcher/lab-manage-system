# Generated by Django 3.0.3 on 2020-03-19 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('literature', '0003_auto_20200317_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='literature',
            name='literature_comment',
            field=models.IntegerField(default=0, verbose_name='文献评论量'),
        ),
        migrations.AddField(
            model_name='literature',
            name='literature_view',
            field=models.IntegerField(default=0, verbose_name='文献访问量'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(verbose_name='评论内容')),
                ('comment_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='评论时间')),
                ('comment_literature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='literature.Literature', verbose_name='评论文献')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
            ],
            options={
                'verbose_name': '文献评论',
                'verbose_name_plural': '文献评论',
            },
        ),
    ]
