# Generated by Django 2.0.13 on 2019-04-18 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_auto_20190417_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicepage',
            name='image',
        ),
    ]
