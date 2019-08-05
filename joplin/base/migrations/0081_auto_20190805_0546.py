# Generated by Django 2.2.3 on 2019-08-05 05:46

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0080_guidepage_guidepagecontact_guidepagerelateddepartments_guidepagetopic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidepage',
            name='sections',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StructBlock([('section_heading', wagtail.core.blocks.TextBlock('Heading')), ('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(label='Page', page_type=['base.InformationPage', 'base.ServicePage'])))], label='Section'))], blank=True, verbose_name='Add a section header and pages to each section'),
        ),
    ]
