# Generated by Django 3.1.7 on 2021-05-19 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udachi', '0013_bronirovanie_kolvo_gostei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bronirovanie',
            name='telephone',
            field=models.CharField(max_length=255, verbose_name='Tелефон'),
        ),
    ]
