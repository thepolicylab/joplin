# Generated by Django 2.2.7 on 2019-12-05 21:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import phonenumber_field.modelfields
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('base', '0100_auto_20191121_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author_notes', wagtail.core.fields.RichTextField(blank=True, verbose_name='Notes for authors (Not visible on the resident facing site)')),
                ('coa_global', models.BooleanField(default=False, verbose_name='Make this a top level page')),
                ('alternate_name', models.CharField(blank=True, help_text='Use this field if the building has a second name, or is inside a larger facility', max_length=255, verbose_name='Location alternate name')),
                ('physical_street', models.CharField(blank=True, max_length=255, verbose_name='Street')),
                ('physical_unit', models.CharField(blank=True, max_length=255, verbose_name='Floor/Suite #')),
                ('physical_city', models.CharField(blank=True, default='Austin', max_length=255, verbose_name='City')),
                ('physical_state', models.CharField(blank=True, default='TX', max_length=255, verbose_name='State')),
                ('physical_country', models.CharField(blank=True, default='USA', max_length=255)),
                ('physical_zip', models.CharField(blank=True, max_length=255, verbose_name='ZIP')),
                ('phone_description', models.CharField(blank=True, max_length=255, verbose_name='Phone description')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone(only if location has a dedicated number)')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email address')),
                ('mailing_street', models.CharField(blank=True, max_length=255, verbose_name='Street or PO box')),
                ('mailing_city', models.CharField(blank=True, default='Austin', max_length=255, verbose_name='City')),
                ('mailing_state', models.CharField(blank=True, default='TX', max_length=255, verbose_name='State')),
                ('mailing_country', models.CharField(blank=True, default='USA', max_length=255)),
                ('mailing_zip', models.CharField(blank=True, max_length=255, verbose_name='ZIP')),
                ('nearest_bus_1', models.IntegerField(blank=True)),
                ('nearest_bus_2', models.IntegerField(blank=True)),
                ('nearest_bus_3', models.IntegerField(blank=True)),
                ('hours_exceptions', models.TextField(blank=True, max_length=255)),
                ('monday_open', models.BooleanField(default=False)),
                ('monday_start_time', models.TimeField(blank=True, null=True)),
                ('monday_end_time', models.TimeField(blank=True, null=True)),
                ('monday_start_time_2', models.TimeField(blank=True, null=True)),
                ('monday_end_time_2', models.TimeField(blank=True, null=True)),
                ('tuesday_open', models.BooleanField(default=False)),
                ('tuesday_start_time', models.TimeField(blank=True, null=True)),
                ('tuesday_end_time', models.TimeField(blank=True, null=True)),
                ('tuesday_start_time_2', models.TimeField(blank=True, null=True)),
                ('tuesday_end_time_2', models.TimeField(blank=True, null=True)),
                ('wednesday_open', models.BooleanField(default=False)),
                ('wednesday_start_time', models.TimeField(blank=True, null=True)),
                ('wednesday_end_time', models.TimeField(blank=True, null=True)),
                ('wednesday_start_time_2', models.TimeField(blank=True, null=True)),
                ('wednesday_end_time_2', models.TimeField(blank=True, null=True)),
                ('thursday_open', models.BooleanField(default=False)),
                ('thursday_start_time', models.TimeField(blank=True, null=True)),
                ('thursday_end_time', models.TimeField(blank=True, null=True)),
                ('thursday_start_time_2', models.TimeField(blank=True, null=True)),
                ('thursday_end_time_2', models.TimeField(blank=True, null=True)),
                ('friday_open', models.BooleanField(default=False)),
                ('friday_start_time', models.TimeField(blank=True, null=True)),
                ('friday_end_time', models.TimeField(blank=True, null=True)),
                ('friday_start_time_2', models.TimeField(blank=True, null=True)),
                ('friday_end_time_2', models.TimeField(blank=True, null=True)),
                ('saturday_open', models.BooleanField(default=False)),
                ('saturday_start_time', models.TimeField(blank=True, null=True)),
                ('saturday_end_time', models.TimeField(blank=True, null=True)),
                ('saturday_start_time_2', models.TimeField(blank=True, null=True)),
                ('saturday_end_time_2', models.TimeField(blank=True, null=True)),
                ('sunday_open', models.BooleanField(default=False)),
                ('sunday_start_time', models.TimeField(blank=True, null=True)),
                ('sunday_end_time', models.TimeField(blank=True, null=True)),
                ('sunday_start_time_2', models.TimeField(blank=True, null=True)),
                ('sunday_end_time_2', models.TimeField(blank=True, null=True)),
                ('physical_location_photo', models.ForeignKey(blank=True, help_text='Use this to show an exterior of the location.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.TranslatedImage', verbose_name='Choose a banner image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LocationPageRelatedServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_exceptions', models.TextField(blank=True, max_length=255)),
                ('monday_open', models.BooleanField(default=False)),
                ('monday_start_time', models.TimeField(blank=True, null=True)),
                ('monday_end_time', models.TimeField(blank=True, null=True)),
                ('monday_start_time_2', models.TimeField(blank=True, null=True)),
                ('monday_end_time_2', models.TimeField(blank=True, null=True)),
                ('tuesday_open', models.BooleanField(default=False)),
                ('tuesday_start_time', models.TimeField(blank=True, null=True)),
                ('tuesday_end_time', models.TimeField(blank=True, null=True)),
                ('tuesday_start_time_2', models.TimeField(blank=True, null=True)),
                ('tuesday_end_time_2', models.TimeField(blank=True, null=True)),
                ('wednesday_open', models.BooleanField(default=False)),
                ('wednesday_start_time', models.TimeField(blank=True, null=True)),
                ('wednesday_end_time', models.TimeField(blank=True, null=True)),
                ('wednesday_start_time_2', models.TimeField(blank=True, null=True)),
                ('wednesday_end_time_2', models.TimeField(blank=True, null=True)),
                ('thursday_open', models.BooleanField(default=False)),
                ('thursday_start_time', models.TimeField(blank=True, null=True)),
                ('thursday_end_time', models.TimeField(blank=True, null=True)),
                ('thursday_start_time_2', models.TimeField(blank=True, null=True)),
                ('thursday_end_time_2', models.TimeField(blank=True, null=True)),
                ('friday_open', models.BooleanField(default=False)),
                ('friday_start_time', models.TimeField(blank=True, null=True)),
                ('friday_end_time', models.TimeField(blank=True, null=True)),
                ('friday_start_time_2', models.TimeField(blank=True, null=True)),
                ('friday_end_time_2', models.TimeField(blank=True, null=True)),
                ('saturday_open', models.BooleanField(default=False)),
                ('saturday_start_time', models.TimeField(blank=True, null=True)),
                ('saturday_end_time', models.TimeField(blank=True, null=True)),
                ('saturday_start_time_2', models.TimeField(blank=True, null=True)),
                ('saturday_end_time_2', models.TimeField(blank=True, null=True)),
                ('sunday_open', models.BooleanField(default=False)),
                ('sunday_start_time', models.TimeField(blank=True, null=True)),
                ('sunday_end_time', models.TimeField(blank=True, null=True)),
                ('sunday_start_time_2', models.TimeField(blank=True, null=True)),
                ('sunday_end_time_2', models.TimeField(blank=True, null=True)),
                ('page', modelcluster.fields.ParentalKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_services', to='locations.LocationPage')),
                ('related_service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.ServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
