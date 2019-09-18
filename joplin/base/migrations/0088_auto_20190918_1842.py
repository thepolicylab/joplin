# Generated by Django 2.2.5 on 2019-09-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0087_auto_20190912_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentpage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='guidepage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='informationpage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='officialdocumentpage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='processpage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='servicepage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='topiccollectionpage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
        migrations.AddField(
            model_name='topicpage',
            name='coa_global',
            field=models.BooleanField(default=False, verbose_name='Make this a top level page'),
        ),
    ]
