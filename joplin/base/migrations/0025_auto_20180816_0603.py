# Generated by Django 2.0.8 on 2018-08-16 06:03

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_auto_20180801_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePageStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('step_description', wagtail.core.fields.RichTextField(blank=True, verbose_name='Step description')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='additional_content',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Write any additional content describing the service', verbose_name='Additional content'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='additional_content_ar',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Write any additional content describing the service', null=True, verbose_name='Additional content'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='additional_content_en',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Write any additional content describing the service', null=True, verbose_name='Additional content'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='additional_content_es',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Write any additional content describing the service', null=True, verbose_name='Additional content'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='additional_content_vi',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Write any additional content describing the service', null=True, verbose_name='Additional content'),
        ),
        migrations.AddField(
            model_name='servicepagestep',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_steps', to='base.ServicePage'),
        ),
    ]