# Generated by Django 2.2.1 on 2019-05-16 09:11

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0064_auto_20190516_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationpage',
            name='options',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_ar',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_en',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_es',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_vi',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
    ]
