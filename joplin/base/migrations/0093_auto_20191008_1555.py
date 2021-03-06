# Generated by Django 2.2.6 on 2019-10-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0092_auto_20191003_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentpage',
            name='mission',
            field=models.TextField(blank=True, verbose_name='Mission'),
        ),
        migrations.AlterField(
            model_name='departmentpage',
            name='mission_ar',
            field=models.TextField(blank=True, null=True, verbose_name='Mission'),
        ),
        migrations.AlterField(
            model_name='departmentpage',
            name='mission_en',
            field=models.TextField(blank=True, null=True, verbose_name='Mission'),
        ),
        migrations.AlterField(
            model_name='departmentpage',
            name='mission_es',
            field=models.TextField(blank=True, null=True, verbose_name='Mission'),
        ),
        migrations.AlterField(
            model_name='departmentpage',
            name='mission_vi',
            field=models.TextField(blank=True, null=True, verbose_name='Mission'),
        ),
    ]
