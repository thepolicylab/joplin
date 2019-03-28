# Generated by Django 2.0.13 on 2019-03-28 08:16

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0046_auto_20190328_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentpage',
            name='top_services',
            field=wagtail.core.fields.StreamField([('url', wagtail.core.blocks.URLBlock(label='Link to top service'))], blank=True, verbose_name='Paste links to top services'),
        ),
    ]
