# Generated by Django 2.2.1 on 2019-05-30 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0067_auto_20190522_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.DepartmentPage', verbose_name='Select a Department'),
        ),
    ]
