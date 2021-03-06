# Generated by Django 3.1.7 on 2021-05-30 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('udachi', '0017_auto_20210530_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='zakaz',
            name='bronirovanie',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='udachi.bronirovanie', verbose_name='Бронирование'),
        ),
        migrations.AddField(
            model_name='zakaz',
            name='email',
            field=models.EmailField(default='kafeudachismolenka@gmail.com', max_length=254, verbose_name='Электронная почта'),
        ),
    ]
