# Generated by Django 3.1.7 on 2021-05-21 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udachi', '0014_auto_20210519_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sotrudnic',
            name='user',
        ),
        migrations.RemoveField(
            model_name='zakaz',
            name='akzia',
        ),
        migrations.AddField(
            model_name='postavshiki',
            name='email',
            field=models.EmailField(default='kafeudachismolenka@gmail.com', max_length=254, verbose_name='Электронная почта'),
        ),
        migrations.DeleteModel(
            name='Akzia',
        ),
        migrations.DeleteModel(
            name='Sotrudnic',
        ),
    ]
