# Generated by Django 4.2.9 on 2024-01-20 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='to_scrape',
            field=models.BooleanField(default=False),
        ),
    ]
