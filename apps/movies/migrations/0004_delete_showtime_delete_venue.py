# Generated by Django 5.1.6 on 2025-02-19 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_venue_alter_showtime_options_alter_showtime_datetime_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Showtime',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
    ]
