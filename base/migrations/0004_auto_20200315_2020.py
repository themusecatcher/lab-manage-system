# Generated by Django 3.0.3 on 2020-03-15 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20200311_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_banji',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Banji'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Major'),
        ),
    ]
