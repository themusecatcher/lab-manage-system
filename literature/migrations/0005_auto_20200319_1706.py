# Generated by Django 3.0.3 on 2020-03-19 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('literature', '0004_auto_20200319_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='literature_file',
            field=models.FileField(blank=True, upload_to='upload/literatures/', verbose_name='文献文件'),
        ),
    ]
