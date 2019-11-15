# Generated by Django 2.2.7 on 2019-11-15 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('locations', '0002_auto_20191115_0052'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='author_notes',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='coa_global',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='updated_at',
        ),
    ]
