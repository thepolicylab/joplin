# Generated by Django 2.2.4 on 2019-09-05 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0083_auto_20190828_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='phone',
        ),
    ]