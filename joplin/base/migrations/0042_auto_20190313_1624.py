# Generated by Django 2.0.13 on 2019-03-13 16:24

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_auto_20190216_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='informationpage',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.DepartmentPage', verbose_name='Select a Department'),
        ),
        migrations.AddField(
            model_name='processpage',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.DepartmentPage', verbose_name='Select a Department'),
        ),
        migrations.AddField(
            model_name='servicepage',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.DepartmentPage', verbose_name='Select a Department'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'link', 'ul', 'ol'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_ar',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'link', 'ul', 'ol'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_en',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'link', 'ul', 'ol'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_es',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'link', 'ul', 'ol'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
        migrations.AlterField(
            model_name='informationpage',
            name='options_vi',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'link', 'ul', 'ol'], label='Option'))], blank=True, help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).', null=True, verbose_name='Add option sections as needed.'),
        ),
    ]
