# Generated by Django 4.2.9 on 2024-01-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0002_alter_publication_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(unique=True)),
                ('to_scrape', models.BooleanField(default=False)),
            ],
        ),
    ]
