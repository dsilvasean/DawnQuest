# Generated by Django 4.2.9 on 2024-02-02 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_publication_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='to_scrape',
            field=models.BooleanField(default=False),
        ),
    ]
