# Generated by Django 2.2.5 on 2019-09-27 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0089_auto_20190926_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officialdocumentpageofficialdocument',
            name='link',
        ),
    ]
