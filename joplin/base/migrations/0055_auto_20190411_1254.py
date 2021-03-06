# Generated by Django 2.0.13 on 2019-04-11 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0054_auto_20190411_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='theme',
        ),
        migrations.AlterField(
            model_name='informationpagetopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.TopicPage', verbose_name='Select a Topic'),
        ),
        migrations.AlterField(
            model_name='processpagetopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.TopicPage', verbose_name='Select a Topic'),
        ),
        migrations.AlterField(
            model_name='servicepagetopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.TopicPage', verbose_name='Select a Topic'),
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
